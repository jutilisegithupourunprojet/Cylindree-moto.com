# -*- coding: utf-8 -*-
import requests
API="https://en.wikipedia.org/w/api.php"
S=requests.Session(); S.headers.update({"User-Agent":"MotoDirectoryResearch/0.1 (viktordu84@gmail.com)"})

def parents(title):
    j=S.get(API,params={"action":"query","prop":"categories","titles":title,
        "cllimit":"max","format":"json","formatversion":"2"},timeout=30).json()
    return [c["title"] for c in j["query"]["pages"][0].get("categories",[])]

def members(cat, typ):
    out,cont=[],{}
    while True:
        p={"action":"query","list":"categorymembers","cmtitle":cat,"cmlimit":500,
           "cmtype":typ,"format":"json","formatversion":"2"}; p.update(cont)
        j=S.get(API,params=p,timeout=30).json()
        out+=j.get("query",{}).get("categorymembers",[])
        if "continue" in j: cont=j["continue"]
        else: break
    return out

print("=== PARENTS DE 'Category:Yamaha motorcycles' ===")
for p in parents("Category:Yamaha motorcycles"): print("   ",p)

for parent in ["Category:Motorcycles by manufacturer","Category:Motorcycles by brand"]:
    subs=members(parent,"subcat")
    print(f"\n=== '{parent}' -> {len(subs)} sous-categories")
    for s in subs[:15]: print("   ",s["title"])

# volume via 'introduced in YYYY'
tot=0; yrs=0
for y in range(1950,2027):
    m=members(f"Category:Motorcycles introduced in {y}","page")
    if m: tot+=len(m); yrs+=1
print(f"\n=== 'Motorcycles introduced in YYYY' (1950-2026) : {tot} articles sur {yrs} annees")
