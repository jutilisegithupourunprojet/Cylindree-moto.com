# -*- coding: utf-8 -*-
"""
Etape 15 : dedoublonnage et enrichissement des modeles collectes en FR.

  - ecarte ceux deja presents via la collecte anglophone ;
  - recupere licence, auteur et vignette de l'image (Commons) ;
  - recupere l'audience Wikipedia FR (60 jours) pour le scoring editorial.

Sortie : data/raw/modeles_fr_pret.json
"""
import requests, json, os, re, time

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


def clean(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", str(s or ""))).strip()


def norm(f):
    return (f or "").replace("_", " ").strip()


rows = json.load(open(os.path.join(RAW, "modeles_fr.json"), encoding="utf-8"))
enr = json.load(open(os.path.join(RAW, "enrichissement.json"), encoding="utf-8"))
base = json.load(open(os.path.join(RAW, "normalise_qa.json"), encoding="utf-8"))

# --- 1. dedoublonnage ----------------------------------------------------
deja_fr = {v["titre_fr"] for v in enr.values() if v.get("titre_fr")}
ids_base = {r["modele_id"] for r in base}
avant = len(rows)
rows = [r for r in rows
        if r["titre_wikipedia"] not in deja_fr and r["modele_id"] not in ids_base]
print("dedoublonnage : %d -> %d (%d deja couverts)" % (avant, len(rows), avant - len(rows)))

# --- 2. images -----------------------------------------------------------
print("\nLicences et vignettes...")
fichiers = {}
for r in rows:
    if r.get("image_fichier"):
        fichiers.setdefault(norm(r["image_fichier"]), []).append(r["modele_id"])
par_id = {r["modele_id"]: r for r in rows}
print("   %d fichiers" % len(fichiers))

LIBRES = ("cc by", "cc0", "public domain", "attribution")
fl = sorted(fichiers)
n_ok = 0
for i in range(0, len(fl), 10):
    lot = fl[i:i+10]
    j = get(COM, {"action": "query", "prop": "imageinfo",
                  "iiprop": "extmetadata|url", "iiurlwidth": "800",
                  "titles": "|".join(lot), "format": "json", "formatversion": "2"})
    if not j:
        continue
    q = j.get("query", {})
    normd = {x["to"]: x["from"] for x in q.get("normalized", [])}
    for p in q.get("pages", []):
        if p.get("missing"):
            continue
        ii = (p.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata", {}) or {}
        lic = clean((em.get("LicenseShortName", {}) or {}).get("value", ""))
        if not lic:
            continue
        cles = {norm(p["title"])}
        if p["title"] in normd:
            cles.add(norm(normd[p["title"]]))
        for c in cles:
            for mid in fichiers.get(c, []):
                m = par_id[mid]
                m["image_licence"] = lic
                m["image_auteur"] = clean((em.get("Artist", {}) or {}).get("value", ""))[:120]
                m["image_page"] = ii.get("descriptionurl", "")
                m["image_vignette"] = (ii.get("thumburl") or "").split("?")[0]
                ll = lic.lower()
                m["image_utilisable"] = ("oui" if any(s in ll for s in LIBRES)
                                         and "free use" not in ll else "verifier")
                n_ok += 1
    if (i // 10) % 15 == 0:
        print("   %d/%d  (%d ok)" % (i + len(lot), len(fl), n_ok))
    time.sleep(0.13)
print("   -> %d images documentees" % n_ok)

# --- 3. audience ---------------------------------------------------------
print("\nAudience Wikipedia FR...")
titres = [r["titre_wikipedia"] for r in rows]
par_titre = {r["titre_wikipedia"]: r for r in rows}
for i in range(0, len(titres), 20):
    lot = titres[i:i+20]
    j = get(FR, {"action": "query", "prop": "pageviews|langlinks",
                 "pvipdays": "60", "lllang": "en", "lllimit": "max",
                 "titles": "|".join(lot), "format": "json", "formatversion": "2"})
    if not j:
        continue
    for p in j.get("query", {}).get("pages", []):
        r = par_titre.get(p["title"])
        if not r:
            continue
        pv = p.get("pageviews") or {}
        vues = [v for v in pv.values() if isinstance(v, int)]
        r["vues_60j"] = sum(vues)
        r["a_version_fr"] = "oui"          # article FR par construction
        r["nb_langues"] = 1 + len(p.get("langlinks", []))
        r["nb_langues_euro"] = 1
    time.sleep(0.12)

# --- 4. champs manquants au schema --------------------------------------
for r in rows:
    r.setdefault("vues_60j", 0)
    r.setdefault("a_version_fr", "oui")
    r.setdefault("nb_langues", 1)
    r.setdefault("nb_langues_euro", 1)
    r.setdefault("image_url", "")
    r.setdefault("image_vignette", r.get("image_url", ""))
    r.setdefault("image_licence", "")
    r.setdefault("image_auteur", "")
    r.setdefault("image_page", "")
    r.setdefault("image_utilisable", "inconnu")
    r.setdefault("titre_fr", r["titre_wikipedia"])
    r.setdefault("url_wikipedia_fr", r["url_wikipedia"])
    r.setdefault("nom_fr", r.get("modele", ""))
    for k in ("type_fr", "resume_fr", "prix_source", "alesage_course", "compression",
              "consommation", "predecesseur", "successeur", "aussi_appele",
              "source_specs_fr", "annee_fin", "longueur_mm", "largeur_mm",
              "hauteur_mm", "couple_nm", "couple_tr_min", "puissance_tr_min",
              "poids_sec_kg", "poids_tous_pleins_kg", "wikidata_id",
              "prix_lancement_eur", "cadre", "suspension", "freins", "pneus",
              "transmission", "moteur"):
        r.setdefault(k, "")

json.dump(rows, open(os.path.join(RAW, "modeles_fr_pret.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("\n=== %d modeles prets a fusionner ===" % len(rows))
print("   avec image utilisable : %d" % sum(1 for r in rows if r["image_utilisable"] == "oui"))
print("   avec prix             : %d" % sum(1 for r in rows if r.get("prix_lancement_eur")))
print("   completude >= 45%%     : %d" % sum(1 for r in rows if r["completude_pct"] >= 45))
top = sorted(rows, key=lambda x: -x["vues_60j"])[:12]
print("\nLES PLUS CONSULTES :")
for r in top:
    print("   %6d vues  %-34s %3d%%" % (r["vues_60j"], r["titre_wikipedia"][:34],
                                        r["completude_pct"]))
