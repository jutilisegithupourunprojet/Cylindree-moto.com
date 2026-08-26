# -*- coding: utf-8 -*-
"""
Etape 9 : enrichissement francophone.
  - titre et nom commercial francais (langlinks + infobox FR)
  - prix de lancement en euros (champ 'Prix a sa sortie' de l'infobox FR)
  - type/categorie en francais
  - resume FR (amorce de contenu - A REECRIRE, licence CC BY-SA)
  - licence et auteur de l'image (Commons) -> conformite juridique
Sortie : data/raw/enrichissement.json
"""
import requests, json, time, os, re

EN = "https://en.wikipedia.org/w/api.php"
FR = "https://fr.wikipedia.org/w/api.php"
COM = "https://commons.wikimedia.org/w/api.php"
S = requests.Session()
S.headers.update({"User-Agent": "MotoDirectoryResearch/0.1 (viktordu84@gmail.com)"})
RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def get(url, params, tries=5):
    d = 0.4
    for _ in range(tries):
        try:
            r = S.get(url, params=params, timeout=60)
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
    dt = dl = db = 0
    k = 0
    while k < len(body):
        c2 = body[k:k+2]
        if c2 == "{{": dt += 1; buf.append(c2); k += 2; continue
        if c2 == "}}": dt -= 1; buf.append(c2); k += 2; continue
        if c2 == "[[": dl += 1; buf.append(c2); k += 2; continue
        if c2 == "]]": dl -= 1; buf.append(c2); k += 2; continue
        ch = body[k]
        if ch == "<": db += 1
        elif ch == ">": db = max(0, db - 1)
        if ch == "|" and dt == 0 and dl == 0 and db == 0:
            parts.append("".join(buf)); buf = []; k += 1; continue
        buf.append(ch); k += 1
    parts.append("".join(buf))
    out = {}
    for p in parts[1:]:
        if "=" not in p:
            continue
        a, b = p.split("=", 1)
        a = a.strip(); b = b.strip()
        if a and b:
            out[a] = b
    return out


def clean(s):
    if not s:
        return ""
    s = re.sub(r"<ref[^>]*>.*?</ref>|<ref[^>]*/>", "", s, flags=re.S | re.I)
    s = re.sub(r"\{\{\s*(?:nb|formatnum|unit[eé]|nombre)\s*\|([^{}|]*)(?:\|[^{}]*)?\}\}",
               r"\1", s, flags=re.I)
    s = re.sub(r"<\s*br\s*/?\s*>", " / ", s, flags=re.I)
    s = re.sub(r"\{\{[^{}]*\}\}", "", s)
    s = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]|]*)\]\]", r"\1", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("&nbsp;", " ").replace("&amp;", "&")
    s = re.sub(r"'{2,}", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip(" ,;:/")


def parse_prix(v):
    """'5 699', '{{nb|7799}}', '7799 ou 8299 euros' -> premier montant en euros."""
    t = clean(v)
    if not t:
        return None, ""
    t2 = t.replace(" ", "").replace(" ", "").replace(" ", "")
    m = re.search(r"(\d{3,6})(?:[.,]\d{1,2})?", t2)
    if not m:
        return None, t
    val = int(m.group(1))
    if not (500 <= val <= 200000):      # borne de plausibilite
        return None, t
    return val, t


rows = json.load(open(os.path.join(RAW, "normalise_qa.json"), encoding="utf-8"))
titres = sorted({r["titre_wikipedia"] for r in rows})
print("%d modeles" % len(titres))

enr = {t: {} for t in titres}

# ---------------------------------------------------------- 1. lien FR + image
print("\n1. Liens vers Wikipedia FR + fichiers image...")
fichiers = {}
for i in range(0, len(titres), 40):
    chunk = titres[i:i+40]
    j = get(EN, {"action": "query", "prop": "langlinks|pageimages",
                 "lllang": "fr", "piprop": "name",
                 "titles": "|".join(chunk), "format": "json", "formatversion": "2"})
    if not j:
        continue
    for p in j.get("query", {}).get("pages", []):
        if p.get("missing"):
            continue
        t = p["title"]
        ll = p.get("langlinks", [])
        if ll:
            enr[t]["titre_fr"] = ll[0]["title"]
        if p.get("pageimage"):
            fichiers.setdefault("File:" + p["pageimage"], []).append(t)
    time.sleep(0.1)
avec_fr = sum(1 for v in enr.values() if v.get("titre_fr"))
print("   %d articles FR, %d fichiers image" % (avec_fr, len(fichiers)))

# ---------------------------------------------------------- 2. infobox FR + prix
print("\n2. Infobox FR (nom commercial, prix de lancement, type)...")
fr_titres = [(v["titre_fr"], t) for t, v in enr.items() if v.get("titre_fr")]
inv = {}
for ft, en_t in fr_titres:
    inv.setdefault(ft, en_t)
noms = list(inv.keys())
n_prix = 0
for i in range(0, len(noms), 25):
    chunk = noms[i:i+25]
    j = get(FR, {"action": "query", "prop": "revisions", "rvprop": "content",
                 "rvslots": "main", "titles": "|".join(chunk),
                 "format": "json", "formatversion": "2", "redirects": "1"})
    if not j:
        continue
    redir = {r["to"]: r["from"] for r in j.get("query", {}).get("redirects", [])}
    for p in j.get("query", {}).get("pages", []):
        if p.get("missing"):
            continue
        ft = p["title"]
        src = inv.get(ft) or inv.get(redir.get(ft, ""), "")
        if not src:
            continue
        try:
            wt = p["revisions"][0]["slots"]["main"]["content"]
        except Exception:
            continue
        box = find_infobox(wt)
        if not box:
            continue
        ch = split_params(box)
        e = enr[src]
        nom = clean(ch.get("Nom", ""))
        if nom:
            e["nom_fr"] = nom
        typ = clean(ch.get("Type", ""))
        if typ:
            e["type_fr"] = typ
        for k in ("Prix à sa sortie", "Prix a sa sortie", "Prix"):
            if k in ch:
                val, brut = parse_prix(ch[k])
                if val:
                    e["prix_lancement_eur"] = val
                    e["prix_lancement_brut"] = brut
                    e["prix_source"] = "Wikipedia FR - prix au lancement"
                    n_prix += 1
                break
    if (i // 25) % 6 == 0:
        print("   %d/%d  (%d prix)" % (i + len(chunk), len(noms), n_prix))
    time.sleep(0.12)
print("   -> %d prix de lancement recuperes" % n_prix)

# ---------------------------------------------------------- 3. resume FR
print("\n3. Resumes FR (amorce de contenu, a reecrire)...")
n_res = 0
for i in range(0, len(noms), 20):
    chunk = noms[i:i+20]
    j = get(FR, {"action": "query", "prop": "extracts", "exintro": "1",
                 "explaintext": "1", "exlimit": "20",
                 "titles": "|".join(chunk), "format": "json",
                 "formatversion": "2", "redirects": "1"})
    if not j:
        continue
    redir = {r["to"]: r["from"] for r in j.get("query", {}).get("redirects", [])}
    for p in j.get("query", {}).get("pages", []):
        ex = (p.get("extract") or "").strip()
        if not ex:
            continue
        src = inv.get(p["title"]) or inv.get(redir.get(p["title"], ""), "")
        if src:
            enr[src]["resume_fr"] = re.sub(r"\s+", " ", ex)[:900]
            n_res += 1
    time.sleep(0.12)
print("   -> %d resumes" % n_res)

# ---------------------------------------------------------- 4. licences images
print("\n4. Licences des images (Commons)...")
fl = list(fichiers.keys())
n_lic = 0
for i in range(0, len(fl), 40):
    chunk = fl[i:i+40]
    j = get(COM, {"action": "query", "prop": "imageinfo",
                  "iiprop": "extmetadata|url", "iiurlwidth": "800",
                  "titles": "|".join(chunk), "format": "json", "formatversion": "2"})
    if not j:
        continue
    for p in j.get("query", {}).get("pages", []):
        ii = (p.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata", {}) or {}

        def g(k):
            return clean(str((em.get(k, {}) or {}).get("value", "")))

        lic = g("LicenseShortName")
        auteur = g("Artist")[:120]
        for t in fichiers.get(p["title"], []):
            enr[t]["image_fichier"] = p["title"]
            enr[t]["image_licence"] = lic
            enr[t]["image_auteur"] = auteur
            enr[t]["image_page"] = ii.get("descriptionurl", "")
            enr[t]["image_vignette"] = ii.get("thumburl", "")
            if lic:
                n_lic += 1
    if (i // 40) % 8 == 0:
        print("   %d/%d" % (i + len(chunk), len(fl)))
    time.sleep(0.12)
print("   -> %d images documentees" % n_lic)

json.dump(enr, open(os.path.join(RAW, "enrichissement.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# ---------------------------------------------------------- bilan
print("\n" + "=" * 70)
print("BILAN DE L'ENRICHISSEMENT")
print("=" * 70)
for champ, lib in [("titre_fr", "article FR"), ("nom_fr", "nom commercial FR"),
                   ("type_fr", "type FR"), ("prix_lancement_eur", "prix de lancement"),
                   ("resume_fr", "resume FR"), ("image_licence", "licence image")]:
    n = sum(1 for v in enr.values() if v.get(champ))
    print("  %-22s %5d / %d  (%d%%)" % (lib, n, len(enr), 100 * n // len(enr)))

from collections import Counter
print("\nLICENCES D'IMAGES :")
for k, v in Counter(v.get("image_licence", "") for v in enr.values()
                    if v.get("image_licence")).most_common(10):
    print("   %5d  %s" % (v, k))

prix = [(v["prix_lancement_eur"], t) for t, v in enr.items() if v.get("prix_lancement_eur")]
prix.sort()
if prix:
    print("\nPRIX DE LANCEMENT - echantillon :")
    for p, t in prix[:4] + prix[len(prix)//2:len(prix)//2+3] + prix[-4:]:
        print("   %8d EUR   %s" % (p, t))
