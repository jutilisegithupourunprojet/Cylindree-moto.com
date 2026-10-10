# -*- coding: utf-8 -*-
"""
Etape 21 : releve des prix d'occasion affiches sur les pages publiques de
Motoplanete (marque, categorie, departement).

Respecte le robots.txt du site : seules les pages listees dans son sitemap sont
lues, jamais /ajax/*, avec le delai de 10 s demande (Crawl-delay). Le robot
s'identifie et s'arrete sur toute reponse 403/429 (jamais de contournement).
Le script est reprenable : les pages deja lues sont conservees dans le cache.

Sortie : data/raw/occasion_motoplanete.json (annonces dedoublonnees par identifiant).
Seuls des agregats (nombre, fourchette, mediane) sont ensuite publies par 20_site.py.
"""
import json, os, re, sys, time
import requests

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw")
CACHE = os.path.join(BASE, "occasion_motoplanete.json")
HOTE = "https://www.motoplanete.com"
DELAI = 10.5
S = requests.Session()
S.headers.update({"User-Agent": "CylindreeBot/0.1 (+https://www.cylindree-moto.com; viktordu84@gmail.com)"})


def pause():
    time.sleep(DELAI)


def pages_a_lire():
    r = S.get(HOTE + "/sitemap.php", timeout=60)
    r.raise_for_status()
    urls = re.findall(r"<loc>([^<]+)</loc>", r.text)
    return [u for u in urls if "/occasion/list/" in u or re.search(r"/occasion_[^/]+/\d+_\d+/?$", u)]


def lignes(html):
    out = []
    for tr in re.findall(r'<tr class="tr">(.*?)</tr>', html, flags=re.S):
        m = re.search(r'/occasion-moto/(\d+)/', tr)
        c = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).replace("&nbsp;", "").strip()
             for x in re.findall(r"<td[^>]*>(.*?)</td>", tr, flags=re.S)]
        if not m or len(c) < 6:
            continue
        titre, cc, prix, km, date = c[1], c[2], c[3], c[4], c[5]
        p = re.sub(r"\D", "", prix)
        k = re.sub(r"\D", "", km)
        a = re.search(r"(?:19|20)\d\d", date)
        out.append({"id": m.group(1), "titre": titre,
                    "cc": int(re.sub(r"\D", "", cc) or 0),
                    "prix": int(p) if p else 0, "km": int(k) if k else 0,
                    "annee": int(a.group(0)) if a else 0})
    return out


def main():
    cache = {"lues": [], "annonces": {}, "date": time.strftime("%Y-%m-%d")}
    if os.path.exists(CACHE):
        cache = json.load(open(CACHE, encoding="utf-8"))
    urls = pages_a_lire()
    print("%d pages dans le sitemap, %d deja lues" % (len(urls), len(cache["lues"])), flush=True)
    for i, u in enumerate(urls, 1):
        if u in cache["lues"]:
            continue
        pause()
        try:
            r = S.get(u, timeout=45)
        except Exception as ex:
            print("erreur reseau", u, ex, flush=True)
            continue
        if r.status_code in (403, 429):
            print("ARRET : HTTP %d sur %s" % (r.status_code, u), flush=True)
            break
        if r.status_code != 200:
            print("ignoree HTTP %d : %s" % (r.status_code, u), flush=True)
            cache["lues"].append(u)
            continue
        # le contenu est servi en iso-8859-1 / cp1252
        r.encoding = r.apparent_encoding or "utf-8"
        rows = lignes(r.text)
        for a in rows:
            cache["annonces"][a["id"]] = a
        cache["lues"].append(u)
        cache["date"] = time.strftime("%Y-%m-%d")
        print("[%d/%d] %d lignes, %d annonces uniques : %s"
              % (i, len(urls), len(rows), len(cache["annonces"]), u.replace(HOTE, "")), flush=True)
        if len(cache["lues"]) % 10 == 0:
            json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)
    print("TERMINE : %d annonces uniques" % len(cache["annonces"]), flush=True)


if __name__ == "__main__":
    main()
