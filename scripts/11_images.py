# -*- coding: utf-8 -*-
"""
Etape 11 : licences d'images (correctif).
Bug corrige : l'API normalise 'File:Nom_Avec_Underscores.jpg' en
'File:Nom Avec Underscores.jpg'. Les cles du dictionnaire ne correspondaient pas.
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
    s = re.sub(r"<[^>]+>", "", str(s))
    return re.sub(r"\s+", " ", s).strip()

def norm(f):
    """Cle canonique : espaces, pas d'underscores (comme l'API les renvoie)."""
    return f.replace("_", " ").strip()

enr = json.load(open(os.path.join(RAW, "enrichissement.json"), encoding="utf-8"))
titres = sorted(enr.keys())

# 1) fichier image de chaque article
print("1. Fichiers image des %d articles..." % len(titres))
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
            fichiers.setdefault(norm("File:" + p["pageimage"]), []).append(p["title"])
    time.sleep(0.1)
print("   %d fichiers distincts" % len(fichiers))

# 2) licences, Commons puis Wikipedia EN pour les fichiers locaux
def poser(titre_fichier, em, url_desc, normalized):
    """Applique la licence aux articles concernes, en resolvant la normalisation."""
    cles = {norm(titre_fichier)}
    if titre_fichier in normalized:
        cles.add(norm(normalized[titre_fichier]))
    lic = clean((em.get("LicenseShortName", {}) or {}).get("value", ""))
    if not lic:
        return 0
    n = 0
    for c in cles:
        for t in fichiers.get(c, []):
            enr[t]["image_fichier"] = titre_fichier
            enr[t]["image_licence"] = lic
            enr[t]["image_auteur"] = clean((em.get("Artist", {}) or {}).get("value", ""))[:120]
            enr[t]["image_credit"] = clean((em.get("Credit", {}) or {}).get("value", ""))[:100]
            enr[t]["image_page"] = url_desc
            n += 1
    return n

fl = sorted(fichiers.keys())
restants = []
n_lic = 0
for source, url in (("Commons", COM), ("Wikipedia EN", EN)):
    cibles = fl if source == "Commons" else restants
    if not cibles:
        continue
    print("\n2. Licences depuis %s (%d fichiers)..." % (source, len(cibles)))
    nouveaux = []
    for i in range(0, len(cibles), 40):
        chunk = cibles[i:i+40]
        j = get(url, {"action": "query", "prop": "imageinfo",
                      "iiprop": "extmetadata|url",
                      "titles": "|".join(chunk), "format": "json",
                      "formatversion": "2"})
        if not j:
            nouveaux += chunk
            continue
        q = j.get("query", {})
        normalized = {x["to"]: x["from"] for x in q.get("normalized", [])}
        for p in q.get("pages", []):
            if p.get("missing"):
                nouveaux.append(p["title"])
                continue
            ii = (p.get("imageinfo") or [{}])[0]
            em = ii.get("extmetadata", {}) or {}
            got = poser(p["title"], em, ii.get("descriptionurl", ""), normalized)
            if got:
                n_lic += got
            else:
                nouveaux.append(p["title"])
        if (i // 40) % 10 == 0:
            print("   %d/%d" % (i + len(chunk), len(cibles)))
        time.sleep(0.12)
    restants = nouveaux
    print("   -> %d articles documentes cumules, %d fichiers restants"
          % (n_lic, len(restants)))

json.dump(enr, open(os.path.join(RAW, "enrichissement.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

from collections import Counter
n = sum(1 for v in enr.values() if v.get("image_licence"))
print("\n=== %d / %d articles avec licence d'image (%d%%) ==="
      % (n, len(enr), 100 * n // len(enr)))
print("\nREPARTITION DES LICENCES :")
for k, v in Counter(v.get("image_licence") for v in enr.values()
                    if v.get("image_licence")).most_common(12):
    print("   %5d  %s" % (v, k))

# alerte : licences necessitant une vigilance
SENSIBLE = ("fair use", "non-free", "all rights", "copyright")
alerte = [t for t, v in enr.items()
          if v.get("image_licence") and
          any(s in v["image_licence"].lower() for s in SENSIBLE)]
print("\n%d images sous licence restrictive (a NE PAS republier)" % len(alerte))
for t in alerte[:10]:
    print("   %-40s %s" % (t[:40], enr[t]["image_licence"]))
