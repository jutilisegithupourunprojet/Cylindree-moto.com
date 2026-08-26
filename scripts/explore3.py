# -*- coding: utf-8 -*-
"""Test de couverture : les infobox Wikipedia contiennent-elles les specs ?"""
import requests, re, sys
API = "https://en.wikipedia.org/w/api.php"
H = {"User-Agent": "MotoDirectoryResearch/0.1 (viktordu84@gmail.com)"}

def wikitext(title):
    r = requests.get(API, params={"action":"parse","page":title,"prop":"wikitext",
                                  "format":"json","formatversion":"2"}, headers=H, timeout=30)
    j = r.json()
    if "error" in j: return None
    return j["parse"]["wikitext"]

TESTS = ["Yamaha MT-07","Honda CB750","Kawasaki Z650","Ducati Monster",
         "Harley-Davidson Sportster","BMW R1250GS","Suzuki SV650","Yamaha YZF-R1"]

for t in TESTS:
    wt = wikitext(t)
    if not wt:
        print(f"{t:<28} -> ABSENT")
        continue
    m = re.search(r"\{\{\s*Infobox[^\n]*\n(.*?)\n\}\}", wt, re.S|re.I)
    if not m:
        print(f"{t:<28} -> article OK, pas d'infobox detectee")
        continue
    box = m.group(1)
    fields = re.findall(r"^\s*\|\s*([A-Za-z_0-9 ]+?)\s*=", box, re.M)
    print(f"{t:<28} -> {len(fields):>2} champs : {', '.join(f.strip() for f in fields[:14])}")
