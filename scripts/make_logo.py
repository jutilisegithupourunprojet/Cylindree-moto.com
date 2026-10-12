# -*- coding: utf-8 -*-
"""
Logo et icones : le compte-tours de la page d'accueil, version simplifiee, sur fond
transparent (disque sombre cerne d'orange, graduations, zone rouge, aiguille).

Genere dans scripts/assets_source/ :
  logo-compteur.svg   source vectorielle, fond transparent (aussi utilisee en favicon SVG)
  favicon.png         192 x 192, fond transparent
  favicon-32.png      32 x 32, fond transparent
  apple-touch-icon.png 180 x 180, fond sombre OPAQUE (iOS remplit sinon la transparence en noir)

Usage : python make_logo.py
"""
import os
from math import cos, sin, radians
from PIL import Image, ImageDraw

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets_source")
ORANGE, ROUGE, CLAIR, FOND = "#ff7a33", "#ff4b1f", "#f3efe7", "#1a140d"
CX = CY = 100.0


def ang(v):
    """Angle (degres, repere ecran) de la valeur v du cadran 0-14 : 0 en bas a gauche, 14 en bas a droite."""
    return -135 + v * 270 / 14 - 90


def pt(v, r):
    a = radians(ang(v))
    return CX + r * cos(a), CY + r * sin(a)


def svg():
    p = []
    p.append('<circle cx="100" cy="100" r="96" fill="%s" stroke="%s" stroke-width="6"/>' % (FOND, ORANGE))
    ax, ay = pt(11, 80)
    bx, by = pt(14, 80)
    p.append('<path d="M%.1f %.1f A80 80 0 0 1 %.1f %.1f" fill="none" stroke="%s" stroke-width="7" '
             'stroke-linecap="round"/>' % (ax, ay, bx, by, ROUGE))
    for v in range(0, 15, 2):
        x1, y1 = pt(v, 68)
        x2, y2 = pt(v, 56)
        p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="6" '
                 'stroke-linecap="round"/>' % (x1, y1, x2, y2, ROUGE if v >= 12 else CLAIR))
    tx, ty = pt(9.2, 62)
    p.append('<line x1="100" y1="100" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="8" '
             'stroke-linecap="round"/>' % (tx, ty, ORANGE))
    p.append('<circle cx="100" cy="100" r="12" fill="%s" stroke="%s" stroke-width="5"/>' % (FOND, ORANGE))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">%s</svg>' % "".join(p))


def png(taille, fond=None, marge=0.0):
    """Rendu Pillow en sur-echantillonnage (anti-crenelage), transparent si fond est None."""
    S = 8
    N = taille * S
    im = Image.new("RGBA", (N, N), fond or (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    k = N * (1 - 2 * marge) / 200.0
    o = N * marge

    def X(x):
        return o + x * k

    def P(v, r):
        x, y = pt(v, r)
        return X(x), X(y)

    def rond(x, y, r, couleur):
        d.ellipse([x - r, y - r, x + r, y + r], fill=couleur)

    d.ellipse([X(4), X(4), X(196), X(196)], fill=ORANGE)
    d.ellipse([X(10), X(10), X(190), X(190)], fill=FOND)
    # zone rouge
    d.arc([X(20), X(20), X(180), X(180)], start=ang(11) % 360, end=ang(14) % 360,
          fill=ROUGE, width=int(7 * k))
    for v in (11, 14):
        x, y = P(v, 80)
        rond(x, y, 3.5 * k, ROUGE)
    for v in range(0, 15, 2):
        x1, y1 = P(v, 68)
        x2, y2 = P(v, 56)
        c = ROUGE if v >= 12 else CLAIR
        d.line([x1, y1, x2, y2], fill=c, width=int(6 * k))
        rond(x1, y1, 3 * k, c)
        rond(x2, y2, 3 * k, c)
    tx, ty = P(9.2, 62)
    d.line([X(100), X(100), tx, ty], fill=ORANGE, width=int(8 * k))
    rond(tx, ty, 4 * k, ORANGE)
    rond(X(100), X(100), 12 * k + 2.5 * k, ORANGE)
    rond(X(100), X(100), 12 * k - 2.5 * k, FOND)
    return im.resize((taille, taille), Image.LANCZOS)


if __name__ == "__main__":
    with open(os.path.join(DIR, "logo-compteur.svg"), "w", encoding="utf-8") as f:
        f.write(svg())
    png(192).save(os.path.join(DIR, "favicon.png"), optimize=True)
    png(32).save(os.path.join(DIR, "favicon-32.png"), optimize=True)
    png(180, fond=(20, 17, 12, 255), marge=0.1).convert("RGB").save(
        os.path.join(DIR, "apple-touch-icon.png"), optimize=True)
    print("logo genere")
