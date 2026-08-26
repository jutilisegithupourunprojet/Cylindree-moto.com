# -*- coding: utf-8 -*-
"""
Etape 16 : integration des fiches saisies a la main.

Transforme scripts/specs_manuelles.py au schema de la base, calcule les champs
derives (kW, poids retenu, A2, complétude) et cherche une image libre sur
Wikimedia Commons quand il en existe une.

Sortie : data/raw/modeles_manuels.json
"""
import json, os, re, sys, time, unicodedata
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
_n = import_module("03_normalise")
MARQUES, slug = _n.MARQUES, _n.slug
from specs_manuelles import MODELES, DATE_SAISIE

COM = "https://commons.wikimedia.org/w/api.php"
S = requests.Session()
S.headers.update({"User-Agent": "MotoDirectoryResearch/0.1 (viktordu84@gmail.com)"})
RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
LIBRES = ("cc by", "cc0", "public domain", "attribution")


def get(params, tries=4):
    d = 0.4
    for _ in range(tries):
        try:
            r = S.get(COM, params=params, timeout=45)
            if r.status_code == 200 and r.text.lstrip().startswith("{"):
                return r.json()
        except Exception:
            pass
        time.sleep(d); d *= 2
    return None


def clean(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", str(s or ""))).strip()


def image_commons(nom, annee=None):
    """Cherche une photo libre du modele sur Commons. Aucune si rien de sur.

    Un nom de modele peut avoir ete reutilise a des decennies d'ecart : la
    recherche 'Kawasaki Ninja 500' remontait une EX-500 de 2009 pour le modele
    2024. On rejette donc tout fichier date de plus de trois ans avant le
    lancement.
    """
    j = get({"action": "query", "generator": "search", "gsrsearch": nom,
             "gsrnamespace": "6", "gsrlimit": "4", "prop": "imageinfo",
             "iiprop": "extmetadata|url", "iiurlwidth": "800",
             "format": "json", "formatversion": "2"})
    if not j:
        return None
    mots = [m for m in re.split(r"[^a-z0-9]+", nom.lower()) if len(m) > 2]
    for p in j.get("query", {}).get("pages", []):
        titre = p["title"].lower()
        # le nom du fichier doit contenir la marque ET un element du modele
        if not all(any(m in titre for m in mots[i:i+1]) for i in (0,)):
            continue
        if sum(1 for m in mots if m in titre) < max(2, len(mots) - 1):
            continue
        if not re.search(r"\.(jpe?g|png)$", titre):
            continue
        if annee:
            an_fichier = [int(y) for y in re.findall(r"\b(19\d{2}|20[0-2]\d)\b", titre)]
            if an_fichier and max(an_fichier) < int(annee) - 3:
                continue
        ii = (p.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata", {}) or {}
        lic = clean((em.get("LicenseShortName", {}) or {}).get("value", ""))
        ll = lic.lower()
        if not lic or not any(x in ll for x in LIBRES) or "free use" in ll:
            continue
        return {"image_url": (ii.get("url") or "").split("?")[0],
                "image_vignette": (ii.get("thumburl") or "").split("?")[0],
                "image_licence": lic,
                "image_auteur": clean((em.get("Artist", {}) or {}).get("value", ""))[:120],
                "image_page": ii.get("descriptionurl", ""),
                "image_utilisable": "oui"}
    return None


rows = []
print("%d fiches saisies a la main" % len(MODELES))
for m in MODELES:
    nom = m["nom"]
    marque = m["marque"]
    pays, ecole = MARQUES.get(marque, ("", ""))
    r = {
     "modele_id": m.get("id") or slug(nom), "titre_wikipedia": nom,
     "marque": marque, "marque_id": slug(marque),
     "modele": nom, "nom_fr": nom, "titre_fr": nom,
     "pays_origine": pays, "ecole": ecole,
     "source": "Saisie manuelle, fiche constructeur (%s)" % DATE_SAISIE,
     "url_wikipedia": m["source"], "url_wikipedia_fr": m["source"],
     "source_specs_fr": m["source"],
     "saisie_manuelle": True,
     "a_version_fr": "oui", "nb_langues": 1, "nb_langues_euro": 1,
     "vues_60j": 0, "alertes": "",
    }
    for k in ("annee_debut", "annee_fin", "categorie", "cylindree_cc",
              "architecture", "refroidissement", "puissance_ch", "puissance_kw",
              "puissance_tr_min", "couple_nm", "couple_tr_min",
              "poids_sec_kg", "poids_tous_pleins_kg", "hauteur_selle_mm",
              "empattement_mm", "reservoir_l", "vitesse_max_kmh",
              "prix_lancement_eur", "cadre", "suspension", "freins", "pneus",
              "transmission", "moteur", "consommation"):
        if m.get(k) not in (None, ""):
            r[k] = m[k]

    if r.get("prix_lancement_eur"):
        r["prix_source"] = "Tarif constructeur France relevé le %s" % DATE_SAISIE
    if r.get("puissance_ch") and not r.get("puissance_kw"):
        r["puissance_kw"] = round(float(r["puissance_ch"]) * 0.735499, 2)
    r["poids_kg"] = r.get("poids_tous_pleins_kg") or r.get("poids_sec_kg") or ""
    r["poids_type"] = ("tous pleins faits" if r.get("poids_tous_pleins_kg")
                       else ("à sec" if r.get("poids_sec_kg") else ""))

    # statut A2 : calcule, puis complete par l'information constructeur
    pw, poids = r.get("puissance_kw"), r.get("poids_kg")
    dispo = (m.get("a2") or "").lower()
    if pw and pw <= 35 and poids and pw / float(poids) <= 0.2:
        r["a2_compatible"], r["a2_detail"] = "oui", "%.1f kW, %.3f kW/kg" % (pw, pw / float(poids))
    elif "bridée" in dispo or "a2 disponible" in dispo:
        r["a2_compatible"] = "oui"
        r["a2_detail"] = "version A2 homologuée proposée au catalogue"
    elif "compatible a2" in dispo:
        r["a2_compatible"], r["a2_detail"] = "oui", "compatible sans bridage"
    elif dispo == "non":
        r["a2_compatible"], r["a2_detail"] = "non", "aucune version A2"
    else:
        r["a2_compatible"], r["a2_detail"] = "à vérifier", clean(m.get("a2", ""))
    if m.get("note"):
        base = r["a2_detail"].strip()
        if base and not base.endswith((".", "!", "?")):
            base += "."
        r["a2_detail"] = (base + " " + m["note"]).strip()

    img = image_commons(nom, m.get("annee_debut"))
    if img:
        r.update(img)
    else:
        r.update({"image_url": "", "image_vignette": "", "image_licence": "",
                  "image_auteur": "", "image_page": "", "image_utilisable": "inconnu"})
    print("   %-30s %s" % (nom[:30], "image trouvée" if img else "pas d'image libre"))
    time.sleep(0.2)

    KEY = ["cylindree_cc", "puissance_kw", "couple_nm", "poids_kg", "hauteur_selle_mm",
           "empattement_mm", "reservoir_l", "vitesse_max_kmh", "categorie",
           "annee_debut", "architecture", "transmission", "freins", "pneus", "image_url"]
    r["completude_pct"] = round(100 * sum(1 for k in KEY if r.get(k)) / len(KEY))
    rows.append(r)

json.dump(rows, open(os.path.join(RAW, "modeles_manuels.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("\n=== %d fiches manuelles pretes ===" % len(rows))
print("   completude moyenne : %.0f%%" % (sum(r["completude_pct"] for r in rows) / len(rows)))
print("   avec image libre   : %d" % sum(1 for r in rows if r["image_utilisable"] == "oui"))
print("   avec prix          : %d" % sum(1 for r in rows if r.get("prix_lancement_eur")))
print("   compatibles A2     : %d" % sum(1 for r in rows if r["a2_compatible"] == "oui"))
