# -*- coding: utf-8 -*-
"""
Etape 12 : URL de vignettes.
Les fiches pointaient vers les fichiers ORIGINAUX de Wikimedia (jusqu'a 1 Mo
chacun). Wikimedia refuse les largeurs arbitraires construites a la main
(HTTP 400) : seule l'API fournit une URL de vignette valide.
Sortie : enrichit data/raw/enrichissement.json (champ image_vignette)
"""
import requests, json, time, os

COM = "https://commons.wikimedia.org/w/api.php"
EN = "https://en.wikipedia.org/w/api.php"
S = requests.Session()
S.headers.update({"User-Agent": "MotoDirectoryResearch/0.1 (viktordu84@gmail.com)"})
RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
LARGEUR = 800

def get(url, params, tries=5):
    d = 0.5
    for _ in range(tries):
        try:
            r = S.get(url, params=params, timeout=60)
            if r.status_code == 200 and r.text.lstrip().startswith("{"):
                return r.json()
        except Exception:
            pass
        time.sleep(d); d *= 2
    return None

def propre(u):
    return u.split("?")[0] if u else ""

enr = json.load(open(os.path.join(RAW, "enrichissement.json"), encoding="utf-8"))

# fichiers a traiter, regroupes par nom de fichier
fichiers = {}
for titre, v in enr.items():
    f = v.get("image_fichier")
    if f:
        fichiers.setdefault(f, []).append(titre)
print("%d fichiers image a vignetter" % len(fichiers))

noms = sorted(fichiers)
ok = 0
restants = []
# la generation de vignettes est couteuse : petits lots obligatoires
for source, url in (("Commons", COM), ("Wikipedia EN", EN)):
    cibles = noms if source == "Commons" else restants
    if not cibles:
        continue
    print("\n%s : %d fichiers" % (source, len(cibles)))
    manques = []
    for i in range(0, len(cibles), 10):
        lot = cibles[i:i+10]
        j = get(url, {"action": "query", "prop": "imageinfo",
                      "iiprop": "url|size", "iiurlwidth": str(LARGEUR),
                      "titles": "|".join(lot), "format": "json",
                      "formatversion": "2"})
        if not j:
            manques += lot
            continue
        q = j.get("query", {})
        norm = {x["to"]: x["from"] for x in q.get("normalized", [])}
        for p in q.get("pages", []):
            if p.get("missing"):
                manques.append(p["title"])
                continue
            ii = (p.get("imageinfo") or [{}])[0]
            th = propre(ii.get("thumburl"))
            if not th:
                manques.append(p["title"])
                continue
            cles = {p["title"]}
            if p["title"] in norm:
                cles.add(norm[p["title"]])
            for c in cles:
                for t in fichiers.get(c, []):
                    enr[t]["image_vignette"] = th
                    enr[t]["image_largeur"] = ii.get("thumbwidth") or LARGEUR
                    enr[t]["image_hauteur"] = ii.get("thumbheight") or ""
                    ok += 1
        if (i // 10) % 20 == 0:
            print("   %d/%d  (%d ok)" % (i + len(lot), len(cibles), ok))
        time.sleep(0.15)
    restants = manques
    print("   -> %d vignettes, %d fichiers restants" % (ok, len(restants)))

json.dump(enr, open(os.path.join(RAW, "enrichissement.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

n = sum(1 for v in enr.values() if v.get("image_vignette"))
print("\n=== %d / %d modeles avec vignette (%d%%) ==="
      % (n, len(enr), 100 * n // len(enr)))
sans = [t for t, v in enr.items() if v.get("image_fichier") and not v.get("image_vignette")]
if sans:
    print("%d fichiers sans vignette (l'original sera utilise) :" % len(sans))
    for t in sans[:5]:
        print("   ", t)
