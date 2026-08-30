# -*- coding: utf-8 -*-
"""
Etape 3 : normalisation des infobox en schema exploitable.
Regle absolue : on ne fabrique jamais une valeur. Champ absent => vide.
Sortie : data/raw/normalise.json
"""
import json, re, os, unicodedata
from collections import Counter

RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

# ---------------------------------------------------------------- marques
# pays d'origine = pays du constructeur (siege historique de la marque)
MARQUES = {
 "Honda": ("Japon", "japonaise"), "Yamaha": ("Japon", "japonaise"),
 "Suzuki": ("Japon", "japonaise"), "Kawasaki": ("Japon", "japonaise"),
 "Mitsubishi Motors": ("Japon", "japonaise"),
 "Ducati": ("Italie", "italienne"), "Aprilia": ("Italie", "italienne"),
 "Piaggio": ("Italie", "italienne"), "MV Agusta": ("Italie", "italienne"),
 "Moto Guzzi": ("Italie", "italienne"), "Benelli": ("Italie", "italienne"),
 "Laverda": ("Italie", "italienne"), "Gilera": ("Italie", "italienne"),
 "Cagiva": ("Italie", "italienne"), "Bimota": ("Italie", "italienne"),
 "Malaguti": ("Italie", "italienne"), "Mondial": ("Italie", "italienne"),
 "Harley-Davidson": ("États-Unis", "américaine"),
 "Indian Motorcycles": ("États-Unis", "américaine"),
 "Buell": ("États-Unis", "américaine"),
 "Zero Motorcycles": ("États-Unis", "américaine"),
 "ACE": ("États-Unis", "américaine"), "Excelsior": ("États-Unis", "américaine"),
 "MTT": ("États-Unis", "américaine"), "Flyscooters": ("États-Unis", "américaine"),
 "BSA": ("Royaume-Uni", "britannique"),
 "Triumph Motorcycles Ltd": ("Royaume-Uni", "britannique"),
 "Triumph Engineering": ("Royaume-Uni", "britannique"),
 "Norton": ("Royaume-Uni", "britannique"), "AMC": ("Royaume-Uni", "britannique"),
 "Vincent": ("Royaume-Uni", "britannique"), "Velocette": ("Royaume-Uni", "britannique"),
 "AJS": ("Royaume-Uni", "britannique"), "Ariel": ("Royaume-Uni", "britannique"),
 "Panther": ("Royaume-Uni", "britannique"),
 "Brough Superior": ("Royaume-Uni", "britannique"),
 "Douglas": ("Royaume-Uni", "britannique"), "James": ("Royaume-Uni", "britannique"),
 "Scott": ("Royaume-Uni", "britannique"), "Sunbeam": ("Royaume-Uni", "britannique"),
 "BMW": ("Allemagne", "allemande"), "MZ": ("Allemagne", "allemande"),
 "NSU": ("Allemagne", "allemande"), "Sachs": ("Allemagne", "allemande"),
 "Maico": ("Allemagne", "allemande"), "Brennabor": ("Allemagne", "allemande"),
 "KTM": ("Autriche", "autrichienne"), "Puch": ("Autriche", "autrichienne"),
 "Husqvarna": ("Suède", "suédoise"),
 "Peugeot": ("France", "française"),
 "Derbi": ("Espagne", "espagnole"),
 "Royal Enfield": ("Inde", "indienne"), "Bajaj": ("Inde", "indienne"),
 "Hero Honda": ("Inde", "indienne"), "TVS": ("Inde", "indienne"),
 "Escorts": ("Inde", "indienne"), "Kinetic": ("Inde", "indienne"),
 "Ideal Jawa": ("Inde", "indienne"), "Mahindra & Mahindra": ("Inde", "indienne"),
 "Hyosung": ("Corée du Sud", "coréenne"),
 "Kymco": ("Taiwan", "taiwanaise"), "Zongshen": ("Chine", "chinoise"),
 "Jawa": ("Tchéquie", "tchèque"),
 "Sokol": ("Pologne", "polonaise"), "SHL": ("Pologne", "polonaise"),
 "Dnepr": ("Ukraine", "autre"), "Tunturi": ("Finlande", "autre"),
 "Condor": ("Suisse", "autre"), "Kasinski": ("Brésil", "autre"),
 "Amazonas Motos Especiais": ("Brésil", "autre"), "Modenas": ("Malaisie", "autre"),
 "Campagna": ("Canada", "autre"),
 "Bombardier Recreational Products": ("Canada", "autre"),
}

# --- signal 1 (prioritaire) : categories de l'article Wikipedia
CAT_ARTICLE = [
 ("Maxi scooters", "Scooter / Cyclomoteur"),
 ("Motor scooters", "Scooter / Cyclomoteur"),
 ("Electric scooters", "Scooter / Cyclomoteur"),
 ("Three-wheeled motor scooters", "Trois-roues"),
 ("Mopeds", "Scooter / Cyclomoteur"),
 ("Standard motorcycles", "Roadster"),
 ("Sport bikes", "Sportive"),
 ("Dual-sport motorcycles", "Trail / Aventure"),
 ("Cruiser motorcycles", "Custom / Cruiser"),
 ("Touring motorcycles", "Routière / GT"),
 ("Off-road motorcycles", "Tout-terrain"),
 ("Motocross", "Tout-terrain"),
 ("Cafe racers", "Café racer"),
 ("Custom motorcycles", "Custom / Cruiser"),
]

# --- signal 2 (secours) : champ 'class' de l'infobox
CATEGORIES = [
 (r"\bsport ?bike|\bsuperbike|\bsuper bike|\bsupersport|\bsports? motorcycle|\bsports\b",
  "Sportive"),
 (r"\bcaf[eé] ?racer", "Café racer"),
 (r"\bsupermotard|\bsupermoto", "Supermotard"),
 (r"\bstreetfighter|\bnaked|\bstandard\b|\broadster|\bcommuter|\bstep.?through",
  "Roadster"),
 (r"\bdual.?sport|\badventure|\bdual.?purpose|\benduro|\bon/?.?off.?road",
  "Trail / Aventure"),
 (r"\bcruiser|\bchopper|\bbobber|\bcustom", "Custom / Cruiser"),
 (r"\btouring|\bsport.?tour|\btourer", "Routière / GT"),
 (r"\bscooter|\bmoped|\bunderbone", "Scooter / Cyclomoteur"),
 (r"\bmotocross|\bmoto.?cross|\bdirt ?bike|\btrials?\b|\boff.?road", "Tout-terrain"),
 (r"\bmini.?bike|\bpocket", "Minibike"),
 (r"\bthree.?wheel|\btrike", "Trois-roues"),
 (r"\belectric", "Électrique"),
 (r"\bmotogp|\bgrand prix|\brace|\bracing|\bstreamliner", "Compétition"),
]

ARCHS = [
 (r"\bv-?twin", "V-twin"),
 (r"\bflat-?twin|\bboxer", "Flat-twin (boxer)"),
 (r"\bv-?four|\bv4\b", "V4"),
 (r"\binline-?four|\bi4\b|\bfour-cylinder|\bstraight-four", "4 cylindres en ligne"),
 (r"\bstraight-?twin|\bparallel-?twin|\btwin-cylinder", "Twin parallèle"),
 (r"\btriple|\bthree-cylinder|\binline-?three", "3 cylindres"),
 (r"\bflat-?six|\bsix-cylinder", "6 cylindres"),
 (r"\brotary|\bwankel", "Rotatif"),
 (r"\bsingle|\bthumper", "Monocylindre"),
]

# ---------------------------------------------------------------- unites
K = {
 "cc": 1.0, "cm3": 1.0, "ccm": 1.0, "cuin": 16.3871, "cuins": 16.3871,
 "cid": 16.3871, "l": 1000.0, "litre": 1000.0,
 "kg": 1.0, "lb": 0.453592, "lbs": 0.453592,
 "mm": 1.0, "cm": 10.0, "in": 25.4, "inch": 25.4, "inches": 25.4,
 "ft": 304.8, "m": 1000.0,
 "km/h": 1.0, "kmh": 1.0, "kph": 1.0, "mph": 1.60934,
 "nm": 1.0, "n.m": 1.0, "n·m": 1.0, "lbft": 1.35582, "lb-ft": 1.35582,
 "ft⋅lbf": 1.35582, "ftlbf": 1.35582, "lbf·ft": 1.35582,
 "kgm": 9.80665, "kg·m": 9.80665, "kg*m": 9.80665,
 "kw": 1.0, "hp": 0.745700, "bhp": 0.745700, "shp": 0.745700,
 "ps": 0.735499, "cv": 0.735499, "ch": 0.735499,
}
FAM = {
 "vol": {"cc", "cm3", "ccm", "cuin", "cuins", "cid", "l", "litre"},
 "mass": {"kg", "lb", "lbs"},
 "len": {"mm", "cm", "in", "inch", "inches", "ft", "m"},
 "spd": {"km/h", "kmh", "kph", "mph"},
 "trq": {"nm", "n.m", "n·m", "lbft", "lb-ft", "ft⋅lbf", "ftlbf",
         "lbf·ft", "kgm", "kg·m", "kg*m"},
 "pwr": {"kw", "hp", "bhp", "shp", "ps", "cv", "ch"},
}

def fam_of(u):
    u = (u or "").lower().strip()
    for f, s in FAM.items():
        if u in s:
            return f
    return None

CONV_RE = re.compile(r"\{\{\s*(?:convert|cvt)\s*\|([^{}]*)\}\}", re.I)
NUM = r"[-+]?\d[\d,]*\.?\d*"

def _f(s):
    try:
        return float(str(s).replace(",", "").strip())
    except Exception:
        return None

def convert_vals(text):
    """Extrait les (valeur, unite) des templates {{convert}}/{{cvt}}."""
    out = []
    for m in CONV_RE.finditer(text or ""):
        parts = [p.strip() for p in m.group(1).split("|")]
        parts = [p for p in parts if p and "=" not in p]
        if len(parts) < 2:
            continue
        v1 = _f(parts[0])
        if v1 is None:
            continue
        if len(parts) >= 4 and parts[1].lower() in ("to", "or", "-", "–", "and", "by"):
            v2 = _f(parts[2])
            u = parts[3]
            if v2 is not None and fam_of(u):
                out.append((v1, u))
                out.append((v2, u))
                continue
        out.append((v1, parts[1]))
    return [(v, u) for v, u in out if fam_of(u)]

PLAIN = re.compile(
    r"(" + NUM + r")\s*(km/h|kmh|kph|mph|cc|cm3|ccm|cuin|kg|lbs?|mm|cm|inch(?:es)?|in\b|"
    r"n·m|n\.m|nm|lb-?ft|ft⋅lbf|kg\*?m|kw|bhp|hp|ps|cv|ch)\b", re.I)

def extract(text, family, prefer=None):
    """Retourne la valeur dans l'unite pivot de la famille, ou None. Jamais d'invention."""
    if not text:
        return None
    cands = [(v, u) for v, u in convert_vals(text) if fam_of(u) == family]
    if not cands:
        clean = re.sub(r"<ref[^>]*>.*?</ref>|<ref[^>]*/>", "", text, flags=re.S | re.I)
        clean = re.sub(r"&nbsp;|&#160;", " ", clean)
        cands = [(_f(a), b) for a, b in PLAIN.findall(clean)]
        cands = [(v, u) for v, u in cands if v is not None and fam_of(u) == family]
    if not cands:
        return None
    if prefer:
        pr = [(v, u) for v, u in cands if u.lower().strip() in prefer]
        if pr:
            cands = pr
    v, u = cands[0]
    return round(v * K[u.lower().strip()], 2)

def rpm_of(text):
    if not text:
        return None
    m = re.search(r"@\s*(" + NUM + r")\s*(?:&nbsp;|\s)*rpm", text, re.I)
    if not m:
        return None
    v = _f(m.group(1))
    return int(v) if v else None

def strip_wiki(s):
    if not s:
        return ""
    s = re.sub(r"<ref[^>]*>.*?</ref>|<ref[^>]*/>", "", s, flags=re.S | re.I)
    def _conv(m):
        # garde toutes les valeurs et separateurs, retient la premiere unite
        parts = [x.strip() for x in m.group(1).split("|") if "=" not in x]
        vals, unite = [], ""
        for x in parts:
            if unite:
                break          # apres l'unite : parametres de mise en forme
            if re.fullmatch(r"[-+]?\d[\d,]*\.?\d*", x):
                vals.append(x)
            elif x in ("/", "x", "×", "-", "to", "or", "and", "by"):
                vals.append("×" if x in ("x", "×") else ("/" if x == "/" else "-"))
            else:
                unite = x
        return (" ".join(vals) + (" " + unite if unite else "")).strip()
    s = re.sub(r"\{\{\s*(?:convert|cvt)\s*\|([^{}]*)\}\}", _conv, s, flags=re.I)
    # les sauts de ligne separent des valeurs distinctes : garder un separateur
    s = re.sub(r"<\s*br\s*/?\s*>|\{\{\s*(?:br|-)\s*\}\}", " / ", s, flags=re.I)
    s = re.sub(r"\n+", " / ", s)
    s = re.sub(r"\{\{[^{}]*\}\}", "", s)
    s = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]|]*)\]\]", r"\1", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("&nbsp;", " ").replace("&ndash;", "–")
    s = s.replace("&mdash;", "—").replace("&amp;", "&")
    s = re.sub(r"'{2,}", "", s)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"(?:\s*/\s*){2,}", " / ", s)
    return s.strip(" ,;:/")

def years(prod):
    if not prod:
        return (None, None, "")
    t = strip_wiki(prod)
    ys = [int(y) for y in re.findall(r"\b(1[89]\d{2}|20[0-2]\d)\b", t)]
    if not ys:
        return (None, None, t)
    deb = min(ys)
    # "Since 2019" / "depuis 2019" : production ouverte au meme titre que
    # "2019-present". Sans ce marqueur, un seul millesime trouve se refermait
    # a tort la meme annee (bug touchant 28 modeles bien vivants, dont la
    # Yamaha Tenere 700 et le Ducati DesertX).
    ouvert = re.search(r"present|current|onwards?|since|depuis|[–—-]\s*$", t, re.I)
    fin = None if ouvert else max(ys)
    return (deb, fin, t)

def categorie(cls, name, cats_article=None):
    """Categories Wikipedia d'abord (fiables), champ 'class' ensuite, nom en dernier."""
    if cats_article:
        s = set(cats_article)
        for nom_cat, lab in CAT_ARTICLE:
            if nom_cat in s:
                return lab
    src = (strip_wiki(cls) + " " + name).lower()
    for pat, lab in CATEGORIES:
        if re.search(pat, src):
            return lab
    return ""

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return re.sub(r"-{2,}", "-", s)

# ---------------------------------------------------------------- pipeline
titres = json.load(open(os.path.join(RAW, "titres.json"), encoding="utf-8"))
boxes = json.load(open(os.path.join(RAW, "infobox.json"), encoding="utf-8"))
_pc = os.path.join(RAW, "categories_articles.json")
CATS_ART = json.load(open(_pc, encoding="utf-8")) if os.path.exists(_pc) else {}

rows = []
for titre, rec in boxes.items():
    it = (rec.get("infobox_type") or "").lower()
    if it != "motorcycle":
        continue
    c = rec["champs"]
    meta = titres.get(titre, {"marques": [], "pays": [], "annees": []})

    marque = ""
    for m in meta.get("marques", []):
        if m in MARQUES:
            marque = m
            break
    if not marque and meta.get("marques"):
        marque = meta["marques"][0]
    if not marque:
        mm = strip_wiki(c.get("manufacturer", ""))
        for k in MARQUES:
            if k.lower() in mm.lower():
                marque = k
                break
    pays, ecole = MARQUES.get(marque, ("", ""))

    deb, fin, prod_raw = years(c.get("production"))
    eng = c.get("engine", "")
    cyl = extract(eng, "vol", prefer={"cc", "cm3", "ccm"})
    pw_kw = extract(c.get("power", ""), "pwr")
    wet = extract(c.get("wet_weight", ""), "mass", prefer={"kg"})
    dry = extract(c.get("dry_weight", ""), "mass", prefer={"kg"})
    poids = wet or dry
    poids_type = "tous pleins faits" if wet else ("à sec" if dry else "")

    # Permis A2 (France) : <= 35 kW ET rapport <= 0.2 kW/kg
    a2, a2_note = "", ""
    if pw_kw is not None:
        if pw_kw > 35:
            a2, a2_note = "non", "puissance > 35 kW"
        elif poids:
            r = pw_kw / poids
            if r <= 0.2:
                a2, a2_note = "oui", "%.1f kW, %.3f kW/kg" % (pw_kw, r)
            else:
                a2, a2_note = "non", "rapport %.3f kW/kg > 0.2" % r
        else:
            a2, a2_note = "à vérifier", "poids inconnu"

    low = (strip_wiki(eng) + " " + titre).lower()
    arch = next((a for p, a in ARCHS if re.search(p, low)), "")
    if re.search(r"liquid.?cool|water.?cool", low):
        refr = "Liquide"
    elif re.search(r"oil.?cool", low):
        refr = "Air/huile"
    elif re.search(r"air.?cool", low):
        refr = "Air"
    else:
        refr = ""

    reservoir_ml = extract(c.get("fuel_capacity", ""), "vol", prefer={"l", "litre"})

    r = {
     "modele_id": slug(titre),
     "titre_wikipedia": titre,
     "marque": marque,
     "marque_id": slug(marque) if marque else "",
     "modele": strip_wiki(c.get("name", "")) or titre,
     "pays_origine": pays,
     "ecole": ecole,
     "categorie": categorie(c.get("class", ""), titre, CATS_ART.get(titre)),
     "annee_debut": deb,
     "annee_fin": fin,
     "production_raw": prod_raw,
     "cylindree_cc": cyl,
     "architecture": arch,
     "refroidissement": refr,
     "puissance_kw": pw_kw,
     "puissance_ch": round(pw_kw / 0.735499, 1) if pw_kw else None,
     "puissance_tr_min": rpm_of(c.get("power", "")),
     "couple_nm": extract(c.get("torque", ""), "trq", prefer={"nm", "n·m", "n.m"}),
     "couple_tr_min": rpm_of(c.get("torque", "")),
     "poids_kg": poids,
     "poids_type": poids_type,
     "poids_sec_kg": dry,
     "poids_tous_pleins_kg": wet,
     "hauteur_selle_mm": extract(c.get("seat_height", ""), "len", prefer={"mm"}),
     "empattement_mm": extract(c.get("wheelbase", ""), "len", prefer={"mm"}),
     "longueur_mm": extract(c.get("length", ""), "len", prefer={"mm"}),
     "largeur_mm": extract(c.get("width", ""), "len", prefer={"mm"}),
     "hauteur_mm": extract(c.get("height", ""), "len", prefer={"mm"}),
     "reservoir_l": round(reservoir_ml / 1000, 1) if reservoir_ml else None,
     "vitesse_max_kmh": extract(c.get("top_speed", ""), "spd", prefer={"km/h", "kmh", "kph"}),
     "a2_compatible": a2,
     "a2_detail": a2_note,
     "moteur": strip_wiki(eng)[:300],
     "transmission": strip_wiki(c.get("transmission", ""))[:200],
     "cadre": strip_wiki(c.get("frame", ""))[:200],
     "suspension": strip_wiki(c.get("suspension", ""))[:250],
     "freins": strip_wiki(c.get("brakes", ""))[:200],
     "pneus": strip_wiki(c.get("tires", ""))[:200],
     "alesage_course": strip_wiki(c.get("bore_stroke", ""))[:120],
     "compression": strip_wiki(c.get("compression", ""))[:80],
     "consommation": strip_wiki(c.get("fuel_consumption", ""))[:120],
     "predecesseur": strip_wiki(c.get("predecessor", ""))[:150],
     "successeur": strip_wiki(c.get("successor", ""))[:150],
     "aussi_appele": strip_wiki(c.get("aka", ""))[:150],
     "image_url": rec.get("image") or "",
     "wikidata_id": rec.get("wikidata") or "",
     "url_wikipedia": "https://en.wikipedia.org/wiki/" + titre.replace(" ", "_"),
     "source": "Wikipedia EN (CC BY-SA 4.0)",
    }
    KEY = ["cylindree_cc", "puissance_kw", "couple_nm", "poids_kg", "hauteur_selle_mm",
           "empattement_mm", "reservoir_l", "vitesse_max_kmh", "categorie", "annee_debut",
           "architecture", "transmission", "freins", "pneus", "image_url"]
    r["completude_pct"] = round(100 * sum(1 for k in KEY if r.get(k) not in (None, "", 0)) / len(KEY))
    rows.append(r)

rows.sort(key=lambda x: (-x["completude_pct"], x["marque"], x["modele"]))
json.dump(rows, open(os.path.join(RAW, "normalise.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("=== %d modeles normalises ===\n" % len(rows))

def pc(k):
    n = sum(1 for r in rows if r.get(k) not in (None, "", 0))
    return "%5d (%3d%%)" % (n, 100 * n // len(rows))

for k in ["marque", "ecole", "categorie", "annee_debut", "cylindree_cc", "puissance_kw",
          "couple_nm", "poids_kg", "hauteur_selle_mm", "empattement_mm", "reservoir_l",
          "vitesse_max_kmh", "a2_compatible", "image_url", "architecture"]:
    print("  %-22s %s" % (k, pc(k)))

print("\n  completude moyenne : %.0f%%" % (sum(r["completude_pct"] for r in rows) / len(rows)))
print("\nECOLES :")
for k, v in Counter(r["ecole"] for r in rows if r["ecole"]).most_common():
    print("   %5d  %s" % (v, k))
print("\nCATEGORIES :")
for k, v in Counter(r["categorie"] for r in rows if r["categorie"]).most_common():
    print("   %5d  %s" % (v, k))
print("\nA2 :")
for k, v in Counter(r["a2_compatible"] for r in rows if r["a2_compatible"]).most_common():
    print("   %5d  %s" % (v, k))
