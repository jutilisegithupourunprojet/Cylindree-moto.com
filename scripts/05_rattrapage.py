# -*- coding: utf-8 -*-
"""
Etape 5 : rattrapage cible des modeles du marche francais absents de l'enumeration
par categories (titres Wikipedia differents du nom commercial francais).
Complete data/raw/titres.json et data/raw/infobox.json.
"""
import requests, json, time, os, re, sys

API = "https://en.wikipedia.org/w/api.php"
S = requests.Session()
S.headers.update({"User-Agent": "MotoDirectoryResearch/0.1 (viktordu84@gmail.com)"})
RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

sys.path.insert(0, os.path.dirname(__file__))
from importlib import import_module
_ib = import_module("02_infobox") if False else None  # on redefinit localement

def get(params, tries=6):
    d = 0.4
    for _ in range(tries):
        try:
            r = S.get(API, params=params, timeout=45)
            if r.status_code == 200 and r.text.lstrip().startswith("{"):
                return r.json()
        except Exception:
            pass
        time.sleep(d); d *= 2
    return None

def find_infobox(wt):
    m = re.search(r"\{\{\s*Infobox", wt, re.I)
    if not m:
        return None
    i = m.start(); depth = 0; j = i
    while j < len(wt) - 1:
        if wt[j:j+2] == "{{":
            depth += 1; j += 2; continue
        if wt[j:j+2] == "}}":
            depth -= 1; j += 2
            if depth == 0:
                return wt[i:j]
            continue
        j += 1
    return None

def split_params(box):
    body = box[2:-2]
    parts, buf = [], []
    d_t = d_l = d_b = 0
    k = 0
    while k < len(body):
        c2 = body[k:k+2]
        if c2 == "{{": d_t += 1; buf.append(c2); k += 2; continue
        if c2 == "}}": d_t -= 1; buf.append(c2); k += 2; continue
        if c2 == "[[": d_l += 1; buf.append(c2); k += 2; continue
        if c2 == "]]": d_l -= 1; buf.append(c2); k += 2; continue
        ch = body[k]
        if ch == "<": d_b += 1
        elif ch == ">": d_b = max(0, d_b - 1)
        if ch == "|" and d_t == 0 and d_l == 0 and d_b == 0:
            parts.append("".join(buf)); buf = []; k += 1; continue
        buf.append(ch); k += 1
    parts.append("".join(buf))
    out = {}
    for p in parts[1:]:
        if "=" not in p:
            continue
        k_, v = p.split("=", 1)
        k_ = k_.strip().lower(); v = v.strip()
        if k_ and v:
            out[k_] = v
    return out

# familles absentes + requetes de recherche associees
RECHERCHES = [
 ("Honda", "Honda NC700 series"), ("Honda", "Honda NC750X"),
 ("Honda", "Honda CRF1000L Africa Twin"), ("Honda", "Honda XRV750"),
 ("Honda", "Honda Forza"), ("Honda", "Honda CB600F Hornet"),
 ("Honda", "Honda CB650R"), ("Honda", "Honda CB1000R"),
 ("Honda", "Honda PCX"), ("Honda", "Honda X-ADV"),
 ("Honda", "Honda CBR650R"), ("Honda", "Honda Rebel 500"),
 ("Yamaha", "Yamaha XT660Z Tenere"), ("Yamaha", "Yamaha Tenere 700"),
 ("Yamaha", "Yamaha MT-03"), ("Yamaha", "Yamaha MT-10"),
 ("Yamaha", "Yamaha NMAX"), ("Yamaha", "Yamaha XMAX"),
 ("Kawasaki", "Kawasaki Z900RS"), ("Kawasaki", "Kawasaki Eliminator"),
 ("Suzuki", "Suzuki GSX-8S"), ("Suzuki", "Suzuki Burgman"),
 ("BMW", "BMW R1300GS"), ("BMW", "BMW F900R"), ("BMW", "BMW G310R"),
 ("BMW", "BMW C400X"),
 ("KTM", "KTM 790 Duke"), ("KTM", "KTM 690 Duke"), ("KTM", "KTM RC 390"),
 ("Ducati", "Ducati DesertX"), ("Ducati", "Ducati Diavel"),
 ("Ducati", "Ducati Streetfighter"), ("Ducati", "Ducati Hypermotard"),
 ("Triumph", "Triumph Tiger 900"), ("Triumph", "Triumph Speed Triple"),
 ("Triumph", "Triumph Rocket 3"), ("Triumph", "Triumph Scrambler 400"),
 ("Aprilia", "Aprilia Tuono"), ("Aprilia", "Aprilia Tuareg"),
 ("Moto Guzzi", "Moto Guzzi V85 TT"),
 ("Harley-Davidson", "Harley-Davidson Pan America"),
 ("Harley-Davidson", "Harley-Davidson Street Glide"),
 ("Harley-Davidson", "Harley-Davidson Iron 883"),
 ("Royal Enfield", "Royal Enfield Himalayan"),
 ("Piaggio", "Piaggio MP3"), ("Piaggio", "Vespa GTS"),
 ("Zero Motorcycles", "Zero SR/F"),
]

titres = json.load(open(os.path.join(RAW, "titres.json"), encoding="utf-8"))
boxes = json.load(open(os.path.join(RAW, "infobox.json"), encoding="utf-8"))
avant_t, avant_b = len(titres), len(boxes)

# 1) resolution des titres reels via l'API de recherche
cibles = {}
for marque, q in RECHERCHES:
    j = get({"action": "query", "list": "search", "srsearch": q, "srnamespace": 0,
             "srlimit": 3, "format": "json", "formatversion": "2"})
    if not j:
        continue
    for hit in j.get("query", {}).get("search", []):
        t = hit["title"]
        if t.startswith(("List of", "Lists of", "Comparison of", "History of")):
            continue
        if t not in boxes:
            cibles[t] = marque
    time.sleep(0.12)

print("%d titres candidats a recuperer" % len(cibles))

# 2) recuperation + parsing
noms = list(cibles.keys())
ajoutes = 0
for i in range(0, len(noms), 40):
    chunk = noms[i:i+40]
    j = get({"action": "query", "prop": "revisions|pageprops|pageimages",
             "rvprop": "content", "rvslots": "main", "piprop": "original",
             "titles": "|".join(chunk), "format": "json", "formatversion": "2",
             "redirects": "1"})
    if not j:
        continue
    for pg in j.get("query", {}).get("pages", []):
        if pg.get("missing"):
            continue
        t = pg["title"]
        try:
            wt = pg["revisions"][0]["slots"]["main"]["content"]
        except Exception:
            continue
        box = find_infobox(wt)
        if not box:
            continue
        mt = re.match(r"\{\{\s*Infobox\s*([^\n|]*)", box, re.I)
        typ = (mt.group(1).strip() if mt else "")
        if typ.lower() != "motorcycle":
            continue
        boxes[t] = {"titre": t,
                    "wikidata": pg.get("pageprops", {}).get("wikibase_item"),
                    "image": pg.get("original", {}).get("source"),
                    "infobox_type": typ,
                    "champs": split_params(box)}
        marque = cibles.get(t) or cibles.get(chunk[0], "")
        if t not in titres:
            titres[t] = {"marques": [marque] if marque else [], "pays": [], "annees": []}
        ajoutes += 1
    time.sleep(0.15)

json.dump(titres, open(os.path.join(RAW, "titres.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
json.dump(boxes, open(os.path.join(RAW, "infobox.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("+%d fiches moto ajoutees" % ajoutes)
print("titres : %d -> %d   |   infobox : %d -> %d"
      % (avant_t, len(titres), avant_b, len(boxes)))
