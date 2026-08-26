# -*- coding: utf-8 -*-
"""
Etape 1 : enumeration des articles moto sur Wikipedia EN.
Sources d'enumeration :
  - Category:Motorcycles by brand  (-> marque)
  - Category:Motorcycles of <Pays> (-> pays d'origine)
  - Category:Motorcycles introduced in YYYY (-> couverture complementaire)
Sortie : data/raw/titres.json
"""
import requests, json, time, os, sys
from collections import defaultdict

API = "https://en.wikipedia.org/w/api.php"
S = requests.Session()
S.headers.update({"User-Agent": "MotoDirectoryResearch/0.1 (viktordu84@gmail.com)"})
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

def members(cat, typ="page"):
    out, cont = [], {}
    for _ in range(40):
        p = {"action":"query","list":"categorymembers","cmtitle":cat,"cmlimit":500,
             "cmtype":typ,"format":"json","formatversion":"2"}
        p.update(cont)
        try:
            j = S.get(API, params=p, timeout=40).json()
        except Exception as e:
            print(f"  ! {cat}: {e}", file=sys.stderr); break
        out += j.get("query", {}).get("categorymembers", [])
        if "continue" in j: cont = j["continue"]
        else: break
    return [m["title"] for m in out]

EXCLUDE = ("List of","Lists of","Category:","Template:","Timeline of","Comparison of",
           "History of","Index of","Outline of")
def keep(t):
    return not t.startswith(EXCLUDE) and ":" not in t.split("(")[0][:20]

titles = {}            # titre -> {marques:set, pays:set, annees:set}
def add(t, key, val):
    if not keep(t): return
    e = titles.setdefault(t, {"marques": set(), "pays": set(), "annees": set()})
    e[key].add(val)

# --- A. par marque -------------------------------------------------------
print("A. Categories par marque...")
brand_cats = members("Category:Motorcycles by brand", "subcat")
brand_cats = [c for c in brand_cats if "designers" not in c.lower() and "Lists of" not in c]
print(f"   {len(brand_cats)} marques")
for i, c in enumerate(brand_cats, 1):
    brand = c.replace("Category:", "").replace(" motorcycles", "").strip()
    pages = members(c, "page")
    for sc in members(c, "subcat"):
        pages += members(sc, "page")
    for p in pages: add(p, "marques", brand)
    if i % 15 == 0: print(f"   ... {i}/{len(brand_cats)}  ({len(titles)} titres)")

# --- B. par pays ---------------------------------------------------------
print("B. Categories par pays...")
PAYS = ["Japan","Italy","the United States","Germany","the United Kingdom","Austria",
        "Spain","India","China","France","Sweden","the Czech Republic","Taiwan",
        "South Korea","Russia","Poland","Brazil","Switzerland","the Netherlands"]
for p_ in PAYS:
    pages = members(f"Category:Motorcycles of {p_}", "page")
    for sc in members(f"Category:Motorcycles of {p_}", "subcat"):
        pages += members(sc, "page")
    if pages:
        lab = p_.replace("the ", "")
        for t in pages: add(t, "pays", lab)
        print(f"   {lab:<20} {len(pages)}")

# --- C. par annee --------------------------------------------------------
print("C. Categories par annee d'introduction...")
n0 = len(titles)
for y in range(1885, 2027):
    for t in members(f"Category:Motorcycles introduced in {y}", "page"):
        add(t, "annees", y)
print(f"   +{len(titles)-n0} titres nouveaux")

os.makedirs(OUT, exist_ok=True)
ser = {t: {k: sorted(v) for k, v in d.items()} for t, d in titles.items()}
with open(os.path.join(OUT, "titres.json"), "w", encoding="utf-8") as f:
    json.dump(ser, f, ensure_ascii=False, indent=1)

print(f"\n=== TOTAL : {len(titles)} articles uniques ===")
print(f"   avec marque identifiee : {sum(1 for d in titles.values() if d['marques'])}")
print(f"   avec pays identifie    : {sum(1 for d in titles.values() if d['pays'])}")
