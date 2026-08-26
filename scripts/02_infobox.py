# -*- coding: utf-8 -*-
"""
Etape 2 : recuperation du wikitext + extraction des infobox.
Parseur a accolades equilibrees (les templates imbriques cassent une regex simple).
Sortie : data/raw/infobox.json
"""
import requests, json, time, os, re, sys

API="https://en.wikipedia.org/w/api.php"
S=requests.Session(); S.headers.update({"User-Agent":"MotoDirectoryResearch/0.1 (viktordu84@gmail.com)"})
RAW=os.path.join(os.path.dirname(__file__),"..","data","raw")

def get(params,tries=6):
    d=0.4
    for _ in range(tries):
        try:
            r=S.get(API,params=params,timeout=60)
            if r.status_code==200 and r.text.lstrip().startswith("{"): return r.json()
        except Exception: pass
        time.sleep(d); d*=2
    return None

def find_infobox(wt):
    """Retourne le contenu brut de la premiere {{Infobox ...}} , accolades equilibrees."""
    m=re.search(r"\{\{\s*Infobox",wt,re.I)
    if not m: return None
    i=m.start(); depth=0; j=i
    while j < len(wt)-1:
        if wt[j:j+2]=="{{": depth+=1; j+=2; continue
        if wt[j:j+2]=="}}":
            depth-=1; j+=2
            if depth==0: return wt[i:j]
            continue
        j+=1
    return None

def split_params(box):
    """Decoupe sur les | de premier niveau (ignore {{}}, [[]], tables)."""
    body=box[2:-2]
    parts=[]; buf=[]; d_t=d_l=d_b=0
    k=0
    while k < len(body):
        c2=body[k:k+2]
        if c2=="{{": d_t+=1; buf.append(c2); k+=2; continue
        if c2=="}}": d_t-=1; buf.append(c2); k+=2; continue
        if c2=="[[": d_l+=1; buf.append(c2); k+=2; continue
        if c2=="]]": d_l-=1; buf.append(c2); k+=2; continue
        ch=body[k]
        if ch=="<": d_b+=1
        elif ch==">": d_b=max(0,d_b-1)
        if ch=="|" and d_t==0 and d_l==0 and d_b==0:
            parts.append("".join(buf)); buf=[]; k+=1; continue
        buf.append(ch); k+=1
    parts.append("".join(buf))
    out={}
    for p in parts[1:]:
        if "=" not in p: continue
        k_,v=p.split("=",1)
        k_=k_.strip().lower()
        v=v.strip()
        if k_ and v: out[k_]=v
    return out

titles=list(json.load(open(os.path.join(RAW,"titres.json"),encoding="utf-8")).keys())
print(f"{len(titles)} articles a traiter")

res={}
B=40
for i in range(0,len(titles),B):
    chunk=titles[i:i+B]
    j=get({"action":"query","prop":"revisions|pageprops|pageimages",
           "rvprop":"content","rvslots":"main","piprop":"original",
           "titles":"|".join(chunk),"format":"json","formatversion":"2",
           "redirects":"1"})
    if j is None:
        print(f"  ! lot {i} echoue",file=sys.stderr); continue
    for pg in j.get("query",{}).get("pages",[]):
        if pg.get("missing"): continue
        t=pg["title"]
        try: wt=pg["revisions"][0]["slots"]["main"]["content"]
        except Exception: continue
        box=find_infobox(wt)
        rec={"titre":t,
             "wikidata":pg.get("pageprops",{}).get("wikibase_item"),
             "image":pg.get("original",{}).get("source"),
             "infobox_type":None,"champs":{}}
        if box:
            mt=re.match(r"\{\{\s*Infobox\s*([^\n|]*)",box,re.I)
            rec["infobox_type"]=(mt.group(1).strip() if mt else "")
            rec["champs"]=split_params(box)
        res[t]=rec
    if (i//B)%10==0:
        print(f"   {i+len(chunk)}/{len(titles)}  ({sum(1 for r in res.values() if r['champs'])} avec infobox)")
    time.sleep(0.15)

json.dump(res,open(os.path.join(RAW,"infobox.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)

avec=[r for r in res.values() if r["champs"]]
print(f"\n=== {len(res)} articles recuperes, {len(avec)} avec infobox ===")
from collections import Counter
print("\nTypes d'infobox :")
for k,v in Counter(r["infobox_type"] for r in avec).most_common(8): print(f"   {v:>5}  {k}")
print("\nChamps les plus frequents :")
for k,v in Counter(c for r in avec for c in r["champs"]).most_common(40): print(f"   {v:>5}  {k}")
