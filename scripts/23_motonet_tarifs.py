# -*- coding: utf-8 -*-
"""
Etape 23 : tarifs France publies par moto-net.com, une page par marque.

moto-net.com/tarifs/<marque> liste, pour chaque modele, l'annee et le prix maximum
conseille. robots.txt : /tarifs/ n'est pas interdit ; delai de 10 s respecte ; le
robot s'identifie et s'arrete sur une reponse 403/429.

Sortie : data/raw/motonet_tarifs.json  {marque: [{"nom", "an", "prix", "variante"}]}
06_export.py ne s'en sert que pour remplir un prix VIDE, sur correspondance exacte
du nom de base (jamais une variante : Y-AMT, SP, Tech Max...).
"""
import html, json, os, re, sys, time
import requests

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw")
F = os.path.join(RAW, "motonet_tarifs.json")
S = requests.Session()
S.headers.update({"User-Agent": "CylindreeBot/0.1 (+https://www.cylindree-moto.com; viktordu84@gmail.com)"})


def get(url):
    time.sleep(10.5)
    r = S.get(url, timeout=60)
    if r.status_code in (403, 429):
        sys.exit("ARRET : HTTP %d sur %s" % (r.status_code, url))
    r.raise_for_status()
    return r.content.decode("utf-8", errors="ignore")


def parse(page):
    out = []
    for li in re.findall(r"<li>(.*?)</li>", page, flags=re.S):
        t = html.unescape(re.sub(r"<[^>]+>", " ", li))
        t = re.sub(r"[\s\xa0 ]+", " ", t).strip()
        # l'annee entre parentheses est facultative selon les marques ("R 1300 GS : 21 300 euros")
        m = re.match(r"^(.+?)\s*(?:\(\s*((?:19|20)\d\d)\s*\))?\s*:\s*([\d ]+?)\s*euros?\b(.*)$", t, re.I)
        if not m:
            continue
        prix = int(re.sub(r"\D", "", m.group(3)) or 0)
        if prix < 500:
            continue
        out.append({"nom": m.group(1).strip(), "an": int(m.group(2)) if m.group(2) else 0, "prix": prix,
                    "note": m.group(4).strip()[:60]})
    return out


def main():
    data = {}
    if os.path.exists(F):
        data = json.load(open(F, encoding="utf-8"))
    index = get("https://moto-net.com/tarifs")
    marques = sorted(set(re.findall(r'href="(?:https?://(?:www\.)?moto-net\.com)?/tarifs/([a-z0-9\-]+)"', index)))
    print("%d marques dans l'index : %s" % (len(marques), ", ".join(marques)), flush=True)
    for i, mq in enumerate(marques, 1):
        if data.get(mq):
            continue
        page = get("https://moto-net.com/tarifs/" + mq)
        data[mq] = parse(page)
        data["_date"] = time.strftime("%Y-%m-%d")
        json.dump(data, open(F, "w", encoding="utf-8"), ensure_ascii=False)
        print("[%d/%d] %s : %d tarifs" % (i, len(marques), mq, len(data[mq])), flush=True)
    print("TERMINE", flush=True)


if __name__ == "__main__":
    main()
