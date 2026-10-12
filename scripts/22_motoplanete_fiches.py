# -*- coding: utf-8 -*-
"""
Etape 22 : fiches techniques de Motoplanete pour combler les donnees manquantes.

Respecte le robots.txt du site : seules les fiches listees dans son sitemap sont
lues (jamais /ajax/*), avec le delai de 10 s demande (Crawl-delay). Le robot
s'identifie et s'arrete sur toute reponse 403/429 : jamais de contournement.

Phases (reprenables, le cache est ecrit au fil de l'eau) :
  1. index  : lit les 13 sitemaps et conserve l'adresse de chaque fiche ;
  2. match  : rattache chaque modele de notre base a une fiche, uniquement quand
              la correspondance est certaine (nom identique ou unique chez la marque) ;
  3. fetch  : lit la fiche choisie et en extrait les champs techniques.

Sortie : data/raw/motoplanete_fiches.json (non versionne). 06_export.py ne s'en sert
que pour remplir des champs VIDES : une valeur deja presente n'est jamais ecrasee.

Usage : python 22_motoplanete_fiches.py [index|match|fetch|tout] [limite]
"""
import csv, html, io, json, os, re, sys, time, unicodedata
import requests

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RAW = os.path.join(BASE, "data", "raw")
OUT = os.path.join(BASE, "data", "out")
F_INDEX = os.path.join(RAW, "motoplanete_index.json")
F_FICHES = os.path.join(RAW, "motoplanete_fiches.json")
HOTE = "https://www.motoplanete.com"
DELAI = 10.5
S = requests.Session()
S.headers.update({"User-Agent": "CylindreeBot/0.1 (+https://www.cylindree-moto.com; viktordu84@gmail.com)"})


def pause():
    time.sleep(DELAI)


def alnum(t):
    t = unicodedata.normalize("NFD", (t or "").lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in t if not unicodedata.combining(c)))


# ------------------------------------------------------------------ 1. index
def phase_index():
    if os.path.exists(F_INDEX):
        return json.load(open(F_INDEX, encoding="utf-8"))
    pause()
    r = S.get(HOTE + "/sitemap_moto.php", timeout=60)
    r.raise_for_status()
    maps = re.findall(r"<loc>([^<]+)</loc>", r.text)
    urls = []
    for i, m in enumerate(maps, 1):
        pause()
        rr = S.get(m, timeout=120)
        if rr.status_code in (403, 429):
            sys.exit("ARRET : HTTP %d sur %s" % (rr.status_code, m))
        rr.raise_for_status()
        lot = [u for u in re.findall(r"<loc>([^<]+)</loc>", rr.text) if "/contact.html" in u]
        urls += lot
        print("[index %d/%d] %d fiches" % (i, len(maps), len(lot)), flush=True)
    index = {"date": time.strftime("%Y-%m-%d"), "urls": sorted(set(urls))}
    json.dump(index, open(F_INDEX, "w", encoding="utf-8"))
    return index


# ------------------------------------------------------------------ 2. match
ALIAS_MARQUE = {"triumphmotorcyclesltd": "triumph", "royalenfield": "royalenfield"}


def decouper(url):
    m = re.match(r"https://www\.motoplanete\.com/([^/]+)/(\d+)/(.+)-((?:19|20)\d\d)/contact\.html$", url)
    if not m:
        return None
    return {"marque": m.group(1), "id": m.group(2), "modele": m.group(3), "an": int(m.group(4)), "url": url}


def charger_modeles():
    return list(csv.DictReader(io.open(os.path.join(OUT, "modeles.csv"), encoding="utf-8-sig")))


def phase_match(index):
    fiches = [x for x in (decouper(u) for u in index["urls"]) if x]
    par_marque = {}
    for f in fiches:
        par_marque.setdefault(alnum(f["marque"]), {}).setdefault(alnum(f["modele"]), []).append(f)
    resultat = {}
    for r in charger_modeles():
        marque = r["marque"]
        cle_m = ALIAS_MARQUE.get(alnum(marque), alnum(marque))
        groupes = par_marque.get(cle_m)
        if not groupes:
            continue
        nom = re.sub(r"\s*\((?:19|20)\d\d\)$", "", r["nom_affichage"])
        if alnum(nom).startswith(alnum(marque)) or alnum(nom).startswith(cle_m):
            nom = nom[len(marque):] if alnum(nom).startswith(alnum(marque)) else nom[len(cle_m):]
        ours = alnum(nom)
        if len(ours) < 2:
            continue
        exact = [k for k in groupes if k == ours]
        cands = exact
        confiance = "exact"
        if not cands:
            cands = [k for k in groupes if len(k) >= 4 and len(ours) >= 4
                     and (k.endswith(ours) or ours.endswith(k) or k.startswith(ours))]
            confiance = "approx"
            if len(cands) != 1:
                continue
        liste = groupes[cands[0]]
        ans = sorted(f["an"] for f in liste)
        debut = int(r["annee_debut"]) if r["annee_debut"] else 0
        fin = int(r["annee_fin"]) if r["annee_fin"] else 0
        # garde-fou : un meme nom peut avoir ete reutilise (Z650 de 1977 et de 2017).
        # La fiche doit tomber dans la periode de production de NOTRE modele.
        if debut:
            ok = [a for a in ans if a >= debut - 1 and (not fin or a <= fin + 1)]
        else:
            ok = ans if not fin else []
        if not ok:
            continue
        an = ok[-1] if not fin else ok[0]
        fiche = next(f for f in liste if f["an"] == an)
        resultat[r["modele_id"]] = {"url": fiche["url"], "an": an, "confiance": confiance,
                                    "nom": r["nom_affichage"], "courant": not r["annee_fin"]}
    return resultat


# ------------------------------------------------------------------ 3. fetch
def texte(raw):
    s = re.sub(r"<script.*?</script>|<style.*?</style>", "", raw, flags=re.S)
    s = re.sub(r"<[^>]+>", "\n", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\xa0 ]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n", s)


def nombre(t):
    t = (t or "").replace(" ", "").replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def parser(raw):
    s = texte(raw)
    d = {}

    def prem(pattern, flags=0, grp=1, source=None):
        m = re.search(pattern, source if source is not None else s, flags)
        return m.group(grp).strip() if m else None

    v = prem(r"Tarifs\s+Version de base\s+France\s+([\d ]+)\s*€")
    if v and nombre(v):
        d["prix_eur"] = int(nombre(v))
    ans = prem(r"Modèle commercialisé en\s+((?:\s*(?:19|20)\d\d)+)")
    if ans:
        a = [int(x) for x in re.findall(r"(?:19|20)\d\d", ans)]
        d["an_min"], d["an_max"] = min(a), max(a)
    m = re.search(r"En occasion sur Motoplanete\s*:\s*de\s*([\d ]+)\s*€\s*à\s*([\d ]+)\s*€\s*\(\s*Voir\s*(\d+)\s*annonces?", s)
    if m:
        d["occ_min"], d["occ_max"], d["occ_n"] = int(nombre(m.group(1))), int(nombre(m.group(2))), int(m.group(3))
    v = prem(r"Vitesse max\s*:?\s*(?:environ\s*)?(\d+)\s*km/h")
    if v:
        d["vitesse_max_kmh"] = int(v)
    v = prem(r"Performances\s.*?Consommation moyenne\s*:\s*([\d,\.]+)\s*l/100\s*km", re.S)
    if v:
        d["conso"] = nombre(v)
    v = prem(r"Réservoir\s*:\s*([\d,\.]+)\s*litres?")
    if v:
        d["reservoir_l"] = nombre(v)
    for cle, lib in (("hauteur_selle_mm", "Hauteur de selle"), ("empattement_mm", "Empattement"),
                     ("longueur_mm", "Longueur"), ("largeur_mm", "Largeur")):
        v = prem(r"%s\s*:\s*([\d ]+)\s*mm" % lib)
        if v and nombre(v):
            d[cle] = int(nombre(v))
    v = prem(r"Poids tous pleins faits\s*:\s*([\d ,\.]+)\s*kg")
    if v and nombre(v):
        d["poids_tous_pleins_kg"] = nombre(v)
    v = prem(r"Poids à sec\s*:\s*([\d ,\.]+)\s*kg")
    if v and nombre(v):
        d["poids_sec_kg"] = nombre(v)
    v = prem(r"Selle (biplaces?|monoplace)")
    if v:
        d["places"] = 2 if v.startswith("biplace") else 1
    v = prem(r"Cadre\s*:\s*([^\n]+)")
    if v:
        d["cadre"] = v
    # train avant / arriere : freinage et pneu
    def bloc(pattern, mot_cle):
        # la page repete chaque titre dans un menu : on garde le bloc qui contient le mot-cle
        for m in re.finditer(pattern, s, re.S):
            if mot_cle in m.group(1):
                return m.group(1)
        return None

    av = bloc(r"Train avant\n(.*?)(?:front--tech-map|Train arrière\n)", "Freinage")
    ar = bloc(r"Train arrière\n(.*?)(?:front--tech-map|\nMoteur\n)", "Freinage")
    fr, pn = [], []
    if av:
        m = re.search(r"Freinage\s*([^\n]+)", av)
        if m:
            fr.append("Avant : " + m.group(1).strip())
        m = re.search(r"Roue avant[^:]*:\s*([\d ]+/\s*[\d ]+)\s*-\s*(\d+)", av)
        if m:
            pn.append("Avant " + re.sub(r"\s+", "", m.group(1)) + "-" + m.group(2))
    if ar:
        m = re.search(r"Freinage\s*([^\n]+)", ar)
        if m:
            fr.append("Arrière : " + m.group(1).strip())
        m = re.search(r"Roue arrière[^:]*:\s*([\d ]+/\s*[\d ]+)\s*-\s*(\d+)", ar)
        if m:
            pn.append("Arrière " + re.sub(r"\s+", "", m.group(1)) + "-" + m.group(2))
    if fr:
        d["freins"] = " ; ".join(fr)
    if pn:
        d["pneus"] = " ; ".join(pn)
    tr = prem(r"Transmission\n((?:boîte[^\n]*\n[^\n]*\n)?[^\n]*(?:chaîne|cardan|courroie)[^\n]*)", re.S | re.I) \
        if False else None
    m = re.search(r"(boîte à \d+ rapports|boîte automatique|variateur[^\n]*)", s, re.I)
    sec = re.search(r"Secondaire par (chaîne|cardan|courroie)", s, re.I)
    if m:
        d["transmission"] = m.group(1).capitalize() + (", secondaire par " + sec.group(1).lower() if sec else "")
    # moteur
    mot = None
    fin = s.find("Équipement de série")
    if fin < 0:
        fin = s.find("Infos pratiques")
    if fin > 0:
        debut = s.rfind("\nMoteur\n", 0, fin)
        if debut >= 0:
            mot = s[debut + 8:fin]
    if mot:
        lignes = [x.strip() for x in mot.split("\n") if x.strip()]
        if lignes:
            d["architecture"] = re.sub(r"\s*,\s*$", "", lignes[0])
        m = re.search(r"Refroidissement\s*:\s*(\w+)", mot)
        if m:
            d["refroidissement"] = m.group(1)
        m = re.search(r"([\d ,\.]+)\s*cc", mot)
        if m and nombre(m.group(1)):
            d["cylindree_cc"] = nombre(m.group(1))
        m = re.search(r"([\d ,\.]+)\s*ch\s*à\s*([\d ]+)\s*tr/min", mot)
        if m:
            d["puissance_ch"] = nombre(m.group(1))
            d["puissance_tr_min"] = int(nombre(m.group(2)))
        m = re.search(r"\(([\d ,\.]+)\s*Nm\)\s*à\s*([\d ]+)\s*tr/min", mot)
        if m:
            d["couple_nm"] = nombre(m.group(1))
            d["couple_tr_min"] = int(nombre(m.group(2)))
    v = prem(r"accessible aux permis\s*:\s*([A-Z0-9, ]+)")
    if v:
        d["permis"] = re.sub(r"\s+", "", v)
    eq = prem(r"Équipement de série\n(.*?)(?:🛒|Infos pratiques)", re.S)
    if eq:
        d["equipement"] = [x.strip() for x in eq.split("\n") if x.strip()][:25]
    return d


def phase_fetch(match, limite=None):
    cache = {}
    if os.path.exists(F_FICHES):
        cache = json.load(open(F_FICHES, encoding="utf-8"))
    # modeles courants d'abord : ce sont eux qui servent aux outils
    ordre = sorted(match.items(), key=lambda kv: (not kv[1]["courant"], kv[1]["confiance"] != "exact"))
    n = 0
    for mid, m in ordre:
        if mid in cache and cache[mid].get("url") == m["url"]:
            continue
        if limite and n >= limite:
            break
        pause()
        try:
            r = S.get(m["url"], timeout=60)
        except Exception as ex:
            print("erreur reseau", m["url"], ex, flush=True)
            continue
        if r.status_code in (403, 429):
            print("ARRET : HTTP %d sur %s" % (r.status_code, m["url"]), flush=True)
            break
        if r.status_code != 200:
            print("ignoree HTTP %d : %s" % (r.status_code, m["url"]), flush=True)
            cache[mid] = {"url": m["url"], "erreur": r.status_code}
            continue
        d = parser(r.content.decode("utf-8", errors="ignore"))
        d.update({"url": m["url"], "an": m["an"], "confiance": m["confiance"], "nom": m["nom"],
                  "date": time.strftime("%Y-%m-%d")})
        cache[mid] = d
        n += 1
        print("[%d] %s -> %d champs" % (n, m["nom"], len(d) - 5), flush=True)
        if n % 10 == 0:
            json.dump(cache, open(F_FICHES, "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(cache, open(F_FICHES, "w", encoding="utf-8"), ensure_ascii=False)
    return cache


if __name__ == "__main__":
    phase = sys.argv[1] if len(sys.argv) > 1 else "tout"
    limite = int(sys.argv[2]) if len(sys.argv) > 2 else None
    index = phase_index()
    print("%d fiches dans l'index" % len(index["urls"]), flush=True)
    match = phase_match(index)
    n_exact = sum(1 for m in match.values() if m["confiance"] == "exact")
    print("%d modeles rattaches (%d exacts, %d approchants, %d courants)"
          % (len(match), n_exact, len(match) - n_exact, sum(1 for m in match.values() if m["courant"])), flush=True)
    json.dump(match, open(os.path.join(RAW, "motoplanete_match.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if phase in ("fetch", "tout"):
        phase_fetch(match, limite)
