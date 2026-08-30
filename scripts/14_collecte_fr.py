# -*- coding: utf-8 -*-
"""
Etape 14 : collecte des modeles presents sur Wikipedia FR uniquement.

La collecte initiale partait de Wikipedia EN. Or la version francaise couvre
mieux le marche europeen : la Yamaha Tracer 9 y figure alors qu'elle est absente
de la version anglaise. 358 modeles supplementaires sont ainsi recuperables.

Produit des fiches au MEME schema que normalise_qa.json, fusionnees a l'export.
Sortie : data/raw/modeles_fr.json
"""
import requests, json, re, os, time, unicodedata, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
_n = import_module("03_normalise")
MARQUES, slug, ARCHS = _n.MARQUES, _n.slug, _n.ARCHS

API = "https://fr.wikipedia.org/w/api.php"
COM = "https://commons.wikimedia.org/w/api.php"
S = requests.Session()
S.headers.update({"User-Agent": "MotoDirectoryResearch/0.1 (viktordu84@gmail.com)"})
RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def get(url, params, tries=5):
    d = 0.4
    for _ in range(tries):
        try:
            r = S.get(url, params=params, timeout=60)
            if r.status_code == 200 and r.text.lstrip().startswith("{"):
                return r.json()
        except Exception:
            pass
        time.sleep(d); d *= 2
    return None


def membres(cat, typ="page"):
    out, cont = [], {}
    for _ in range(30):
        p = {"action": "query", "list": "categorymembers", "cmtitle": cat,
             "cmlimit": 500, "cmtype": typ, "format": "json", "formatversion": "2"}
        p.update(cont)
        j = get(API, p)
        if not j:
            break
        out += j.get("query", {}).get("categorymembers", [])
        if "continue" in j:
            cont = j["continue"]
        else:
            break
        time.sleep(0.08)
    return [m["title"] for m in out]


def find_ib(wt):
    m = re.search(r"\{\{\s*Infobox", wt, re.I)
    if not m:
        return None
    i, d, j = m.start(), 0, m.start()
    while j < len(wt) - 1:
        if wt[j:j+2] == "{{":
            d += 1; j += 2; continue
        if wt[j:j+2] == "}}":
            d -= 1; j += 2
            if d == 0:
                return wt[i:j]
            continue
        j += 1
    return None


def params_ib(box):
    body = box[2:-2]
    parts, buf, dt, dl, k = [], [], 0, 0, 0
    while k < len(body):
        c2 = body[k:k+2]
        if c2 == "{{": dt += 1; buf.append(c2); k += 2; continue
        if c2 == "}}": dt -= 1; buf.append(c2); k += 2; continue
        if c2 == "[[": dl += 1; buf.append(c2); k += 2; continue
        if c2 == "]]": dl -= 1; buf.append(c2); k += 2; continue
        ch = body[k]
        if ch == "|" and dt == 0 and dl == 0:
            parts.append("".join(buf)); buf = []; k += 1; continue
        buf.append(ch); k += 1
    parts.append("".join(buf))
    out = {}
    for p in parts[1:]:
        if "=" not in p:
            continue
        a, b = p.split("=", 1)
        a, b = a.strip(), b.strip()
        if a and b:
            out[a] = b
    typ = re.match(r"\{\{\s*Infobox\s*([^\n|]*)", box, re.I)
    return (typ.group(1).strip() if typ else ""), out


def texte(v):
    if not v:
        return ""
    v = re.sub(r"<ref[^>]*>.*?</ref>|<ref[^>]*/>", "", v, flags=re.S | re.I)
    v = re.sub(r"\{\{\s*unité\s*\|([^{}|]*)\|?([^{}|]*)\|?([^{}]*)\}\}",
               lambda m: (m.group(1) + " " + m.group(2)).strip(), v, flags=re.I)
    v = re.sub(r"\{\{\s*(?:nb|formatnum|nombre)\s*\|([^{}|]*)[^{}]*\}\}", r"\1", v, flags=re.I)
    v = re.sub(r"<\s*br\s*/?\s*>", " / ", v, flags=re.I)
    v = re.sub(r"\{\{[^{}]*\}\}", "", v)
    v = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]|]*)\]\]", r"\1", v)
    v = re.sub(r"<[^>]+>", "", v)
    v = v.replace("&nbsp;", " ").replace("&amp;", "&")
    v = re.sub(r"'{2,}", "", v)
    v = re.sub(r"\s+", " ", v)
    return re.sub(r"(?:\s*/\s*){2,}", " / ", v).strip(" ,;:/")


def nombre(v):
    t = texte(v).replace(",", ".").replace(" ", "").replace("\xa0", "").replace(" ", "")
    m = re.search(r"-?\d+(?:\.\d+)?", t)
    return float(m.group(0)) if m else None


BORNES = {
 "cylindree_cc": (30, 2500), "puissance_ch": (1, 320),
 "puissance_tr_min": (1000, 20000), "couple_tr_min": (800, 18000),
 "poids_sec_kg": (30, 500), "poids_tous_pleins_kg": (30, 550),
 "hauteur_selle_mm": (500, 1000), "empattement_mm": (900, 1900),
 "reservoir_l": (2, 40), "vitesse_max_kmh": (25, 400),
}
CHAMPS = {
 "Cylindrée": "cylindree_cc", "Puissance": "puissance_ch",
 "Régime Puissance": "puissance_tr_min", "Régime Couple": "couple_tr_min",
 "Poids à sec": "poids_sec_kg", "Poids tous pleins faits": "poids_tous_pleins_kg",
 "Hauteur de selle": "hauteur_selle_mm", "Empattement": "empattement_mm",
 "Réservoir": "reservoir_l", "Vitesse maximale": "vitesse_max_kmh",
}
CAT_FR = [
 (r"sportive|superbike|supersport", "Sportive"),
 (r"caf[eé] ?racer", "Café racer"),
 (r"supermotard", "Supermotard"),
 (r"roadster|routi[eè]re sportive|naked", "Roadster"),
 (r"trail|aventure|enduro|tout.?chemin", "Trail / Aventure"),
 (r"custom|cruiser|chopper", "Custom / Cruiser"),
 (r"routi[eè]re|grand tourisme|\bgt\b", "Routière / GT"),
 (r"scooter|cyclomoteur|mobylette", "Scooter / Cyclomoteur"),
 (r"motocross|tout.?terrain|trial", "Tout-terrain"),
 (r"[ée]lectrique", "Électrique"),
 (r"comp[ée]tition|grand prix|course", "Compétition"),
]

# --- 1. enumeration -------------------------------------------------------
print("1. Enumeration des categories FR...")
titres = set()
for sc in membres("Catégorie:Motocyclette par constructeur", "subcat"):
    pages = membres(sc, "page")
    for ss in membres(sc, "subcat"):
        pages += membres(ss, "page")
    titres.update(pages)
print("   %d articles" % len(titres))

EXCLURE = ("Liste", "Catégorie:", "Portail:", "Modèle:", "Histoire de")
titres = {t for t in titres if not t.startswith(EXCLURE)}
# on ecarte les articles de marque (titre = nom de marque seul)
marques_nues = {m.lower() for m in MARQUES} | {
    "aprilia", "bmw", "honda", "yamaha", "suzuki", "kawasaki", "ducati",
    "triumph", "ktm", "peugeot", "bimota", "voxan", "vyrus", "motobécane"}
titres = {t for t in titres if t.lower() not in marques_nues}
print("   %d apres filtrage" % len(titres))

# --- 2. recuperation ------------------------------------------------------
print("\n2. Recuperation des infobox...")
noms = sorted(titres)
rows, sans_ib = [], 0
for i in range(0, len(noms), 20):
    lot = noms[i:i+20]
    j = get(API, {"action": "query", "prop": "revisions|pageimages|pageprops",
                  "rvprop": "content", "rvslots": "main", "piprop": "name|original",
                  "pilimit": "50", "titles": "|".join(lot),
                  "format": "json", "formatversion": "2", "redirects": "1"})
    if not j:
        continue
    for p in j.get("query", {}).get("pages", []):
        if p.get("missing"):
            continue
        try:
            wt = p["revisions"][0]["slots"]["main"]["content"]
        except Exception:
            continue
        box = find_ib(wt)
        if not box:
            sans_ib += 1
            continue
        typ, ch = params_ib(box)
        if "moto" not in typ.lower():
            sans_ib += 1
            continue

        titre = p["title"]
        marque = ""
        cons = texte(ch.get("Constructeur", ""))
        for k in MARQUES:
            if k.lower() in cons.lower() or titre.lower().startswith(k.lower()):
                marque = k
                break
        if not marque:
            for k in MARQUES:
                if k.split()[0].lower() == titre.split()[0].lower():
                    marque = k
                    break
        pays, ecole = MARQUES.get(marque, ("", ""))

        r = {"modele_id": slug(titre), "titre_wikipedia": titre,
             "marque": marque, "marque_id": slug(marque) if marque else "",
             "modele": texte(ch.get("Nom", "")) or titre,
             "pays_origine": pays, "ecole": ecole,
             "source": "Wikipédia FR (CC BY-SA 4.0)",
             "url_wikipedia": "https://fr.wikipedia.org/wiki/" + titre.replace(" ", "_"),
             "collecte_fr": True}

        for k_fr, k_int in CHAMPS.items():
            if k_fr in ch:
                v = nombre(ch[k_fr])
                lo, hi = BORNES[k_int]
                if v is not None and lo <= v <= hi:
                    r[k_int] = round(v, 2)
        # couple : unite ambigue en francais, on n'importe que si elle est explicite
        if "Couple" in ch:
            brut = texte(ch["Couple"])
            v = nombre(brut)
            if v is not None:
                if re.search(r"N\s*[.·]?\s*m", brut, re.I) and 2 <= v <= 250:
                    r["couple_nm"] = round(v, 1)
                elif re.search(r"m\s*[.·]?\s*kg|kg\s*[.·]?\s*m", brut, re.I):
                    n = v * 9.80665
                    if 2 <= n <= 250:
                        r["couple_nm"] = round(n, 1)

        prod = texte(ch.get("Années de production", ""))
        ys = [int(y) for y in re.findall(r"\b(1[89]\d{2}|20[0-2]\d)\b", prod)]
        if ys:
            r["annee_debut"] = min(ys)
            r["annee_fin"] = (None if re.search(
                r"aujourd|présent|en cours|depuis|since|[–—-]\s*$", prod, re.I)
                              else max(ys))
        r["production_raw"] = prod

        moteur = texte(ch.get("Moteurs", ""))
        r["moteur"] = moteur[:300]
        low = (moteur + " " + titre).lower()
        r["architecture"] = next((a for p_, a in ARCHS if re.search(p_, low)), "")
        if re.search(r"liquide|refroidi par eau", low):
            r["refroidissement"] = "Liquide"
        elif re.search(r"\bair\b", low):
            r["refroidissement"] = "Air"
        else:
            r["refroidissement"] = ""

        src_cat = (texte(ch.get("Type", "")) + " " + titre + " " + moteur).lower()
        r["categorie"] = next((lab for pat, lab in CAT_FR if re.search(pat, src_cat)), "")

        for k_fr, k_int in (("Cadre", "cadre"), ("Transmission", "transmission")):
            if k_fr in ch:
                r[k_int] = texte(ch[k_fr])[:220]
        susp = " / ".join(x for x in (texte(ch.get("Suspension avant", "")),
                                      texte(ch.get("Suspension arrière", ""))) if x)
        frein = " / ".join(x for x in (texte(ch.get("Frein avant", "")),
                                       texte(ch.get("Frein arrière", ""))) if x)
        pneus = " / ".join(x for x in (texte(ch.get("Roue avant", "")),
                                       texte(ch.get("Roue arrière", ""))) if x)
        if susp: r["suspension"] = susp[:250]
        if frein: r["freins"] = frein[:200]
        if pneus: r["pneus"] = pneus[:200]

        if "Prix à sa sortie" in ch:
            v = nombre(ch["Prix à sa sortie"])
            brut = texte(ch["Prix à sa sortie"])
            an = r.get("annee_debut") or 0
            devise_autre = re.search(r"franc|\bfr\b|mark|dollar|\$|£|yen|lire", brut, re.I)
            if v and 800 <= v <= 60000 and not devise_autre and (
                    an >= 2002 or re.search(r"€|euro", brut, re.I)):
                r["prix_lancement_eur"] = int(v)
                r["prix_source"] = "Wikipédia FR - prix au lancement (%s)" % (an or "?")

        if p.get("original"):
            r["image_url"] = p["original"].get("source", "").split("?")[0]
        if p.get("pageimage"):
            r["image_fichier"] = "File:" + p["pageimage"]
        r["wikidata_id"] = p.get("pageprops", {}).get("wikibase_item", "")
        rows.append(r)
    if (i // 20) % 5 == 0:
        print("   %d/%d  (%d fiches)" % (i + len(lot), len(noms), len(rows)))
    time.sleep(0.12)

print("   %d articles sans infobox moto ecartes" % sans_ib)

# --- 3. poids retenu, A2, completude -------------------------------------
for r in rows:
    r["poids_kg"] = r.get("poids_tous_pleins_kg") or r.get("poids_sec_kg")
    r["poids_type"] = ("tous pleins faits" if r.get("poids_tous_pleins_kg")
                       else ("à sec" if r.get("poids_sec_kg") else ""))
    if r.get("puissance_ch"):
        r["puissance_kw"] = round(r["puissance_ch"] * 0.735499, 2)
    pw, poids = r.get("puissance_kw"), r.get("poids_kg")
    if not pw:
        r["a2_compatible"], r["a2_detail"] = "", ""
    elif pw > 35:
        r["a2_compatible"], r["a2_detail"] = "non", "puissance > 35 kW"
    elif poids:
        ratio = pw / poids
        r["a2_compatible"] = "oui" if ratio <= 0.2 else "non"
        r["a2_detail"] = ("%.1f kW, %.3f kW/kg" % (pw, ratio) if ratio <= 0.2
                          else "rapport %.3f kW/kg > 0.2" % ratio)
    else:
        r["a2_compatible"], r["a2_detail"] = "à vérifier", "poids inconnu"
    KEY = ["cylindree_cc", "puissance_kw", "couple_nm", "poids_kg", "hauteur_selle_mm",
           "empattement_mm", "reservoir_l", "vitesse_max_kmh", "categorie",
           "annee_debut", "architecture", "transmission", "freins", "pneus", "image_url"]
    r["completude_pct"] = round(100 * sum(1 for k in KEY if r.get(k)) / len(KEY))
    r["alertes"] = ""

json.dump(rows, open(os.path.join(RAW, "modeles_fr.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("\n=== %d modeles collectes depuis Wikipedia FR ===" % len(rows))
print("   completude moyenne : %.0f%%" % (sum(r["completude_pct"] for r in rows) / max(1, len(rows))))
for s in (80, 60, 45):
    print("   >= %d%% : %d" % (s, sum(1 for r in rows if r["completude_pct"] >= s)))
from collections import Counter
print("\nMARQUES :")
for k, v in Counter(r["marque"] for r in rows if r["marque"]).most_common(12):
    print("   %4d  %s" % (v, k))
print("\nAvec prix : %d" % sum(1 for r in rows if r.get("prix_lancement_eur")))
