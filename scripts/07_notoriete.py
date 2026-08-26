# -*- coding: utf-8 -*-
"""
Etape 7 : signal de notoriete.
Pour chaque article : vues Wikipedia (60 derniers jours) + versions linguistiques.
L'existence d'une version FR/DE/IT/ES est le meilleur proxy disponible de la
pertinence pour le marche europeen.
Sortie : data/raw/notoriete.json
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
print("%d articles a sonder" % len(titres))

EURO = {"fr", "de", "it", "es", "nl", "pt", "pl", "sv"}
out = {}
B = 20   # langlinks + pageviews : lots plus petits
for i in range(0, len(titres), B):
    chunk = titres[i:i+B]
    j = get({"action": "query", "prop": "langlinks|pageviews",
             "lllimit": "max", "pvipdays": "60",
             "titles": "|".join(chunk), "format": "json", "formatversion": "2"})
    if not j:
        continue
    for pg in j.get("query", {}).get("pages", []):
        if pg.get("missing"):
            continue
        langs = {ll["lang"] for ll in pg.get("langlinks", [])}
        pv = pg.get("pageviews") or {}
        vues = [v for v in pv.values() if isinstance(v, int)]
        out[pg["title"]] = {
            "vues_60j": sum(vues),
            "vues_jour": round(sum(vues) / max(1, len(vues)), 1),
            "nb_langues": len(langs),
            "a_version_fr": "oui" if "fr" in langs else "non",
            "nb_langues_euro": len(langs & EURO),
        }
    if (i // B) % 15 == 0:
        print("   %d/%d" % (i + len(chunk), len(titres)))
    time.sleep(0.12)

json.dump(out, open(os.path.join(RAW, "notoriete.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("\n=== %d articles sondes ===" % len(out))
avec_fr = sum(1 for v in out.values() if v["a_version_fr"] == "oui")
print("  avec version francaise : %d (%d%%)" % (avec_fr, 100 * avec_fr // max(1, len(out))))
tot = sorted(out.items(), key=lambda x: -x[1]["vues_60j"])
print("\nTOP 20 ARTICLES LES PLUS CONSULTES (60 j) :")
for t, v in tot[:20]:
    print("  %7d vues  %2d langues  fr=%-3s  %s"
          % (v["vues_60j"], v["nb_langues"], v["a_version_fr"], t))
print("\nMEDIANE vues 60j : %d" % tot[len(tot)//2][1]["vues_60j"])
