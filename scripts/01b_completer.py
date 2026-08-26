# -*- coding: utf-8 -*-
"""Etape 1b : rattrapage des categories manquees (rate-limit) avec backoff."""
import requests, json, time, os, sys

API="https://en.wikipedia.org/w/api.php"
S=requests.Session(); S.headers.update({"User-Agent":"MotoDirectoryResearch/0.1 (viktordu84@gmail.com)"})
RAW=os.path.join(os.path.dirname(__file__),"..","data","raw")
P=os.path.join(RAW,"titres.json")

def get(params, tries=6):
    d=0.4
    for a in range(tries):
        try:
            r=S.get(API,params=params,timeout=45)
            if r.status_code==200 and r.text.lstrip().startswith("{"):
                return r.json()
        except Exception: pass
        time.sleep(d); d*=2
    return None

def members(cat, typ="page"):
    out,cont=[],{}
    for _ in range(40):
        p={"action":"query","list":"categorymembers","cmtitle":cat,"cmlimit":500,
           "cmtype":typ,"format":"json","formatversion":"2"}; p.update(cont)
        j=get(p)
        if j is None:
            print(f"  ! echec definitif {cat}",file=sys.stderr); break
        out+=j.get("query",{}).get("categorymembers",[])
        if "continue" in j: cont=j["continue"]
        else: break
        time.sleep(0.12)
    return [m["title"] for m in out]

titles=json.load(open(P,encoding="utf-8"))
titles={t:{k:set(v) for k,v in d.items()} for t,d in titles.items()}
EXCLUDE=("List of","Lists of","Category:","Template:","Timeline of","Comparison of",
         "History of","Index of","Outline of")
def add(t,key,val):
    if t.startswith(EXCLUDE): return
    e=titles.setdefault(t,{"marques":set(),"pays":set(),"annees":set()}); e[key].add(val)

print("PAYS (rattrapage complet)...")
PAYS=["Japan","Italy","the United States","Germany","the United Kingdom","Austria","Spain",
      "India","China","France","Sweden","the Czech Republic","Taiwan","South Korea",
      "Russia","Poland","Brazil","Switzerland","the Netherlands","Belgium","Hungary","Slovenia"]
for p_ in PAYS:
    pages=members(f"Category:Motorcycles of {p_}","page")
    for sc in members(f"Category:Motorcycles of {p_}","subcat"):
        pages+=members(sc,"page")
    lab=p_.replace("the ","")
    for t in pages: add(t,"pays",lab)
    print(f"   {lab:<20} {len(pages)}")
    time.sleep(0.25)

print("\nANNEES (rattrapage 1885-2026)...")
n0=len(titles); ok=0
for y in range(1885,2027):
    m=members(f"Category:Motorcycles introduced in {y}","page")
    if m: ok+=1
    for t in m: add(t,"annees",y)
    time.sleep(0.1)
print(f"   {ok} annees peuplees, +{len(titles)-n0} titres nouveaux")

json.dump({t:{k:sorted(v) for k,v in d.items()} for t,d in titles.items()},
          open(P,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n=== TOTAL : {len(titles)} articles uniques ===")
print(f"   marque : {sum(1 for d in titles.values() if d['marques'])}")
print(f"   pays   : {sum(1 for d in titles.values() if d['pays'])}")
print(f"   annee  : {sum(1 for d in titles.values() if d['annees'])}")
