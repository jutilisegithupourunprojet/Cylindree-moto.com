# -*- coding: utf-8 -*-
import requests
API="https://en.wikipedia.org/w/api.php"
S=requests.Session(); S.headers.update({"User-Agent":"MotoDirectoryResearch/0.1 (viktordu84@gmail.com)"})

def search_cat(term, n=25):
    j=S.get(API,params={"action":"query","list":"search","srsearch":f"incategory-like {term}",
        "srnamespace":14,"srlimit":n,"format":"json","formatversion":"2"},timeout=30).json()
    return [x["title"] for x in j.get("query",{}).get("search",[])]

for term in ["motorcycles by manufacturer","motorcycles","Honda motorcycles","motorcycles introduced"]:
    print(f"--- recherche categorie: {term}")
    for t in search_cat(term, 12): print("   ", t)
    print()

# categories de l'article Yamaha MT-07 : point d'entree fiable
j=S.get(API,params={"action":"query","prop":"categories","titles":"Yamaha MT-07",
    "cllimit":"max","format":"json","formatversion":"2"},timeout=30).json()
print("=== CATEGORIES DE 'Yamaha MT-07' ===")
for c in j["query"]["pages"][0].get("categories",[]): print("   ", c["title"])
