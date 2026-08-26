# -*- coding: utf-8 -*-
"""
Etape 10 : corrections de l'enrichissement.
  a) PRIX : validation stricte de la devise. Le champ 'Prix a sa sortie' de
     Wikipedia FR melange euros, francs, Reichsmark, DM, dollars. On ne garde
     que ce qui est certainement en euros. Le reste est rejete, pas devine.
  b) IMAGES : le parametre iiurlwidth faisait plafonner l'API Commons.
  c) LIENS FR : rattrapage des lots perdus.
Sortie : data/raw/enrichissement.json (mis a jour)
"""
import requests, json, time, os, re

EN = "https://en.wikipedia.org/w/api.php"
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

def clean(s):
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip()

enr = json.load(open(os.path.join(RAW, "enrichissement.json"), encoding="utf-8"))
rows = json.load(open(os.path.join(RAW, "normalise_qa.json"), encoding="utf-8"))
annee = {r["titre_wikipedia"]: r.get("annee_debut") for r in rows}

# ================================================== a) PRIX
print("=" * 70)
print("a) VALIDATION STRICTE DES PRIX")
print("=" * 70)

AUTRES_DEVISES = re.compile(
    r"franc|\bfr\b|\bff\b|reichsmark|\bdm\b|deutsche|mark|dollar|\$|£|livre|"
    r"yen|¥|lire|lira|peseta|florin|couronne", re.I)
EURO = re.compile(r"€|euro", re.I)

garde, rejet = 0, 0
motifs = {}
for t, v in enr.items():
    if not v.get("prix_lancement_eur"):
        continue
    brut = v.get("prix_lancement_brut", "")
    val = v["prix_lancement_eur"]
    a = annee.get(t)
    motif = None

    if AUTRES_DEVISES.search(brut):
        motif = "devise etrangere citee"
    elif not EURO.search(brut) and (a is None or a < 2002):
        motif = "anterieur a l'euro (< 2002), devise non precisee"
    elif re.search(r"\b(18|19|20)\d{2}\b", brut) and str(val) in brut and 1800 < val < 2030:
        motif = "la valeur ressemble a une annee"
    elif not (800 <= val <= 60000):
        motif = "hors fourchette plausible pour une moto neuve"

    if motif:
        for k in ("prix_lancement_eur", "prix_lancement_brut", "prix_source"):
            v.pop(k, None)
        v["prix_rejete"] = "%s | source : %s" % (motif, brut[:60])
        motifs[motif] = motifs.get(motif, 0) + 1
        rejet += 1
    else:
        v["prix_source"] = "Wikipedia FR - prix au lancement (%s)" % (a or "annee inconnue")
        garde += 1

for m, n in sorted(motifs.items(), key=lambda x: -x[1]):
    print("   rejete : %-46s %3d" % (m, n))
print("\n   -> %d prix conserves, %d rejetes" % (garde, rejet))

# ================================================== b) IMAGES
print("\n" + "=" * 70)
print("b) LICENCES D'IMAGES (sans iiurlwidth)")
print("=" * 70)

titres = sorted(enr.keys())
fichiers = {}
for i in range(0, len(titres), 40):
    chunk = titres[i:i+40]
    j = get(EN, {"action": "query", "prop": "pageimages", "piprop": "name",
                 "pilimit": "50", "titles": "|".join(chunk),
                 "format": "json", "formatversion": "2"})
    if not j:
        continue
    for p in j.get("query", {}).get("pages", []):
        if p.get("pageimage"):
            fichiers.setdefault("File:" + p["pageimage"], []).append(p["title"])
    time.sleep(0.1)
print("   %d fichiers image distincts" % len(fichiers))

fl = list(fichiers.keys())
n_lic = 0
manquants = []
for i in range(0, len(fl), 40):
    chunk = fl[i:i+40]
    j = get(COM, {"action": "query", "prop": "imageinfo",
                  "iiprop": "extmetadata|url",
                  "titles": "|".join(chunk), "format": "json", "formatversion": "2"})
    if not j:
        manquants += chunk
        continue
    vus = set()
    for p in j.get("query", {}).get("pages", []):
        vus.add(p["title"])
        ii = (p.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata", {}) or {}
        def g(k):
            return clean(str((em.get(k, {}) or {}).get("value", "")))
        lic = g("LicenseShortName")
        if not lic:
            manquants.append(p["title"])
            continue
        for t in fichiers.get(p["title"], []):
            enr[t]["image_fichier"] = p["title"]
            enr[t]["image_licence"] = lic
            enr[t]["image_auteur"] = g("Artist")[:120]
            enr[t]["image_credit"] = g("Credit")[:100]
            enr[t]["image_page"] = ii.get("descriptionurl", "")
            n_lic += 1
    manquants += [c for c in chunk if c not in vus]
    if (i // 40) % 8 == 0:
        print("   %d/%d" % (i + len(chunk), len(fl)))
    time.sleep(0.12)

# les fichiers locaux a en.wikipedia (non Commons)
if manquants:
    print("   %d fichiers absents de Commons -> recherche sur Wikipedia EN" % len(manquants))
    for i in range(0, len(manquants), 40):
        chunk = manquants[i:i+40]
        j = get(EN, {"action": "query", "prop": "imageinfo",
                     "iiprop": "extmetadata|url",
                     "titles": "|".join(chunk), "format": "json", "formatversion": "2"})
        if not j:
            continue
        for p in j.get("query", {}).get("pages", []):
            ii = (p.get("imageinfo") or [{}])[0]
            em = ii.get("extmetadata", {}) or {}
            lic = clean(str((em.get("LicenseShortName", {}) or {}).get("value", "")))
            if not lic:
                continue
            for t in fichiers.get(p["title"], []):
                enr[t]["image_fichier"] = p["title"]
                enr[t]["image_licence"] = lic
                enr[t]["image_auteur"] = clean(
                    str((em.get("Artist", {}) or {}).get("value", "")))[:120]
                enr[t]["image_page"] = ii.get("descriptionurl", "")
                n_lic += 1
        time.sleep(0.12)

print("   -> %d images documentees" % n_lic)

# ================================================== c) LIENS FR
print("\n" + "=" * 70)
print("c) RATTRAPAGE DES LIENS WIKIPEDIA FR")
print("=" * 70)
sans = [t for t in titres if not enr[t].get("titre_fr")]
print("   %d articles sans lien FR connu" % len(sans))
trouve = 0
for i in range(0, len(sans), 40):
    chunk = sans[i:i+40]
    j = get(EN, {"action": "query", "prop": "langlinks", "lllang": "fr",
                 "lllimit": "max", "titles": "|".join(chunk),
                 "format": "json", "formatversion": "2"})
    if not j:
        continue
    for p in j.get("query", {}).get("pages", []):
        ll = p.get("langlinks", [])
        if ll:
            enr[p["title"]]["titre_fr"] = ll[0]["title"]
            trouve += 1
    time.sleep(0.1)
print("   -> +%d liens FR trouves" % trouve)

json.dump(enr, open(os.path.join(RAW, "enrichissement.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# ================================================== bilan
print("\n" + "=" * 70)
print("BILAN APRES CORRECTION")
print("=" * 70)
N = len(enr)
for champ, lib in [("titre_fr", "article FR"), ("nom_fr", "nom commercial FR"),
                   ("type_fr", "type FR"), ("prix_lancement_eur", "prix (euros verifies)"),
                   ("resume_fr", "resume FR"), ("image_licence", "licence image")]:
    n = sum(1 for v in enr.values() if v.get(champ))
    print("  %-24s %5d / %d  (%d%%)" % (lib, n, N, 100 * n // N))

p = [(v["prix_lancement_eur"], t, v.get("prix_source", ""))
     for t, v in enr.items() if v.get("prix_lancement_eur")]
p.sort()
if p:
    print("\nPRIX CONSERVES (%d) :" % len(p))
    for prix, t, src in p:
        print("   %7d EUR   %-34s %s" % (prix, t[:34], src[-18:]))
