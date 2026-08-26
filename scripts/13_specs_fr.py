# -*- coding: utf-8 -*-
"""
Etape 13 : specifications issues de Wikipedia FR.

Les infobox francaises contiennent les caracteristiques deja en unites
metriques, et les descriptions (cadre, suspensions, freins) directement en
francais. On s'en sert pour COMBLER LES TROUS de la base anglophone.

Regles :
  - on ne remplace jamais une valeur existante, on ne remplit que le vide ;
  - le champ 'Couple' des infobox FR melange N.m et m.kg selon les articles.
    Sans marqueur d'unite explicite, on ne l'importe pas : mieux vaut une
    case vide qu'un chiffre faux ;
  - toute valeur hors bornes physiques est rejetee.

Sortie : data/raw/specs_fr.json
"""
import requests, json, re, os, time

FR = "https://fr.wikipedia.org/w/api.php"
S = requests.Session()
S.headers.update({"User-Agent": "MotoDirectoryResearch/0.1 (viktordu84@gmail.com)"})
RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def get(params, tries=5):
    d = 0.4
    for _ in range(tries):
        try:
            r = S.get(FR, params=params, timeout=60)
            if r.status_code == 200 and r.text.lstrip().startswith("{"):
                return r.json()
        except Exception:
            pass
        time.sleep(d); d *= 2
    return None


def find_ib(wt):
    m = re.search(r"\{\{\s*Infobox", wt, re.I)
    if not m:
        return None
    i, d, j = m.start(), 0, m.start()
    while j < len(wt) - 1:
        if wt[j:j+2] == "{{":
            d += 1; j += 2; continue
        if wt[j:j+2] == "}}":
            d -= 1; j += 2
            if d == 0:
                return wt[i:j]
            continue
        j += 1
    return None


def params_ib(box):
    body = box[2:-2]
    parts, buf = [], []
    dt = dl = 0
    k = 0
    while k < len(body):
        c2 = body[k:k+2]
        if c2 == "{{": dt += 1; buf.append(c2); k += 2; continue
        if c2 == "}}": dt -= 1; buf.append(c2); k += 2; continue
        if c2 == "[[": dl += 1; buf.append(c2); k += 2; continue
        if c2 == "]]": dl -= 1; buf.append(c2); k += 2; continue
        ch = body[k]
        if ch == "|" and dt == 0 and dl == 0:
            parts.append("".join(buf)); buf = []; k += 1; continue
        buf.append(ch); k += 1
    parts.append("".join(buf))
    out = {}
    for p in parts[1:]:
        if "=" not in p:
            continue
        a, b = p.split("=", 1)
        a, b = a.strip(), b.strip()
        if a and b:
            out[a] = b
    return out


def texte(v):
    """Nettoie pour affichage : garde le francais, retire le balisage."""
    if not v:
        return ""
    v = re.sub(r"<ref[^>]*>.*?</ref>|<ref[^>]*/>", "", v, flags=re.S | re.I)
    v = re.sub(r"\{\{\s*unité\s*\|([^{}|]*)\|?([^{}|]*)\|?([^{}]*)\}\}",
               lambda m: (m.group(1) + " " + m.group(2)).strip(), v, flags=re.I)
    v = re.sub(r"\{\{\s*(?:nb|formatnum|nombre)\s*\|([^{}|]*)[^{}]*\}\}", r"\1", v, flags=re.I)
    v = re.sub(r"\{\{[^{}]*\}\}", "", v)
    v = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]|]*)\]\]", r"\1", v)
    v = re.sub(r"<[^>]+>", "", v)
    v = v.replace("&nbsp;", " ").replace("&amp;", "&")
    v = re.sub(r"'{2,}", "", v)
    return re.sub(r"\s+", " ", v).strip(" ,;:")


def nombre(v):
    """Premier nombre de la valeur, ou None."""
    t = texte(v).replace(",", ".").replace(" ", "").replace(" ", "")
    m = re.search(r"-?\d+(?:\.\d+)?", t)
    return float(m.group(0)) if m else None


# champ FR -> (champ interne, borne min, borne max)
NUM = {
 "Cylindrée":        ("cylindree_cc", 30, 2500),
 "Puissance":        ("puissance_ch", 1, 320),
 "Régime Puissance": ("puissance_tr_min", 1000, 20000),
 "Régime Couple":    ("couple_tr_min", 800, 18000),
 "Poids à sec":      ("poids_sec_kg", 30, 500),
 "Poids tous pleins faits": ("poids_tous_pleins_kg", 30, 550),
 "Hauteur de selle": ("hauteur_selle_mm", 500, 1000),
 "Empattement":      ("empattement_mm", 900, 1900),
 "Réservoir":        ("reservoir_l", 2, 40),
 "Vitesse maximale": ("vitesse_max_kmh", 25, 400),
}
# champs texte : le francais d'origine vaut mieux qu'une traduction automatique
TXT = {
 "Cadre": "cadre_fr",
 "Suspension avant": "suspension_av_fr",
 "Suspension arrière": "suspension_ar_fr",
 "Frein avant": "frein_av_fr",
 "Frein arrière": "frein_ar_fr",
 "Transmission": "transmission_fr",
 "Boîte de vitesses": "boite_fr",
 "Moteurs": "moteur_fr",
 "Distribution": "distribution_fr",
 "Alimentation": "alimentation_fr",
 "Embrayage": "embrayage_fr",
 "Roue avant": "pneu_av_fr",
 "Roue arrière": "pneu_ar_fr",
}

enr = json.load(open(os.path.join(RAW, "enrichissement.json"), encoding="utf-8"))
inv = {}
for src, v in enr.items():
    if v.get("titre_fr"):
        inv.setdefault(v["titre_fr"], src)
noms = sorted(inv)
print("%d articles FR a exploiter" % len(noms))

out = {}
n_couple_rejete = 0
for i in range(0, len(noms), 20):
    lot = noms[i:i+20]
    j = get({"action": "query", "prop": "revisions", "rvprop": "content",
             "rvslots": "main", "titles": "|".join(lot),
             "format": "json", "formatversion": "2", "redirects": "1"})
    if not j:
        continue
    q = j.get("query", {})
    redir = {r["to"]: r["from"] for r in q.get("redirects", [])}
    for p in q.get("pages", []):
        if p.get("missing"):
            continue
        src = inv.get(p["title"]) or inv.get(redir.get(p["title"], ""), "")
        if not src:
            continue
        try:
            wt = p["revisions"][0]["slots"]["main"]["content"]
        except Exception:
            continue
        box = find_ib(wt)
        if not box:
            continue
        ch = params_ib(box)
        rec = {}
        for k_fr, (k_int, lo, hi) in NUM.items():
            if k_fr not in ch:
                continue
            v = nombre(ch[k_fr])
            if v is not None and lo <= v <= hi:
                rec[k_int] = round(v, 2)
        # couple : unite ambigue en francais (N.m ou m.kg selon l'article)
        if "Couple" in ch:
            brut = texte(ch["Couple"])
            v = nombre(brut)
            if v is not None:
                if re.search(r"N\s*[.·]?\s*m", brut, re.I) and 2 <= v <= 250:
                    rec["couple_nm"] = round(v, 1)
                elif re.search(r"m\s*[.·]?\s*kg|kg\s*[.·]?\s*m|daN", brut, re.I):
                    n = v * 9.80665 if not re.search(r"daN", brut, re.I) else v * 10
                    if 2 <= n <= 250:
                        rec["couple_nm"] = round(n, 1)
                else:
                    n_couple_rejete += 1   # unite non precisee : on n'importe pas
        for k_fr, k_int in TXT.items():
            if k_fr in ch:
                t = texte(ch[k_fr])
                if t:
                    rec[k_int] = t[:220]
        if rec:
            rec["source_fr"] = "https://fr.wikipedia.org/wiki/" + p["title"].replace(" ", "_")
            out[src] = rec
    if (i // 20) % 5 == 0:
        print("   %d/%d  (%d fiches)" % (i + len(lot), len(noms), len(out)))
    time.sleep(0.12)

json.dump(out, open(os.path.join(RAW, "specs_fr.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("\n=== %d fiches enrichies depuis Wikipedia FR ===" % len(out))
print("   %d valeurs de couple rejetees (unite non precisee)" % n_couple_rejete)
from collections import Counter
c = Counter(k for v in out.values() for k in v if k != "source_fr")
print("\nCHAMPS RECUPERES :")
for k, v in c.most_common():
    print("   %4d  %s" % (v, k))
