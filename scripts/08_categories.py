# -*- coding: utf-8 -*-
"""
Etape 8 : categories Wikipedia de chaque article.
Signal de typologie bien plus fiable que le champ 'class' de l'infobox,
absent sur 359 modeles.
Sortie : data/raw/categories_articles.json
"""
import requests, json, time, os

API = "https://en.wikipedia.org/w/api.php"
S = requests.Session()
S.headers.update({"User-Agent": "MotoDirectoryResearch/0.1 (viktordu84@gmail.com)"})
RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

def get(params, tries=5):
    d = 0.4
    for _ in range(tries):
        try:
            r = S.get(API, params=params, timeout=60)
            if r.status_code == 200 and r.text.lstrip().startswith("{"):
                return r.json()
        except Exception:
            pass
        time.sleep(d); d *= 2
    return None

rows = json.load(open(os.path.join(RAW, "normalise_qa.json"), encoding="utf-8"))
titres = sorted({r["titre_wikipedia"] for r in rows})
print("%d articles" % len(titres))

IGNORE = ("Articles ", "CS1 ", "Commons category", "Short description",
          "Webarchive", "Official website", "All articles", "Wikipedia ",
          "Use dmy", "Use mdy", "Pages ", "Automatic category", "Category main",
          "Harv and Sfn", "Interlanguage", "Vague or ambiguous")

out = {}
B = 40
for i in range(0, len(titres), B):
    chunk = titres[i:i+B]
    j = get({"action": "query", "prop": "categories", "cllimit": "max",
             "titles": "|".join(chunk), "format": "json", "formatversion": "2"})
    if not j:
        continue
    for pg in j.get("query", {}).get("pages", []):
        if pg.get("missing"):
            continue
        cats = []
        for c in pg.get("categories", []):
            nom = c["title"].replace("Category:", "")
            if nom.startswith(IGNORE):
                continue
            cats.append(nom)
        out[pg["title"]] = cats
    if (i // B) % 10 == 0:
        print("   %d/%d" % (i + len(chunk), len(titres)))
    time.sleep(0.12)

json.dump(out, open(os.path.join(RAW, "categories_articles.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

from collections import Counter
c = Counter(x for v in out.values() for x in v)
print("\n=== %d articles, %d categories distinctes ===" % (len(out), len(c)))
print("\nCATEGORIES DE TYPOLOGIE LES PLUS FREQUENTES :")
MOTS = ("motorcycle", "bike", "scooter", "moped", "cruiser", "tour", "sport",
        "standard", "off-road", "racing", "custom", "enduro", "trial")
for k, v in c.most_common(400):
    kl = k.lower()
    if any(m in kl for m in MOTS) and not kl.startswith(("motorcycles introduced",
                                                          "motorcycles of")):
        print("  %5d  %s" % (v, k))
