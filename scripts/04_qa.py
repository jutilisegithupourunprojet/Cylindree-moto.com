# -*- coding: utf-8 -*-
"""
Etape 4 : controle qualite.
1) Verification contre des valeurs connues (verite terrain saisie a la main).
2) Detection des valeurs aberrantes -> champ 'alertes' + mise a blanc des impossibles.
Sortie : data/raw/normalise_qa.json
"""
import json, os

RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
rows = json.load(open(os.path.join(RAW, "normalise.json"), encoding="utf-8"))
by_title = {r["titre_wikipedia"]: r for r in rows}

# ------------------------------------------------ 1. verite terrain
# valeurs de reference verifiees manuellement (fiches constructeur)
TRUTH = {
 "Yamaha MT-07":     {"cylindree_cc": 689,  "poids_kg": 184, "puissance_ch": 74.8},
 "Kawasaki Z650":    {"cylindree_cc": 649,  "puissance_ch": 68},
 "Suzuki SV650":     {"cylindree_cc": 645,  "puissance_ch": 76},
 "BMW R1250GS":      {"cylindree_cc": 1254, "puissance_ch": 136},
 "Yamaha YZF-R1":    {"cylindree_cc": 998},
 "Honda CB500F":     {"cylindree_cc": 471,  "puissance_ch": 47},
 "Ducati Monster":   {"cylindree_cc": 937},
 "KTM 390 Duke":     {"cylindree_cc": 373},
 "Honda CBR600RR":   {"cylindree_cc": 599},
 "Kawasaki Ninja 400": {"cylindree_cc": 399},
}

print("=" * 74)
print("1. CONTROLE CONTRE VALEURS CONNUES")
print("=" * 74)
ok = bad = absent = 0
for titre, exp in TRUTH.items():
    r = by_title.get(titre)
    if not r:
        print("  %-22s ABSENT de la base" % titre)
        absent += 1
        continue
    for champ, attendu in exp.items():
        got = r.get(champ)
        if got is None:
            print("  %-22s %-14s attendu %-8s -> VIDE" % (titre, champ, attendu))
            continue
        ecart = abs(got - attendu) / attendu * 100
        flag = "OK " if ecart <= 6 else "ECART"
        if ecart <= 6:
            ok += 1
        else:
            bad += 1
        print("  %-22s %-14s attendu %-8s obtenu %-8s %s (%.1f%%)"
              % (titre, champ, attendu, got, flag, ecart))
print("\n  -> %d conformes, %d ecarts, %d modeles absents" % (ok, bad, absent))

# ------------------------------------------------ 2. bornes de plausibilite
BORNES = {
 "cylindree_cc":     (30, 2500,   "cylindree"),
 "puissance_ch":     (1, 320,     "puissance"),
 "puissance_kw":     (0.5, 240,   "puissance kW"),
 "couple_nm":        (2, 250,     "couple"),
 "poids_kg":         (30, 500,    "poids"),
 "hauteur_selle_mm": (500, 1000,  "hauteur de selle"),
 "empattement_mm":   (900, 1900,  "empattement"),
 "longueur_mm":      (1300, 2800, "longueur"),
 "largeur_mm":       (400, 1200,  "largeur"),
 "hauteur_mm":       (700, 1700,  "hauteur"),
 "reservoir_l":      (2, 40,      "reservoir"),
 "vitesse_max_kmh":  (25, 400,    "vitesse max"),
}

print("\n" + "=" * 74)
print("2. VALEURS ABERRANTES")
print("=" * 74)
compte = {}
for r in rows:
    alertes = []
    for champ, (lo, hi, lib) in BORNES.items():
        v = r.get(champ)
        if v is None or v == "":
            continue
        if not (lo <= v <= hi):
            alertes.append("%s=%s hors [%s-%s]" % (champ, v, lo, hi))
            compte[lib] = compte.get(lib, 0) + 1
            r[champ] = None          # on efface plutot que de publier un chiffre faux
    # coherence interne
    if r.get("poids_sec_kg") and r.get("poids_tous_pleins_kg"):
        if r["poids_sec_kg"] > r["poids_tous_pleins_kg"]:
            alertes.append("poids sec > poids tous pleins")
            compte["coherence poids"] = compte.get("coherence poids", 0) + 1
    if r.get("annee_debut") and r.get("annee_fin"):
        if r["annee_fin"] < r["annee_debut"]:
            alertes.append("annee_fin < annee_debut")
            r["annee_fin"] = None
            compte["coherence annees"] = compte.get("coherence annees", 0) + 1
    r["alertes"] = " ; ".join(alertes)

for lib, n in sorted(compte.items(), key=lambda x: -x[1]):
    print("  %-22s %4d valeurs effacees / signalees" % (lib, n))
tot = sum(compte.values())
print("\n  -> %d anomalies sur %d modeles (%.1f%%)" % (tot, len(rows), 100 * tot / max(1, len(rows))))

# ------------------------------------------------ 3. recalcul A2 apres nettoyage
maj = 0
for r in rows:
    pw, poids = r.get("puissance_kw"), r.get("poids_kg")
    avant = r.get("a2_compatible")
    if pw is None:
        r["a2_compatible"], r["a2_detail"] = "", ""
    elif pw > 35:
        r["a2_compatible"], r["a2_detail"] = "non", "puissance > 35 kW"
    elif poids:
        ratio = pw / poids
        if ratio <= 0.2:
            r["a2_compatible"] = "oui"
            r["a2_detail"] = "%.1f kW, %.3f kW/kg" % (pw, ratio)
        else:
            r["a2_compatible"] = "non"
            r["a2_detail"] = "rapport %.3f kW/kg > 0.2" % ratio
    else:
        r["a2_compatible"], r["a2_detail"] = "à vérifier", "poids inconnu"
    if avant != r["a2_compatible"]:
        maj += 1

# recalcul completude
KEY = ["cylindree_cc", "puissance_kw", "couple_nm", "poids_kg", "hauteur_selle_mm",
       "empattement_mm", "reservoir_l", "vitesse_max_kmh", "categorie", "annee_debut",
       "architecture", "transmission", "freins", "pneus", "image_url"]
for r in rows:
    r["completude_pct"] = round(100 * sum(1 for k in KEY if r.get(k) not in (None, "", 0)) / len(KEY))

rows.sort(key=lambda x: (-x["completude_pct"], x["marque"] or "zz", x["modele"]))
json.dump(rows, open(os.path.join(RAW, "normalise_qa.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("  -> %d statuts A2 recalcules apres nettoyage" % maj)
print("\n" + "=" * 74)
print("3. REPARTITION PAR COMPLETUDE")
print("=" * 74)
for seuil in [90, 80, 70, 60, 50, 40]:
    n = sum(1 for r in rows if r["completude_pct"] >= seuil)
    print("  >= %2d%% de champs remplis : %4d modeles" % (seuil, n))
print("\n  completude moyenne apres QA : %.0f%%"
      % (sum(r["completude_pct"] for r in rows) / len(rows)))
