# -*- coding: utf-8 -*-
"""Combien d'articles moto sont enumerables via les categories Wikipedia ?"""
import requests
API = "https://en.wikipedia.org/w/api.php"
H = {"User-Agent": "MotoDirectoryResearch/0.1 (viktordu84@gmail.com)"}
S = requests.Session(); S.headers.update(H)

def members(cat, typ="page|subcat", limit=500):
    out, cont = [], {}
    while True:
        p = {"action":"query","list":"categorymembers","cmtitle":cat,"cmlimit":limit,
             "cmtype":typ,"format":"json","formatversion":"2"}
        p.update(cont)
        j = S.get(API, params=p, timeout=30).json()
        out += j.get("query",{}).get("categorymembers",[])
        if "continue" in j: cont = j["continue"]
        else: break
    return out

subs = members("Category:Motorcycles by manufacturer", typ="subcat")
print(f"Sous-categories constructeurs : {len(subs)}\n")
total = 0
rows = []
for s in subs:
    pages = members(s["title"], typ="page")
    subsubs = members(s["title"], typ="subcat")
    n = len(pages)
    for ss in subsubs:
        n += len(members(ss["title"], typ="page"))
    rows.append((n, s["title"].replace("Category:","")))
    total += n
rows.sort(reverse=True)
for n, t in rows[:30]:
    print(f"{n:>5}  {t}")
print(f"\nTOTAL articles (avec doublons) : {total}")
