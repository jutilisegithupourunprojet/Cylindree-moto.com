# -*- coding: utf-8 -*-
"""
Generateur de site statique a partir de data/out/*.csv

Produit du HTML pur : pas de base de donnees, pas de serveur, pas de plugin.
Hebergeable gratuitement (Cloudflare Pages, Netlify) et parfait pour le SEO.

  site/index.html
  site/motos/<marque>/<modele>.html
  site/marques/<marque>.html
  site/ecoles/<ecole>.html
  site/categories/<slug>.html
  site/duels/<a>-vs-<b>.html
  site/comparateur.html
  site/assets/{style.css, comparateur.js, data.json}
  site/sitemap.xml, site/robots.txt
"""
import csv, io, json, os, re, html, unicodedata, shutil, sys, base64
from datetime import date
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guides_contenu import GUIDES as _G1, METHODE, DATE_MAJ
from guides_equipement import GUIDES_EQUIPEMENT as _G2
GUIDES = _G1 + _G2
from collections import defaultdict

BASE = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(BASE, "data", "out")
SITE = os.path.join(BASE, "site")

SITE_NOM = "Cylindrée"
SITE_URL = "https://www.cylindree-moto.com"       # cylindree-moto.com redirige (308) vers www, jamais l'inverse
GA_ID = "G-MNFQ3GT2YM"
ADSENSE_CLIENT = "ca-pub-6448509444467784"
SITE_DESC = ("Fiches techniques, comparateur et duels de motos. "
             "Caractéristiques vérifiées, compatibilité permis A2, "
             "écoles japonaise, italienne et américaine.")

# seuils de publication : mieux vaut peu de fiches completes que beaucoup de vides
MIN_COMPLETUDE = 45

# prefixe racine des URL (vide = site servi a la racine du domaine)
RACINE = ""


# ----------------------------------------------------------------- utilitaires
def slug(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return re.sub(r"-{2,}", "-", s) or "x"


def e(s):
    return html.escape(str(s or ""), quote=True)


def num(v, unite="", dec=0):
    """Formate un nombre a la francaise. Chaine vide si absent - jamais de zero invente."""
    if v in (None, "", "0", 0):
        return ""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return e(v)
    t = ("%%.%df" % dec) % f
    ent, _, frac = t.partition(".")
    ent = re.sub(r"(?<=\d)(?=(\d{3})+$)", " ", ent)
    out = ent + ("," + frac if frac else "")
    return out + (" " + unite if unite else "")


def lire(nom):
    with io.open(os.path.join(OUT, nom), encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


_EMDASH_FIN = re.compile(r"\s*—\s*\)")   # ex. "(2004—)" : plage ouverte
_EMDASH_DEBUT = re.compile(r"\(\s*—\s*")

def sans_emdash(html_txt):
    """Filet de securite : le contenu editorial est ecrit sans tiret cadratin,
    mais des donnees brutes (specs Wikipedia non reecrites) peuvent encore en
    contenir un, par exemple une plage d'annees ouverte "(2004—)". On les
    normalise ici plutot que de laisser passer le caractere."""
    if "—" not in html_txt:
        return html_txt
    html_txt = _EMDASH_FIN.sub(")", html_txt)
    html_txt = _EMDASH_DEBUT.sub("(", html_txt)
    return html_txt.replace("—", ", ")


def ecrire(chemin, contenu):
    p = os.path.join(SITE, chemin)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(sans_emdash(contenu))


# ----------------------------------------------------------------- gabarit
def page(titre, desc, corps, canon, extra_head="", fil=None, script=""):
    fil_html = ""
    if fil:
        items = []
        crumbs = []
        for i, (lib, href) in enumerate(fil, 1):
            if href:
                items.append('<a href="%s">%s</a>' % (e(href), e(lib)))
            else:
                items.append('<span aria-current="page">%s</span>' % e(lib))
            crumbs.append({"@type": "ListItem", "position": i, "name": lib,
                           "item": SITE_URL + href if href else None})
        fil_html = ('<nav class="fil" aria-label="Fil d\'Ariane">%s</nav>'
                    % '<span class="sep">›</span>'.join(items))
        extra_head += ('<script type="application/ld+json">%s</script>'
                       % json.dumps({"@context": "https://schema.org",
                                     "@type": "BreadcrumbList",
                                     "itemListElement": crumbs},
                                    ensure_ascii=False))
    return """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titre)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(canon)s">
<meta property="og:title" content="%(titre)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:image" content="%(og_image)s">
<meta property="og:image:width" content="1000">
<meta property="og:image:height" content="1000">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="%(og_image)s">
<link rel="stylesheet" href="%(racine)s/assets/style.css">
<link rel="icon" type="image/png" href="%(racine)s/assets/favicon.png">
<link rel="apple-touch-icon" href="%(racine)s/assets/favicon.png">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=%(ga_id)s"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '%(ga_id)s');
</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=%(adsense)s"
     crossorigin="anonymous"></script>
%(extra)s
</head>
<body>
<a class="saut" href="#contenu">Aller au contenu</a>
<header class="entete">
  <div class="conteneur barre">
    <a class="logo" href="%(racine)s/">%(site)s</a>
    <nav class="nav-principale" aria-label="Navigation principale">
      <a href="%(racine)s/guides/">Guides</a>
      <a href="%(racine)s/comparateur.html">Comparateur</a>
      <a href="%(racine)s/marques/">Marques</a>
      <a href="%(racine)s/ecoles/">Écoles</a>
      <a href="%(racine)s/duels/">Duels</a>
    </nav>
  </div>
</header>
<main id="contenu">
%(fil)s
%(corps)s
</main>
<footer class="pied">
  <div class="conteneur">
    <p class="pied-titre">%(site)s</p>
    <p>Fiches techniques, comparateur et duels de motos.</p>
    <p class="mention">Données issues de Wikipédia, sous licence
      <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.fr" rel="license nofollow">CC&nbsp;BY-SA&nbsp;4.0</a>.
      Chaque fiche renvoie à son article source. Les photographies conservent
      la licence et l'auteur indiqués sur la fiche.</p>
    <p class="mention">Les caractéristiques sont fournies à titre indicatif et
      peuvent comporter des erreurs. Vérifiez auprès du constructeur avant tout achat.</p>
    <nav class="pied-liens" aria-label="Informations légales">
      <a href="%(racine)s/mentions-legales.html">Mentions légales</a>
      <a href="%(racine)s/politique-de-confidentialite.html">Politique de confidentialité</a>
    </nav>
    <p class="mention">&copy; %(annee)s %(site)s. Tous droits réservés sur le
      contenu éditorial ; les données techniques restent sous licence
      CC&nbsp;BY-SA&nbsp;4.0 (Wikipédia).</p>
  </div>
</footer>
%(script)s
</body>
</html>""" % {"titre": e(titre), "desc": e(desc), "canon": e(canon),
              "extra": extra_head, "corps": corps, "fil": fil_html,
              "site": e(SITE_NOM), "racine": RACINE, "script": script,
              "og_image": e(SITE_URL + "/assets/og-image.jpg"), "ga_id": GA_ID,
              "adsense": ADSENSE_CLIENT, "annee": date.today().year}


# ----------------------------------------------------------------- polices
# Oswald (variable, licence OFL) auto-hebergee en base64 : aucune requete
# externe au chargement, conforme au reste du site.
_FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")

def _font_b64(nom):
    p = os.path.join(_FONT_DIR, nom)
    if not os.path.exists(p):
        return ""
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

_OSWALD_B64 = _font_b64("oswald-variable.woff2")
FONT_FACE_CSS = ""
if _OSWALD_B64:
    FONT_FACE_CSS = (
        "@font-face{font-family:'Oswald';font-style:normal;"
        "font-weight:500 700;font-display:swap;"
        "src:url(data:font/woff2;base64," + _OSWALD_B64 + ") format('woff2');}\n"
    )

# ----------------------------------------------------------------- CSS
CSS = FONT_FACE_CSS + """
:root{
  --fond:#f1eee6; --carte:#fff; --creux:#e9e3d6;
  --texte:#1a1714; --doux:#5c554a; --pale:#8a8172;
  --trait:#ded6c4; --trait-fort:#c4b9a0;
  --accent:#b93f0a; --accent-clair:#f8ded0;
  --petrole:#0e3b3d; --vert:#2c6a4e; --rouge:#8f2a1f;
  --cta:#b93f0a; --cta-survol:#963309;
  --ombre:0 1px 2px rgba(26,23,20,.06),0 8px 22px -14px rgba(26,23,20,.24);
  --police:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --police-titre:"Oswald",Impact,"Arial Narrow",var(--police);
  --mono:ui-monospace,"SFMono-Regular","Consolas","Liberation Mono",monospace;
  --large:1180px;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --fond:#14110c; --carte:#1f1b15; --creux:#191510;
    --texte:#f1ece2; --doux:#b9ae9c; --pale:#8e8371;
    --trait:#332b1f; --trait-fort:#473c2a;
    --accent:#ff7a33; --accent-clair:#3a2013;
    --petrole:#5fc2b8; --vert:#6dbf94; --rouge:#e0836f;
    --ombre:0 1px 2px rgba(0,0,0,.4),0 10px 28px -16px rgba(0,0,0,.7);
  }
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--fond);color:var(--texte);font-family:var(--police);
  font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}
img{max-width:100%;height:auto;display:block}
a{color:inherit;text-underline-offset:2px;text-decoration-color:var(--accent)}
a:focus-visible,button:focus-visible,select:focus-visible,input:focus-visible{
  outline:2px solid var(--accent);outline-offset:2px;border-radius:3px}
.conteneur{max-width:var(--large);margin:0 auto;padding:0 clamp(1rem,4vw,2rem)}
.saut{position:absolute;left:-9999px}
.saut:focus{left:1rem;top:1rem;z-index:99;background:var(--carte);padding:.6rem 1rem;
  border:2px solid var(--accent);border-radius:4px}

.entete{background:var(--carte);border-bottom:1px solid var(--trait);
  position:sticky;top:0;z-index:20}
.barre{display:flex;align-items:center;gap:1.5rem clamp(1.2rem,4vw,3.2rem);
  min-height:60px;flex-wrap:wrap}
.logo{font-family:var(--police-titre);font-weight:600;font-size:1.4rem;
  letter-spacing:.02em;text-transform:uppercase;text-decoration:none;flex:none}
.nav-principale{flex:1 1 auto;display:flex;justify-content:space-evenly;
  flex-wrap:wrap;gap:.5rem 1.25rem}
.nav-principale a{text-decoration:none;color:var(--doux);font-size:.94rem;font-weight:500}
.nav-principale a:hover{color:var(--accent)}

.fil{max-width:var(--large);margin:0 auto;padding:.9rem clamp(1rem,4vw,2rem) 0;
  font-size:.84rem;color:var(--pale)}
.fil a{color:var(--doux);text-decoration:none}
.fil a:hover{color:var(--accent);text-decoration:underline}
.fil .sep{margin:0 .45rem;color:var(--trait-fort)}

.section{padding:2.5rem 0}
h1{font-family:var(--police-titre);font-weight:600;
  font-size:clamp(1.9rem,4.6vw,2.8rem);line-height:1.08;letter-spacing:.001em;
  margin:.4rem 0 .6rem;text-wrap:balance}
h2{font-family:var(--police-titre);font-weight:600;
  font-size:clamp(1.4rem,3vw,1.8rem);letter-spacing:.001em;margin:2.2rem 0 1rem;
  text-wrap:balance}
h3{font-family:var(--police-titre);font-weight:600;font-size:1.2rem;
  letter-spacing:.001em;margin:1.6rem 0 .5rem}
p{margin:0 0 1rem}
.chapo{font-size:1.08rem;color:var(--doux);max-width:64ch}

.heros{background:var(--carte);border-bottom:1px solid var(--trait);
  padding:clamp(2.5rem,7vw,4.5rem) 0}
.heros h1{margin-top:0}
.heros .chapo{font-size:1.15rem}
.chiffres{display:flex;flex-wrap:wrap;gap:1.5rem 2.5rem;margin-top:2rem}
.chiffre .v{font-size:1.7rem;font-weight:700;letter-spacing:-.02em;
  font-variant-numeric:tabular-nums;display:block;color:var(--accent)}
.chiffre .l{font-size:.76rem;text-transform:uppercase;letter-spacing:.1em;color:var(--pale)}

.grille{display:grid;gap:1.1rem;
  grid-template-columns:repeat(auto-fill,minmax(255px,1fr))}
.carte{background:var(--carte);border:1px solid var(--trait);border-radius:8px;
  overflow:hidden;box-shadow:var(--ombre);display:flex;flex-direction:column;
  text-decoration:none;color:inherit;transition:border-color .15s,transform .15s}
.carte:hover{border-color:var(--accent);transform:translateY(-2px)}
.carte-img{aspect-ratio:16/10;background:var(--creux);overflow:hidden}
.carte-img img{width:100%;height:100%;object-fit:cover}
.carte-corps{padding:.85rem 1rem 1rem;display:flex;flex-direction:column;gap:.35rem;flex:1}
.carte-marque{font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;color:var(--pale)}
.carte-nom{font-family:var(--police-titre);font-weight:600;font-size:1.12rem;
  line-height:1.22;letter-spacing:.001em}
.carte-specs{margin-top:auto;padding-top:.5rem;font-size:.83rem;color:var(--doux);
  font-variant-numeric:tabular-nums;display:flex;flex-wrap:wrap;gap:.15rem .7rem}

.etiq{display:inline-block;font-size:.7rem;font-weight:650;text-transform:uppercase;
  letter-spacing:.07em;padding:.16rem .45rem;border-radius:3px;border:1px solid currentColor}
.etiq.a2{color:var(--vert)}
.etiq.a2non{color:var(--doux)}
.etiq.ecole{color:var(--accent)}
.etiq.nouveau{color:#fff;background:var(--cta);border-color:var(--cta)}
.etiq.reference{color:var(--petrole);border-color:var(--petrole)}

.fiche{display:grid;gap:2rem;grid-template-columns:1fr}
@media(min-width:900px){.fiche{grid-template-columns:minmax(0,1.15fr) minmax(0,1fr)}}
.fiche-photo{border-radius:8px;overflow:hidden;border:1px solid var(--trait);background:var(--carte)}
.credit{font-size:.74rem;color:var(--pale);padding:.5rem .7rem;border-top:1px solid var(--trait)}
.credit a{color:var(--doux)}

.specs{width:100%;border-collapse:collapse;background:var(--carte);
  border:1px solid var(--trait);border-radius:8px;overflow:hidden}
.specs caption{text-align:left;font-size:.74rem;text-transform:uppercase;
  letter-spacing:.11em;color:var(--pale);padding:.9rem 1rem .3rem}
.specs th,.specs td{padding:.6rem 1rem;border-bottom:1px solid var(--trait);
  text-align:left;font-size:.94rem}
.specs th{font-weight:500;color:var(--doux);width:48%}
.specs td{font-variant-numeric:tabular-nums;font-weight:550}
.specs tr:last-child th,.specs tr:last-child td{border-bottom:0}

.encart{background:var(--accent-clair);border:1px solid var(--trait);
  border-left:4px solid var(--accent);border-radius:0 8px 8px 0;
  padding:1rem 1.2rem;margin:1.5rem 0}
.encart-titre{font-family:var(--police-titre);font-size:.78rem;text-transform:uppercase;
  letter-spacing:.1em;color:var(--accent);font-weight:600;margin-bottom:.35rem}
.encart p{margin:0;font-size:.94rem}

.encart-achat{background:var(--carte)}
.liens-affilies{display:flex;flex-wrap:wrap;gap:.6rem;margin-top:.2rem}
.lien-affilie{display:inline-flex;align-items:center;gap:.4rem;
  background:var(--cta);color:#fff;font-family:var(--police-titre);
  font-weight:600;font-size:.88rem;letter-spacing:.02em;
  padding:.55rem 1.1rem;border-radius:4px;text-decoration:none;
  transition:transform .12s,background .12s}
.lien-affilie:hover{background:var(--cta-survol);transform:translateY(-1px)}
.mention-affilie{margin-top:.7rem !important;font-size:.76rem !important;
  color:var(--pale)}

.duel{display:grid;gap:1rem;grid-template-columns:1fr}
@media(min-width:760px){.duel{grid-template-columns:1fr auto 1fr;align-items:start}}
.duel-vs{align-self:center;font-family:var(--police-titre);font-weight:600;
  color:var(--accent);font-size:1.3rem;letter-spacing:.04em;text-transform:uppercase;
  text-align:center}
.tab-duel{width:100%;border-collapse:collapse;background:var(--carte);
  border:1px solid var(--trait);border-radius:8px;overflow:hidden;margin-top:1.5rem}
.tab-duel th,.tab-duel td{padding:.6rem .8rem;border-bottom:1px solid var(--trait);font-size:.92rem}
.tab-duel thead th{font-size:.74rem;text-transform:uppercase;letter-spacing:.09em;
  color:var(--doux);border-bottom:1px solid var(--trait-fort)}
.tab-duel td{text-align:center;font-variant-numeric:tabular-nums}
.tab-duel th[scope=row]{text-align:left;font-weight:500;color:var(--doux)}
.gagne{color:var(--vert);font-weight:650}

.filtres{background:var(--carte);border:1px solid var(--trait);border-radius:8px;
  padding:1.1rem;display:grid;gap:.9rem;
  grid-template-columns:repeat(auto-fit,minmax(165px,1fr));margin-bottom:1.5rem}
.champ{display:flex;flex-direction:column;gap:.3rem}
.champ label{font-size:.74rem;text-transform:uppercase;letter-spacing:.09em;color:var(--pale)}
.champ select,.champ input{padding:.5rem .6rem;border:1px solid var(--trait-fort);
  border-radius:5px;background:var(--fond);color:var(--texte);font-size:.92rem;
  font-family:inherit;width:100%}
/* Menu deroulant maison : remplace les <select> a tres nombreuses options
   (ecole, categorie, marque) dont l'ouverture native peut se faire vers le
   haut faute de place sous le champ. La liste est positionnee explicitement
   sous le bouton, donc s'ouvre toujours vers le bas. Le <select> reel est
   conserve (masque) comme source de valeur pour le script de filtrage. */
.menu-deroulant{position:relative}
.md-select-reel{position:absolute;opacity:0;pointer-events:none;width:1px;height:1px}
.md-bouton{display:flex;align-items:center;justify-content:space-between;gap:.5rem;
  width:100%;padding:.5rem .6rem;border:1px solid var(--trait-fort);border-radius:5px;
  background:var(--fond);color:var(--texte);font-size:.92rem;font-family:inherit;
  text-align:left;cursor:pointer}
.md-bouton:hover{border-color:var(--accent)}
.menu-deroulant.ouvert .md-bouton{border-color:var(--accent)}
.md-val{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.md-fleche{width:14px;height:14px;flex:none;color:var(--pale);transition:transform .12s}
.menu-deroulant.ouvert .md-fleche{transform:rotate(180deg);color:var(--accent)}
.md-liste{position:absolute;top:calc(100% + 4px);left:0;right:0;z-index:30;
  margin:0;padding:.3rem;list-style:none;max-height:280px;overflow-y:auto;
  background:var(--carte);border:1px solid var(--trait-fort);border-radius:7px;
  box-shadow:var(--ombre)}
.md-liste[hidden]{display:none}
.md-liste li{padding:.45rem .6rem;border-radius:4px;font-size:.92rem;cursor:pointer;
  color:var(--texte)}
.md-liste li.md-surlignee{background:var(--creux)}
.md-liste li[aria-selected="true"]{color:var(--accent);font-weight:650}
.compteur{font-size:.9rem;color:var(--doux);margin-bottom:1rem}
.vide{padding:2.5rem 1rem;text-align:center;color:var(--doux);background:var(--carte);
  border:1px dashed var(--trait-fort);border-radius:8px}

.liste-liens{display:grid;gap:.5rem;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));
  list-style:none;padding:0;margin:0}
.liste-liens a{display:flex;justify-content:space-between;gap:.5rem;align-items:baseline;
  padding:.6rem .8rem;background:var(--carte);border:1px solid var(--trait);
  border-radius:6px;text-decoration:none;font-size:.94rem}
.liste-liens a:hover{border-color:var(--accent)}
.liste-liens .n{color:var(--pale);font-size:.82rem;font-variant-numeric:tabular-nums}

/* --- identité nationale et bandeaux --- */
.bandes{display:flex;height:5px;width:100%}
.bandes i{flex:1}

.hero-nation,.hero-cat{position:relative;overflow:hidden;isolation:isolate;
  background:#15100a;color:#f3efe7;margin-bottom:2rem}
/* le bandeau est sombre dans les deux themes : on y emploie toujours la
   variante claire de la couleur nationale. Le bleu britannique d'origine
   tombe a 1,28:1 sur ce fond, la variante claire remonte au-dela de 4,5:1. */
.hero-nation{--nat-actif:var(--nat-nuit)}
.hero-nation .bandes{position:absolute;top:0;left:0;z-index:3}
.hero-fond{position:absolute;inset:0;background-size:cover;background-position:center;
  opacity:.32;filter:grayscale(.3) contrast(1.08) saturate(1.1);z-index:0}
.hero-nation::after,.hero-cat::after{content:"";position:absolute;inset:0;z-index:1;
  background:linear-gradient(105deg,#15100a 8%,rgba(21,16,10,.86) 48%,rgba(21,16,10,.42) 100%)}
.hero-corps{position:relative;z-index:2;padding:clamp(2.6rem,7vw,4.4rem) 0 clamp(2rem,5vw,3rem);
  max-width:min(680px,100%)}
.hero-eyebrow{font-family:var(--police-titre);font-size:.8rem;text-transform:uppercase;
  letter-spacing:.16em;font-weight:600;color:var(--nat-actif,#ff7a33);margin:0 0 .5rem;
  display:flex;align-items:center;gap:.5rem}
.hero-cat .hero-eyebrow{color:#ff7a33}
.hero-drapeau{font-size:1.15rem;line-height:1}
.hero-nation h1,.hero-cat h1{font-family:var(--police-titre);margin:0;color:#fff;
  font-size:clamp(2.1rem,5.6vw,3.4rem);font-weight:600;letter-spacing:.002em;
  line-height:1.02;text-transform:uppercase}
.hero-signature{margin:.5rem 0 0;font-size:1.1rem;font-weight:600;
  color:var(--nat-actif,#ff7a33)}
.hero-chapo{margin:.9rem 0 0;color:#d4cbba;font-size:1.02rem;line-height:1.6;
  max-width:60ch}
.hero-corps .chiffres{margin-top:1.8rem;gap:1.2rem 2.2rem}
.hero-corps .chiffre .v{font-family:var(--police-titre);color:#fff;font-weight:600}
.hero-corps .chiffre .l{color:#a79c89}

.hero-accueil{position:relative;overflow:hidden;isolation:isolate;
  background:#15100a;color:#f3efe7;border-bottom:1px solid var(--trait)}
.hero-accueil::after{content:"";position:absolute;inset:0;z-index:1;
  background:linear-gradient(100deg,#15100a 6%,rgba(21,16,10,.9) 46%,rgba(21,16,10,.5) 100%)}
.hero-accueil .hero-corps{max-width:min(700px,100%);
  padding:clamp(3rem,8vw,5.5rem) 0 clamp(2.4rem,5vw,3.4rem)}
.hero-accueil .hero-eyebrow{color:#ff7a33}
.hero-accueil h1{font-family:var(--police-titre);color:#fff;font-weight:600;
  font-size:clamp(2.2rem,5.8vw,3.6rem);letter-spacing:.002em;line-height:1;
  text-transform:uppercase}
.hero-actions{display:flex;flex-wrap:wrap;gap:.7rem;margin:2rem 0 0}
.bouton,.bouton-secondaire{display:inline-flex;align-items:center;gap:.5rem;
  padding:.75rem 1.4rem;border-radius:4px;font-family:var(--police-titre);
  font-size:.95rem;font-weight:600;letter-spacing:.03em;text-transform:uppercase;
  text-decoration:none;transition:transform .12s,background .12s,color .12s}
.bouton{background:#ff7a33;color:#1a1512}
.bouton:hover{background:#ff9557;transform:translateY(-1px)}
.bouton-secondaire{border:1.5px solid rgba(243,239,231,.35);color:#f3efe7}
.bouton-secondaire:hover{border-color:#ff7a33;color:#ff7a33;transform:translateY(-1px)}
.hero-credit{margin:1.6rem 0 0;font-size:.76rem;color:#93876f}
.hero-credit a{color:#c4b8a0}

.hero-mosaique{position:absolute;top:0;right:0;bottom:0;width:42%;z-index:1;
  display:none;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:2px;
  opacity:.5;
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 55%);
  mask-image:linear-gradient(90deg,transparent,#000 55%)}
@media(min-width:900px){.hero-mosaique{display:grid}}
.hero-mosaique img{width:100%;height:100%;object-fit:cover}

.grille-ecoles{display:grid;gap:1.1rem;
  grid-template-columns:repeat(auto-fill,minmax(260px,1fr));margin-top:1.6rem}
.carte-ecole{--ce-actif:var(--nat);background:var(--carte);border:1px solid var(--trait);
  border-radius:8px;overflow:hidden;text-decoration:none;color:inherit;
  box-shadow:var(--ombre);display:flex;flex-direction:column;
  transition:border-color .15s,transform .15s}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]) .carte-ecole{--ce-actif:var(--nat-nuit)}
}
.carte-ecole:hover{transform:translateY(-3px);border-color:var(--ce-actif)}
.ce-img{aspect-ratio:16/9;background:var(--creux) center/cover}
.ce-vide{background:var(--creux)}
.ce-corps{padding:.9rem 1.05rem 1.1rem;display:flex;flex-direction:column;gap:.25rem;flex:1}
.ce-pays{font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:var(--pale);
  display:flex;align-items:center;gap:.4rem}
.ce-drapeau{font-size:1rem;line-height:1}
.ce-nom{font-family:var(--police-titre);font-weight:600;font-size:1.2rem;
  letter-spacing:.001em;color:var(--ce-actif)}
.ce-signature{font-size:.9rem;color:var(--doux);line-height:1.4;margin-top:.15rem}
.ce-chiffres{margin-top:auto;padding-top:.6rem;font-size:.8rem;color:var(--pale);
  font-variant-numeric:tabular-nums}

/* pastille de nationalité sur les fiches */
.etiq-nat{display:inline-flex;align-items:center;gap:.35rem;font-size:.7rem;
  font-weight:650;text-transform:uppercase;letter-spacing:.07em;
  padding:.18rem .5rem;border-radius:3px;text-decoration:none;
  border:1px solid var(--nat,var(--accent));color:var(--nat,var(--accent))}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]) .etiq-nat{border-color:var(--nat-nuit,var(--accent));
    color:var(--nat-nuit,var(--accent))}
}

/* --- guides d'achat --- */
.guide{max-width:820px}
.guide h2{scroll-margin-top:80px;padding-top:.6rem;border-top:1px solid var(--trait)}
.guide-meta{font-size:.72rem;text-transform:uppercase;letter-spacing:.12em;
  color:var(--accent);font-weight:650;margin:0 0 .3rem}
.sommaire{background:var(--creux);border-radius:8px;padding:1.1rem 1.3rem;margin:2rem 0}
.sommaire-t{font-size:.72rem;text-transform:uppercase;letter-spacing:.11em;
  color:var(--pale);font-weight:650;margin:0 0 .6rem}
.sommaire ol{margin:0;padding-left:1.2rem;display:flex;flex-direction:column;gap:.35rem}
.sommaire a{color:var(--texte);text-decoration:none;font-size:.95rem}
.sommaire a:hover{color:var(--accent);text-decoration:underline}

.grille-guide{display:flex;flex-direction:column;gap:1.2rem;margin:1.5rem 0}
.carte-guide{background:var(--carte);border:1px solid var(--trait);border-radius:8px;
  padding:1.3rem;box-shadow:var(--ombre);scroll-margin-top:80px}
.cg-tete{display:flex;align-items:center;gap:.8rem;margin-bottom:.8rem}
.cg-rang{font-family:var(--police-titre);font-size:1rem;font-weight:600;
  color:var(--accent);font-variant-numeric:tabular-nums;flex:none;
  width:2.1rem;height:2.1rem;border:1.5px solid var(--accent);border-radius:50%;
  display:flex;align-items:center;justify-content:center}
.cg-tete h3{margin:0;font-size:1.25rem;letter-spacing:.001em}
.cg-img{border-radius:6px;overflow:hidden;margin-bottom:1rem;background:var(--creux);
  max-height:280px}
.cg-img img{width:100%;height:100%;object-fit:cover}
.cg-pour{font-size:.96rem;margin:0 0 .9rem}
.cg-chiffres{display:flex;flex-wrap:wrap;gap:1.6rem;padding:.8rem 0;
  border-top:1px solid var(--trait);border-bottom:1px solid var(--trait);margin-bottom:1rem}
.cg-chiffres>div{display:flex;flex-direction:column;gap:.1rem}
.cg-l{font-size:.66rem;text-transform:uppercase;letter-spacing:.1em;color:var(--pale)}
.cg-v{font-weight:650;font-variant-numeric:tabular-nums;font-size:.98rem}
.cg-listes{display:grid;gap:1.2rem;grid-template-columns:1fr}
@media(min-width:640px){.cg-listes{grid-template-columns:1fr 1fr}}
.cg-sl{font-size:.68rem;text-transform:uppercase;letter-spacing:.1em;font-weight:650;
  margin:0 0 .4rem}
.cg-listes>div:first-child .cg-sl{color:var(--vert)}
.cg-listes>div:last-child .cg-sl{color:var(--rouge)}
.cg-plus,.cg-moins{margin:0;padding-left:1.1rem;display:flex;flex-direction:column;
  gap:.35rem;font-size:.92rem}
.cg-plus li::marker{color:var(--vert)}
.cg-moins li::marker{color:var(--rouge)}
.cg-verdict{margin:1.1rem 0 .8rem;padding:.8rem 1rem;background:var(--creux);
  border-radius:6px;font-size:.95rem}
.cg-lien{display:inline-block;font-size:.88rem;font-weight:600;color:var(--accent);
  text-decoration:none;border-bottom:1px solid currentColor}
.cg-absent{font-size:.84rem;color:var(--pale);font-style:italic}

.faq{background:var(--carte);border:1px solid var(--trait);border-radius:6px;
  padding:.85rem 1.1rem;margin-bottom:.6rem}
.faq summary{cursor:pointer;font-weight:600;font-size:.98rem}
.faq summary::marker{color:var(--accent)}
.faq p{margin:.7rem 0 0;font-size:.94rem;color:var(--doux)}
.sources{font-size:.88rem;color:var(--doux);padding-left:1.2rem;
  display:flex;flex-direction:column;gap:.4rem}
.sources a{word-break:break-word}

.grille-guides-index{display:grid;gap:1rem;
  grid-template-columns:repeat(auto-fill,minmax(280px,1fr));margin-top:1.5rem}
.carte-guide-lien{background:var(--carte);border:1px solid var(--trait);
  border-left:3px solid var(--accent);border-radius:0 8px 8px 0;padding:1.2rem;
  text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:.5rem;
  box-shadow:var(--ombre);transition:border-color .15s,transform .15s}
.carte-guide-lien:hover{transform:translateY(-2px)}
.cgl-titre{font-family:var(--police-titre);font-weight:600;font-size:1.22rem;
  letter-spacing:.001em;line-height:1.2}
.cgl-desc{font-size:.9rem;color:var(--doux);line-height:1.45}

/* --- entree par modele sur la page Duels --- */
.selecteur{background:var(--carte);border:1px solid var(--trait);
  border-left:3px solid var(--accent);border-radius:0 8px 8px 0;
  padding:1.2rem 1.3rem;margin:1.5rem 0 2rem;max-width:640px}
.selecteur label{display:block;font-size:.74rem;text-transform:uppercase;
  letter-spacing:.1em;color:var(--accent);font-weight:650;margin-bottom:.5rem}
.selecteur select{width:100%;padding:.65rem .7rem;border:1px solid var(--trait-fort);
  border-radius:6px;background:var(--fond);color:var(--texte);
  font-size:1rem;font-family:inherit}
.selecteur-aide{margin:.6rem 0 0;font-size:.86rem;color:var(--doux)}

.grille-duels{display:grid;gap:1rem;
  grid-template-columns:repeat(auto-fill,minmax(320px,1fr))}
.carte-duel{background:var(--carte);border:1px solid var(--trait);border-radius:8px;
  padding:1rem;text-decoration:none;color:inherit;box-shadow:var(--ombre);
  display:flex;flex-direction:column;gap:.8rem;
  transition:border-color .15s,transform .15s}
.carte-duel:hover{border-color:var(--accent);transform:translateY(-2px)}
.cd-cotes{display:grid;grid-template-columns:1fr auto 1fr;gap:.6rem;align-items:start}
.cd-cote{display:flex;flex-direction:column;gap:.2rem;min-width:0}
.cd-img{aspect-ratio:4/3;background:var(--creux);border-radius:5px;overflow:hidden;
  margin-bottom:.35rem}
.cd-img img{width:100%;height:100%;object-fit:cover}
.cd-marque{font-size:.66rem;text-transform:uppercase;letter-spacing:.09em;color:var(--pale)}
.cd-nom{font-family:var(--police-titre);font-weight:600;font-size:1rem;
  line-height:1.2;letter-spacing:.001em}
.cd-spec{font-size:.78rem;color:var(--doux);font-variant-numeric:tabular-nums;
  line-height:1.35}
.cd-vs{align-self:center;font-family:var(--police-titre);font-size:.78rem;
  text-transform:uppercase;letter-spacing:.1em;color:var(--accent);
  font-weight:600;padding-top:2.2rem}
.cd-pied{display:flex;flex-wrap:wrap;gap:.35rem;padding-top:.6rem;
  border-top:1px solid var(--trait)}

.pied{background:var(--carte);border-top:1px solid var(--trait);margin-top:4rem;
  padding:2rem 0;font-size:.9rem;color:var(--doux)}
.pied-titre{font-weight:700;color:var(--texte);margin-bottom:.3rem}
.mention{font-size:.8rem;color:var(--pale);max-width:75ch}
.pied-liens{display:flex;flex-wrap:wrap;gap:.3rem 1rem;margin:.8rem 0}
.pied-liens a{color:var(--doux);font-size:.85rem;text-decoration:underline}
.pied-liens a:hover{color:var(--accent)}
.tableau-large{overflow-x:auto}
"""


# ----------------------------------------------------------------- donnees
modeles = lire("modeles.csv")
duels = lire("duels.csv")

pub = [m for m in modeles
       if int(m["completude_pct"] or 0) >= MIN_COMPLETUDE
       and m["marque"] and m["nom_affichage"]]
for m in pub:
    m["url"] = "/motos/%s/%s.html" % (slug(m["marque"]), m["modele_id"])
par_id = {m["modele_id"]: m for m in pub}

print("%d modeles publiables sur %d" % (len(pub), len(modeles)))

par_marque = defaultdict(list)
par_ecole = defaultdict(list)
par_cat = defaultdict(list)
for m in pub:
    par_marque[m["marque"]].append(m)
    if m["ecole"]:
        par_ecole[m["ecole"]].append(m)
    if m["categorie"]:
        par_cat[m["categorie"]].append(m)
for d in (par_marque, par_ecole, par_cat):
    for k in d:
        d[k].sort(key=lambda x: -float(x["priorite"] or 0))

duels_ok = [d for d in duels
            if d["modele_a_id"] in par_id and d["modele_b_id"] in par_id]
for d in duels_ok:
    d["url"] = "/duels/%s.html" % d["duel_id"]
print("%d duels publiables sur %d" % (len(duels_ok), len(duels)))

urls = []


def enregistrer(chemin, prio="0.6"):
    urls.append((chemin, prio))


# ----------------------------------------------------------------- fragments
def vignette(m, prio_img=False):
    img = m.get("image_vignette") or m["image_url"]
    if img and m["image_utilisable"] == "oui":
        lazy = "" if prio_img else ' loading="lazy" decoding="async"'
        media = ('<div class="carte-img"><img src="%s" alt="%s"%s></div>'
                 % (e(img), e(m["nom_affichage"]), lazy))
    else:
        media = '<div class="carte-img"></div>'
    bits = []
    if m["cylindree_cc"]:
        bits.append(num(m["cylindree_cc"], "cm³"))
    if m["puissance_ch"]:
        bits.append(num(m["puissance_ch"], "ch", 0))
    if m["poids_kg"]:
        bits.append(num(m["poids_kg"], "kg", 0))
    a2 = ('<span class="etiq a2">A2</span>' if m["a2_compatible"] == "oui" else "")
    return ('<a class="carte" href="%s%s">%s<div class="carte-corps">'
            '<span class="carte-marque">%s</span>'
            '<span class="carte-nom">%s</span>'
            '<span class="carte-specs">%s %s</span></div></a>'
            % (RACINE, e(m["url"]), media, e(m["marque"]), e(m["nom_affichage"]),
               " · ".join(bits), a2))


def grille(liste, prio_n=0):
    if not liste:
        return '<p class="vide">Aucun modèle pour cette sélection.</p>'
    return ('<div class="grille">%s</div>'
            % "".join(vignette(m, i < prio_n) for i, m in enumerate(liste)))


def _cote(m):
    """Donnees d'un des deux cotes d'un duel."""
    return {"n": m["nom_affichage"], "m": m["marque"],
            "i": (m.get("image_vignette") or m["image_url"]) if m["image_utilisable"] == "oui" else "",
            "cy": m["cylindree_cc"] or "", "p": m["puissance_ch"] or "",
            "kg": m["poids_kg"] or ""}


def _cote_html(c, lazy=True):
    img = ('<img src="%s" alt="%s"%s>'
           % (e(c["i"]), e(c["n"]), ' loading="lazy" decoding="async"' if lazy else "")
           ) if c["i"] else ""
    bits = [x for x in (num(c["cy"], "cm³"), num(c["p"], "ch", 0),
                        num(c["kg"], "kg", 0)) if x]
    return ('<div class="cd-cote"><div class="cd-img">%s</div>'
            '<span class="cd-marque">%s</span>'
            '<span class="cd-nom">%s</span>'
            '<span class="cd-spec">%s</span></div>'
            % (img, e(c["m"]), e(c["n"]), " · ".join(bits)))


def carte_duel(d, lazy=True):
    a, b = _cote(par_id[d["modele_a_id"]]), _cote(par_id[d["modele_b_id"]])
    etiqs = []
    if d.get("phare_du_moment") == "oui":
        etiqs.append('<span class="etiq nouveau">Duel du moment</span>')
    elif d.get("phare_intemporel") == "oui":
        etiqs.append('<span class="etiq reference">Grand classique</span>')
    etiqs.append('<span class="etiq">%s</span>' % e(d["categorie"]))
    if d["a2"] == "oui":
        etiqs.append('<span class="etiq a2">A2</span>')
    if d["inter_ecoles"] == "oui":
        etiqs.append('<span class="etiq ecole">%s / %s</span>'
                     % (e(d["ecole_a"]), e(d["ecole_b"])))
    return ('<a class="carte-duel" href="%s%s">'
            '<div class="cd-cotes">%s<span class="cd-vs">contre</span>%s</div>'
            '<div class="cd-pied">%s</div></a>'
            % (RACINE, e(d["url"]), _cote_html(a, lazy), _cote_html(b, lazy),
               " ".join(etiqs)))




# ------------------------------------------------- traduction du vocabulaire
# Les champs libres de Wikipedia EN restent en anglais. On traduit le
# vocabulaire technique recurrent au moment de l'affichage ; le CSV conserve
# le texte source pour rester tracable.
TERMES = [
    # transmissions
    (r"\bconstant mesh\b", "à prise constante"),
    (r"\b(\d+)[- ]speed\b", r"\1 rapports"),
    (r"\bspeed manual\b", "rapports, boîte manuelle"),
    (r"\bmanual transmission\b", "boîte manuelle"),
    (r"\bcontinuously variable transmission\b", "variateur continu"),
    (r"\bCVT\b", "variateur continu (CVT)"),
    (r"\bautomatic\b", "automatique"),
    (r"\bsemi-automatic\b", "semi-automatique"),
    (r"\bwet (?:multi-?plate )?clutch\b", "embrayage multidisque à bain d'huile"),
    (r"\bdry clutch\b", "embrayage à sec"),
    (r"\bmulti-?plate\b", "multidisque"),
    (r"\bslipper clutch\b", "embrayage antidribble"),
    (r"\bwet\b", "à bain d'huile"),
    (r"\bchain drive\b", "transmission par chaîne"),
    (r"\bshaft drive\b", "transmission par cardan"),
    (r"\bbelt drive\b", "transmission par courroie"),
    (r"\bfinal drive\b", "transmission finale"),
    (r"\bchain\b", "chaîne"),
    (r"\bshaft\b", "cardan"),
    (r"\bbelt\b", "courroie"),
    (r"\bgearbox\b", "boîte de vitesses"),
    (r"\bsequential\b", "séquentielle"),
    # freins
    (r"\bdisc brakes?\b", "freins à disque"),
    (r"\bdrum brakes?\b", "freins à tambour"),
    (r"\btwin disc\b", "double disque"),
    (r"\bdual disc\b", "double disque"),
    (r"\bsingle disc\b", "simple disque"),
    (r"\bfloating disc\b", "disque flottant"),
    (r"\bdisc\b", "disque"),
    (r"\bdrum\b", "tambour"),
    (r"\bcalipers?\b", "étrier"),
    (r"\bpistons?\b", "pistons"),
    (r"\bmm\b", "mm"),
    # suspensions
    (r"\btelescopic forks?\b", "fourche télescopique"),
    (r"\binverted forks?\b", "fourche inversée"),
    (r"\bupside[- ]down forks?\b", "fourche inversée"),
    (r"\busd forks?\b", "fourche inversée"),
    (r"\bfork\b", "fourche"),
    (r"\bswinga?rm\b", "bras oscillant"),
    (r"\bmonoshock\b", "monoamortisseur"),
    (r"\btwin shocks?\b", "double amortisseur"),
    (r"\bshock absorbers?\b", "amortisseur"),
    (r"\bshocks?\b", "amortisseur"),
    (r"\bpreload\b", "précontrainte"),
    (r"\badjustable\b", "réglable"),
    (r"\brebound\b", "détente"),
    (r"\bdamping\b", "amortissement"),
    (r"\bspring\b", "ressort"),
    (r"\btravel\b", "débattement"),
    # cadres
    (r"\bsingle cradle\b", "simple berceau"),
    (r"\bdouble cradle\b", "double berceau"),
    (r"\bduplex cradle\b", "double berceau"),
    (r"\bhalf-duplex cradle\b", "demi-berceau"),
    (r"\bfull duplex cradle\b", "double berceau complet"),
    (r"\bcradle\b", "berceau"),
    (r"\btrellis\b", "treillis"),
    (r"\blattice\b", "treillis"),
    (r"\bperimeter\b", "périmétrique"),
    (r"\bbackbone\b", "poutre"),
    (r"\bspine\b", "poutre"),
    (r"\bmonocoque\b", "monocoque"),
    (r"\btubular\b", "tubulaire"),
    (r"\bsteel\b", "acier"),
    (r"\baluminium\b", "aluminium"),
    (r"\baluminum\b", "aluminium"),
    (r"\bcast\b", "coulé"),
    (r"\bcarbon fibre\b", "fibre de carbone"),
    (r"\bcarbon fiber\b", "fibre de carbone"),
    (r"\bdiamond\b", "diamant"),
    (r"\bframe\b", "cadre"),
    # moteur
    (r"\bfour-?stroke\b", "quatre temps"),
    (r"\btwo-?stroke\b", "deux temps"),
    (r"\bliquid-?cooled\b", "refroidissement liquide"),
    (r"\bair-?cooled\b", "refroidissement par air"),
    (r"\boil-?cooled\b", "refroidissement par huile"),
    (r"\bwater-?cooled\b", "refroidissement liquide"),
    (r"\bfuel injection\b", "injection électronique"),
    (r"\bcarburett?ors?\b", "carburateur"),
    (r"\bvalves?\b", "soupapes"),
    (r"\bcamshafts?\b", "arbre à cames"),
    (r"\boverhead camshaft\b", "arbre à cames en tête"),
    (r"\bcylinders?\b", "cylindres"),
    (r"\belectric start\b", "démarreur électrique"),
    (r"\bkick ?start\b", "kick"),
    # pneus / roues
    (r"\btyres?\b", "pneus"),
    (r"\btires?\b", "pneus"),
    (r"\bspoked?\b", "à rayons"),
    (r"\balloy wheels?\b", "jantes alliage"),
    (r"\bwheels?\b", "roues"),
    (r"\btubeless\b", "tubeless"),
    # positions
    (r"\bfront (?:and|&) rear\b", "avant et arrière"),
    (r"\bfront\b", "avant"),
    (r"\brear\b", "arrière"),
    (r"\bleft\b", "gauche"),
    (r"\bright\b", "droite"),
    (r"\bboth\b", "les deux"),
    # divers
    (r"\bversion\b", "version"),
    (r"\boptional\b", "en option"),
    (r"\bstandard\b", "de série"),
    (r"\bwith\b", "avec"),
    (r"\band\b", "et"),
    (r"\bor\b", "ou"),
    (r"\bfor the\b", "pour la"),
    (r"\bfor\b", "pour"),
    (r"\bsingle\b", "simple"),
    (r"\bdual\b", "double"),
    (r"\btwin\b", "double"),
    (r"\btriple\b", "triple"),
]
_TERMES = [(re.compile(p, re.I), r) for p, r in TERMES]


def fr_tech(s):
    """Traduit le vocabulaire technique anglais recurrent. Non exhaustif :
    les formulations rares restent en anglais plutot que d'etre deformees."""
    if not s:
        return ""
    out = str(s)
    for rx, rep in _TERMES:
        out = rx.sub(rep, out)
    out = re.sub(r"\s+", " ", out).strip(" ,;:")
    return out[:1].upper() + out[1:] if out else ""


LIGNES_SPECS = [
    ("Cylindrée", lambda m: num(m["cylindree_cc"], "cm³")),
    ("Architecture", lambda m: e(m["architecture"])),
    ("Refroidissement", lambda m: e(m["refroidissement"])),
    ("Puissance", lambda m: (num(m["puissance_ch"], "ch", 1)
                             + (" (%s)" % num(m["puissance_kw"], "kW", 1) if m["puissance_kw"] else "")
                             + (" à %s tr/min" % num(m["puissance_tr_min"]) if m["puissance_tr_min"] else ""))),
    ("Couple", lambda m: (num(m["couple_nm"], "Nm", 1)
                          + (" à %s tr/min" % num(m["couple_tr_min"]) if m["couple_tr_min"] else ""))),
    ("Poids", lambda m: (num(m["poids_kg"], "kg", 0)
                         + (" (%s)" % e(m["poids_type"]) if m["poids_type"] else ""))),
    ("Hauteur de selle", lambda m: num(m["hauteur_selle_mm"], "mm", 0)),
    ("Empattement", lambda m: num(m["empattement_mm"], "mm", 0)),
    ("Réservoir", lambda m: num(m["reservoir_l"], "L", 1)),
    ("Vitesse maximale", lambda m: num(m["vitesse_max_kmh"], "km/h", 0)),
    ("Alésage × course", lambda m: e(m["alesage_course"])),
    ("Compression", lambda m: e(fr_tech(m["compression"]))),
    ("Transmission", lambda m: e(fr_tech(m["transmission"]))),
    ("Cadre", lambda m: e(fr_tech(m["cadre"]))),
    ("Suspensions", lambda m: e(fr_tech(m["suspension"]))),
    ("Freins", lambda m: e(fr_tech(m["freins"]))),
    ("Pneus", lambda m: e(fr_tech(m["pneus"]))),
    ("Prix au lancement", lambda m: (num(m["prix_lancement_eur"], "€", 0)
                                     if m["prix_lancement_eur"] else "")),
]


# ----------------------------------------------------------------- pages
def page_modele(m):
    nom = m["nom_affichage"]
    marque = m["marque"]
    titre = "%s : fiche technique et caractéristiques" % nom
    bits = [x for x in (num(m["cylindree_cc"], "cm³"),
                        num(m["puissance_ch"], "ch", 0),
                        num(m["poids_kg"], "kg", 0)) if x]
    desc = "%s : %s. Fiche technique complète, %s." % (
        nom, ", ".join(bits) if bits else "caractéristiques détaillées",
        "compatible permis A2" if m["a2_compatible"] == "oui" else "spécifications vérifiées")

    # photo + credit
    photo = ""
    if (m.get("image_vignette") or m["image_url"]) and m["image_utilisable"] == "oui":
        cred = []
        if m["image_auteur"]:
            cred.append("© %s" % e(m["image_auteur"]))
        if m["image_licence"]:
            cred.append(e(m["image_licence"]))
        lien = (', <a href="%s" rel="nofollow">source</a>' % e(m["image_page"])
                if m["image_page"] else "")
        photo = ('<figure class="fiche-photo"><img src="%s" alt="%s" width="900">'
                 '<figcaption class="credit">%s%s</figcaption></figure>'
                 % (e(m.get("image_vignette") or m["image_url"]), e(nom),
                    " · ".join(cred) or "Wikimedia Commons", lien))

    lignes = []
    for lib, fn in LIGNES_SPECS:
        v = fn(m)
        if v and v.strip():
            lignes.append("<tr><th scope=\"row\">%s</th><td>%s</td></tr>" % (lib, v))
    tableau = ('<table class="specs"><caption>Caractéristiques techniques</caption>'
               '<tbody>%s</tbody></table>' % "".join(lignes))

    # A2 : on n'affiche l'encart que dans le cas positif, jamais "non compatible"
    a2 = ""
    if m["a2_compatible"] == "oui":
        a2 = ('<div class="encart"><p class="encart-titre">Permis A2</p>'
              '<p><strong>Compatible.</strong> %s, sous les 35 kW et un rapport '
              'poids/puissance inférieur à 0,2 kW/kg. Vérifiez l\'existence d\'une '
              'version bridée homologuée auprès du concessionnaire.</p></div>'
              % e(m["a2_detail"]))

    # identite
    ident = []
    if m["ecole"]:
        _id = ECOLES.get(slug(m["ecole"]), ECOLE_DEFAUT)
        ident.append('<a class="etiq-nat" href="%s/ecoles/%s.html" '
                     'style="--nat:%s;--nat-nuit:%s">'
                     '<span aria-hidden="true">%s</span> école %s</a>'
                     % (RACINE, slug(m["ecole"]), _id["accent"], _id["accent_nuit"],
                        _id["emoji"], e(m["ecole"])))
    if m["categorie"]:
        ident.append('<a class="etiq" href="%s/categories/%s.html">%s</a>'
                     % (RACINE, slug(m["categorie"]), e(m["categorie"])))
    periode = ""
    if m["annee_debut"]:
        periode = ("Produite depuis %s" % e(m["annee_debut"]) if not m["annee_fin"]
                   else "Produite de %s à %s" % (e(m["annee_debut"]), e(m["annee_fin"])))

    # resume : on ne recopie pas, on renvoie
    resume = ""
    if m["url_wikipedia_fr"]:
        resume = ('<p class="chapo">%s. Pour l\'historique détaillé du modèle, '
                  'consultez <a href="%s" rel="nofollow">l\'article Wikipédia</a>.</p>'
                  % (e(periode or "Modèle de la marque " + marque), e(m["url_wikipedia_fr"])))
    elif periode:
        resume = '<p class="chapo">%s.</p>' % e(periode)

    # duels lies
    liens_duels = [d for d in duels_ok
                   if m["modele_id"] in (d["modele_a_id"], d["modele_b_id"])][:6]
    bloc_duels = ""
    if liens_duels:
        li = []
        for d in liens_duels:
            autre = (d["modele_b"] if d["modele_a_id"] == m["modele_id"] else d["modele_a"])
            li.append('<li><a href="%s%s"><span>%s ou %s</span></a></li>'
                      % (RACINE, e(d["url"]), e(nom), e(autre)))
        bloc_duels = ('<h2>Comparer la %s</h2><ul class="liste-liens">%s</ul>'
                      % (e(nom), "".join(li)))

    # modeles proches
    proches = [x for x in par_marque.get(marque, [])
               if x["modele_id"] != m["modele_id"]][:8]
    bloc_proches = ""
    if proches:
        bloc_proches = ("<h2>Autres %s</h2>%s" % (e(marque), grille(proches)))

    # donnees structurees
    ld = {"@context": "https://schema.org", "@type": "Product",
          "name": nom, "category": m["categorie"] or "Motocyclette",
          "brand": {"@type": "Brand", "name": marque},
          "url": SITE_URL + m["url"]}
    if m["image_url"] and m["image_utilisable"] == "oui":
        ld["image"] = m["image_url"]
    props = []
    for lib, champ, unite in (("Cylindrée", "cylindree_cc", "cm3"),
                              ("Puissance", "puissance_ch", "ch"),
                              ("Poids", "poids_kg", "kg"),
                              ("Hauteur de selle", "hauteur_selle_mm", "mm")):
        if m[champ]:
            props.append({"@type": "PropertyValue", "name": lib,
                          "value": m[champ], "unitText": unite})
    if props:
        ld["additionalProperty"] = props
    extra = ('<script type="application/ld+json">%s</script>'
             % json.dumps(ld, ensure_ascii=False))

    corps = """<div class="conteneur section">
<p>%(ident)s</p>
<h1>%(nom)s</h1>
%(resume)s
<div class="fiche">
  <div>%(photo)s%(a2)s</div>
  <div class="tableau-large">%(tab)s</div>
</div>
%(duels)s
%(proches)s
<div class="encart"><p class="encart-titre">Source</p>
<p>Caractéristiques extraites de <a href="%(wen)s" rel="nofollow">Wikipédia</a>
(CC BY-SA 4.0). Complétude de cette fiche : %(comp)s %%.
Les valeurs absentes ne figurent pas dans la source.</p></div>
</div>""" % {"ident": " ".join(ident), "nom": e(nom), "resume": resume,
             "photo": photo, "a2": a2, "tab": tableau,
             "duels": bloc_duels, "proches": bloc_proches,
             "wen": e(m["url_wikipedia"]), "comp": e(m["completude_pct"])}

    fil = [("Accueil", "/"), ("Marques", "/marques/"),
           (marque, "/marques/%s.html" % slug(marque)), (nom, None)]
    ecrire(m["url"].lstrip("/"), page(titre, desc, corps, SITE_URL + m["url"],
                                      extra, fil))
    enregistrer(m["url"], "0.8")


# ----------------------------------------------------------------- ecoles
# Chaque ecole porte les couleurs de son pays. Ce ne sont pas des drapeaux
# reproduits mais des bandes de couleurs nationales : le drapeau lui-meme est
# rendu par l'emoji, qui reste lisible et accessible.
ECOLES = {
 "japonaise": {
   "pays": "Japon", "emoji": "🇯🇵",
   "bandes": ["#BC002D", "#F7F7F7", "#BC002D"],
   "accent": "#C41E3A", "accent_nuit": "#F08098",
   "signature": "Fiabilité et polyvalence",
   "texte": "Fiabilité, production de masse et polyvalence. Les quatre grands "
            "constructeurs nippons ont imposé un standard de robustesse que le "
            "reste du monde a dû rattraper. On ne les choisit pas pour le "
            "panache, mais pour la certitude que la moto démarrera dans dix ans."},
 "italienne": {
   "pays": "Italie", "emoji": "🇮🇹",
   "bandes": ["#008C45", "#F4F5F0", "#CD212A"],
   "accent": "#CD212A", "accent_nuit": "#F2707A",
   "signature": "Le caractère avant la raison",
   "texte": "Le caractère avant la raison. Châssis affûtés, moteurs typés et un "
            "dessin qui n'a jamais cherché le consensus. L'école italienne assume "
            "de faire des motos qu'on aime ou qu'on déteste, rarement des machines "
            "qui laissent indifférent."},
 "americaine": {
   "pays": "États-Unis", "emoji": "🇺🇸",
   "bandes": ["#B22234", "#F7F7F7", "#3C3B6E"],
   "accent": "#B22234", "accent_nuit": "#EE7C88",
   "signature": "Le couple et la ligne droite",
   "texte": "Le gros twin, le couple à bas régime et la ligne droite. Une "
            "conception née de routes larges et de longues distances, où le "
            "confort et la présence comptent davantage que le chrono."},
 "britannique": {
   "pays": "Royaume-Uni", "emoji": "🇬🇧",
   "bandes": ["#012169", "#F5F5F5", "#C8102E"],
   "accent": "#C8102E", "accent_nuit": "#F0808F",
   "signature": "L'école historique",
   "texte": "L'école historique. Twins verticaux, esthétique intemporelle et une "
            "influence qui dépasse largement les volumes produits. Beaucoup de "
            "codes du motocyclisme moderne viennent de ces ateliers."},
 "allemande": {
   "pays": "Allemagne", "emoji": "🇩🇪",
   "bandes": ["#1A1A1A", "#DD0000", "#FFCE00"],
   "accent": "#B8860B", "accent_nuit": "#EBC55A",
   "signature": "Ingénierie et longévité",
   "texte": "Ingénierie et longévité. Le flat-twin BMW a défini la moto de voyage "
            "moderne, avec des solutions techniques que personne d'autre n'a "
            "osées, cardan, Telelever, boxer transversal."},
 "autrichienne": {
   "pays": "Autriche", "emoji": "🇦🇹",
   "bandes": ["#ED2939", "#F7F7F7", "#ED2939"],
   "accent": "#ED2939", "accent_nuit": "#F58089",
   "signature": "Le tout-terrain comme point de départ",
   "texte": "Le tout-terrain comme point de départ. Des machines légères, "
            "nerveuses, orientées performance, où l'orange n'est pas une "
            "coquetterie mais une signature de compétition."},
 "indienne": {
   "pays": "Inde", "emoji": "🇮🇳",
   "bandes": ["#FF9933", "#F7F7F7", "#138808"],
   "accent": "#C8651B", "accent_nuit": "#F0A85E",
   "signature": "Le rapport prix-plaisir",
   "texte": "Longtemps cantonnée aux petites cylindrées utilitaires, l'école "
            "indienne s'est imposée en Europe avec des twins simples et "
            "abordables, au style assumé."},
 "espagnole": {
   "pays": "Espagne", "emoji": "🇪🇸",
   "bandes": ["#AA151B", "#F1BF00", "#AA151B"],
   "accent": "#AA151B", "accent_nuit": "#EB7B80",
   "signature": "Petites cylindrées et trial",
   "texte": "Une tradition de petites cylindrées vives et de trial, portée par "
            "des marques qui ont marqué les années 1970 et 1980."},
 "suedoise": {
   "pays": "Suède", "emoji": "🇸🇪",
   "bandes": ["#006AA7", "#FECC00", "#006AA7"],
   "accent": "#006AA7", "accent_nuit": "#5FA8D3",
   "signature": "Le tout-terrain nordique",
   "texte": "Une école née du tout-terrain et du motocross, aujourd'hui prolongée "
            "par des roadsters au dessin épuré."},
 "coreenne": {
   "pays": "Corée du Sud", "emoji": "🇰🇷",
   "bandes": ["#CD2E3A", "#F7F7F7", "#0047A0"],
   "accent": "#CD2E3A", "accent_nuit": "#F0838C",
   "signature": "L'accessible",
   "texte": "Une production tournée vers l'accessibilité, souvent dérivée de "
            "licences japonaises."},
 "taiwanaise": {
   "pays": "Taïwan", "emoji": "🇹🇼",
   "bandes": ["#000095", "#F7F7F7", "#FE0000"],
   "accent": "#0033A0", "accent_nuit": "#6E9BE0",
   "signature": "Le scooter urbain",
   "texte": "Spécialiste du scooter urbain et des petites cylindrées, avec une "
            "présence européenne solide sur ce créneau."},
 "francaise": {
   "pays": "France", "emoji": "🇫🇷",
   "bandes": ["#002395", "#F5F5F5", "#ED2939"],
   "accent": "#002395", "accent_nuit": "#7796DD",
   "signature": "Le deux-roues du quotidien",
   "texte": "Une école tournée vers le deux-roues urbain et le cyclomoteur, avec "
            "une histoire industrielle longue et quelques tentatives ambitieuses "
            "sur les grosses cylindrées."},
 "tcheque": {
   "pays": "Tchéquie", "emoji": "🇨🇿",
   "bandes": ["#11457E", "#F5F5F5", "#D7141A"],
   "accent": "#11457E", "accent_nuit": "#7E9DD0",
   "signature": "La simplicité robuste",
   "texte": "Des machines simples, robustes et faciles à entretenir, conçues pour "
            "durer dans des conditions difficiles."},
 "polonaise": {
   "pays": "Pologne", "emoji": "🇵🇱",
   "bandes": ["#F5F5F5", "#DC143C", "#DC143C"],
   "accent": "#DC143C", "accent_nuit": "#F2818F",
   "signature": "L'après-guerre utilitaire",
   "texte": "Une production essentiellement utilitaire, marquée par l'histoire "
            "industrielle de l'après-guerre."},
}
ECOLE_DEFAUT = {"pays": "", "emoji": "🏍️", "bandes": ["#9A6410", "#F2F2F2", "#123B41"],
                "accent": "#9A6410", "accent_nuit": "#DFA548",
                "signature": "", "texte": ""}


def bandes_html(ident):
    return ('<div class="bandes" aria-hidden="true">%s</div>'
            % "".join('<i style="background:%s"></i>' % c for c in ident["bandes"]))


def _fond(liste):
    """Image de fond d'un bandeau : la fiche la mieux classee qui en possede une."""
    for m in liste:
        u = m.get("image_vignette") or m.get("image_url")
        if u and m.get("image_utilisable") == "oui":
            return u
    return ""


def _chiffres(liste):
    n_a2 = sum(1 for m in liste if m["a2_compatible"] == "oui")
    marques = len({m["marque"] for m in liste if m["marque"]})
    cases = [("%d" % len(liste), "modèles"), ("%d" % marques, "marques")]
    if n_a2:
        cases.append(("%d" % n_a2, "compatibles A2"))
    return ('<div class="chiffres">%s</div>'
            % "".join('<div class="chiffre"><span class="v">%s</span>'
                      '<span class="l">%s</span></div>' % (v, l) for v, l in cases))


def hero_ecole(ecole, liste):
    ident = ECOLES.get(slug(ecole), ECOLE_DEFAUT)
    fond = _fond(liste)
    img = ('<div class="hero-fond" style="background-image:url(%s)" aria-hidden="true"></div>'
           % e(fond)) if fond else ""
    top = [m for m in liste if (m.get("image_vignette") or m.get("image_url"))
           and m.get("image_utilisable") == "oui"][:4]
    mosaique = ""
    if len(top) >= 3:
        mosaique = ('<div class="hero-mosaique" aria-hidden="true">%s</div>'
                    % "".join('<img src="%s" alt="" loading="lazy" decoding="async">'
                              % e(m.get("image_vignette") or m["image_url"])
                              for m in top[:4]))
    return """<header class="hero-nation" style="--nat:%(accent)s;--nat-nuit:%(nuit)s">
%(bandes)s
%(img)s
<div class="conteneur hero-corps">
  <p class="hero-eyebrow"><span class="hero-drapeau">%(emoji)s</span> %(pays)s</p>
  <h1>L'école %(ecole)s</h1>
  <p class="hero-signature">%(signature)s</p>
  <p class="hero-chapo">%(texte)s</p>
  %(chiffres)s
</div>
%(mosaique)s
</header>""" % {"accent": ident["accent"], "nuit": ident["accent_nuit"],
                "bandes": bandes_html(ident), "img": img,
                "emoji": ident["emoji"], "pays": e(ident["pays"]),
                "ecole": e(ecole), "signature": e(ident["signature"]),
                "texte": e(ident["texte"]), "chiffres": _chiffres(liste),
                "mosaique": mosaique}


CAT_TEXTES = {
 "Roadster": "Guidon large, position droite, pas de carénage. La catégorie la "
             "plus polyvalente, et de loin la plus vendue en France.",
 "Sportive": "Position engagée, carénage intégral, châssis rigide. Conçues pour "
             "la performance avant le confort.",
 "Trail / Aventure": "Grandes roues, longues suspensions, position haute. Le "
                     "compromis qui accepte la route dégradée et le voyage chargé.",
 "Custom / Cruiser": "Selle basse, couple à bas régime, pieds en avant. Le "
                     "plaisir de rouler tranquille plutôt que vite.",
 "Routière / GT": "Protection au vent, confort de selle, capacité de bagages. "
                  "Les machines qui avalent les kilomètres sans fatiguer.",
 "Scooter / Cyclomoteur": "Transmission automatique, plancher plat, rangement "
                          "intégré. La réponse la plus simple à la circulation urbaine.",
 "Tout-terrain": "Légèreté, débattement de suspension et garde au sol. Pensées "
                 "pour le chemin, pas pour le bitume.",
 "Compétition": "Machines de course ou dérivés directs, rarement homologuées "
                "pour la route.",
 "Café racer": "Le style né dans les cafés britanniques des années 1960 : "
               "guidon bracelet, selle monoplace, ligne épurée.",
 "Supermotard": "Un tout-terrain chaussé en jantes de 17 pouces. Vif, léger, "
                "taillé pour la ville et les petites routes.",
}


def hero_categorie(cat, liste):
    fond = _fond(liste)
    img = ('<div class="hero-fond" style="background-image:url(%s)" aria-hidden="true"></div>'
           % e(fond)) if fond else ""
    txt = CAT_TEXTES.get(cat, "")
    return """<header class="hero-cat">
%(img)s
<div class="conteneur hero-corps">
  <p class="hero-eyebrow">Catégorie</p>
  <h1>%(cat)s</h1>
  %(txt)s
  %(chiffres)s
</div>
</header>""" % {"img": img, "cat": e(cat),
                "txt": '<p class="hero-chapo">%s</p>' % e(txt) if txt else "",
                "chiffres": _chiffres(liste)}


def carte_ecole(ecole, liste):
    """Vignette d'ecole : couleurs nationales, photo et signature editoriale."""
    ident = ECOLES.get(slug(ecole), ECOLE_DEFAUT)
    fond = _fond(liste)
    img = ('<div class="ce-img" style="background-image:url(%s)" aria-hidden="true"></div>'
           % e(fond)) if fond else '<div class="ce-img ce-vide" aria-hidden="true"></div>'
    n_a2 = sum(1 for m in liste if m["a2_compatible"] == "oui")
    return ('<a class="carte-ecole" href="%s/ecoles/%s.html" '
            'style="--nat:%s;--nat-nuit:%s">%s%s'
            '<div class="ce-corps">'
            '<span class="ce-pays"><span class="ce-drapeau">%s</span> %s</span>'
            '<span class="ce-nom">École %s</span>'
            '<span class="ce-signature">%s</span>'
            '<span class="ce-chiffres">%d modèles%s</span>'
            '</div></a>'
            % (RACINE, slug(ecole), ident["accent"], ident["accent_nuit"],
               bandes_html(ident), img, ident["emoji"], e(ident["pays"]),
               e(ecole), e(ident["signature"]), len(liste),
               " · %d en A2" % n_a2 if n_a2 else ""))


MAX_LISTE = 120   # au-dela, la page devient trop lourde : on renvoie au comparateur

def page_liste(chemin, titre, h1, intro, liste, fil, prio="0.7", extra_corps="",
               entete=""):
    total = len(liste)
    montres = liste[:MAX_LISTE]
    suite = ""
    if total > MAX_LISTE:
        suite = ('<p class="compteur">%d modèles au total. Les %d plus consultés sont '
                 'affichés ci-dessous, utilisez le <a href="/comparateur.html">comparateur</a> '
                 "pour filtrer l'ensemble.</p>" % (total, MAX_LISTE))
    else:
        suite = ('<p class="compteur">%d modèle%s</p>'
                 % (total, "s" if total > 1 else ""))
    if entete:
        corps = ('%s<div class="conteneur section">%s%s%s</div>'
                 % (entete, extra_corps, suite, grille(montres, 6)))
    else:
        corps = ('<div class="conteneur section"><h1>%s</h1><p class="chapo">%s</p>'
                 '%s%s%s</div>'
                 % (e(h1), intro, extra_corps, suite, grille(montres, 6)))
    desc = re.sub(r"<[^>]+>", "", intro)[:158]
    ecrire(chemin.lstrip("/"), page(titre, desc, corps, SITE_URL + chemin, "", fil))
    enregistrer(chemin, prio)


def page_duel(d):
    a, b = par_id[d["modele_a_id"]], par_id[d["modele_b_id"]]
    na, nb = a["nom_affichage"], b["nom_affichage"]
    titre = "%s ou %s : lequel choisir ?" % (na, nb)
    desc = ("Comparatif %s contre %s : cylindree, puissance, poids, hauteur de "
            "selle et compatibilite permis A2." % (na, nb))

    CRIT = [("Cylindrée", "cylindree_cc", "cm³", 0, None),
            ("Puissance", "puissance_ch", "ch", 1, "haut"),
            ("Couple", "couple_nm", "Nm", 1, "haut"),
            ("Poids", "poids_kg", "kg", 0, "bas"),
            ("Hauteur de selle", "hauteur_selle_mm", "mm", 0, None),
            ("Réservoir", "reservoir_l", "L", 1, "haut"),
            ("Vitesse maximale", "vitesse_max_kmh", "km/h", 0, "haut"),
            ("Empattement", "empattement_mm", "mm", 0, None),
            ("Année", "annee_debut", "", 0, "brut"),
            ("Prix au lancement", "prix_lancement_eur", "€", 0, "bas")]
    lignes = []
    for lib, champ, unite, dec, sens in CRIT:
        va, vb = a[champ], b[champ]
        if not va and not vb:
            continue
        ca = cb = ""
        if sens and va and vb:
            try:
                fa, fb = float(va), float(vb)
                if fa != fb:
                    gagnant_a = (fa > fb) if sens == "haut" else (fa < fb)
                    ca, cb = ("gagne", "") if gagnant_a else ("", "gagne")
            except ValueError:
                pass
        fmt = (lambda v: e(v) if v else "") if sens == "brut" else               (lambda v: num(v, unite, dec))
        if sens == "brut":
            ca = cb = ""
        lignes.append('<tr><th scope="row">%s</th><td class="%s">%s</td>'
                      '<td class="%s">%s</td></tr>'
                      % (lib, ca, fmt(va) or "-", cb, fmt(vb) or "-"))
    tab = ('<div class="tableau-large"><table class="tab-duel"><thead><tr>'
           '<th>Critère</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody>'
           '</table></div>' % (e(na), e(nb), "".join(lignes)))

    # synthese calculee, sans superlatif invente
    pts = []

    def cmp_num(champ, lib, sens):
        try:
            fa, fb = float(a[champ]), float(b[champ])
        except (ValueError, TypeError):
            return
        if fa == fb or max(fa, fb) == 0:
            return
        gagne_a = (fa > fb) if sens == "haut" else (fa < fb)
        if abs(fa - fb) / max(fa, fb) * 100 < 4:
            return
        pts.append("la <strong>%s</strong> %s (%s contre %s)"
                   % (e(na if gagne_a else nb), lib,
                      num(a[champ] if gagne_a else b[champ], "", 0),
                      num(b[champ] if gagne_a else a[champ], "", 0)))

    cmp_num("puissance_ch", "annonce plus de chevaux", "haut")
    cmp_num("poids_kg", "est plus légère", "bas")
    cmp_num("couple_nm", "offre plus de couple", "haut")
    cmp_num("hauteur_selle_mm", "a une selle plus basse", "bas")
    synth = ("<p>Sur le papier : %s.</p>" % " ; ".join(pts[:4])) if pts else ""

    duo = ('<div class="duel"><div>%s</div><div class="duel-vs">contre</div>'
           '<div>%s</div></div>' % (vignette(a, True), vignette(b, True)))

    autres = [x for x in duels_ok if x["categorie"] == d["categorie"]
              and x["duel_id"] != d["duel_id"]][:8]
    bloc = ""
    if autres:
        bloc = ('<h2>Autres duels en %s</h2><ul class="liste-liens">%s</ul>'
                % (e(d["categorie"]),
                   "".join('<li><a href="%s%s"><span>%s ou %s</span></a></li>'
                           % (RACINE, e(x["url"]), e(x["modele_a"]), e(x["modele_b"]))
                           for x in autres)))

    corps = """<div class="conteneur section">
<h1>%(t)s</h1>
<p class="chapo">Comparaison des caractéristiques constructeur. Les deux modèles
appartiennent à la catégorie %(cat)s%(a2)s.</p>
%(duo)s
%(tab)s
%(synth)s
<div class="encart"><p class="encart-titre">Comment lire ce comparatif</p>
<p>Seules les valeurs mesurables sont confrontées ici : elles ne disent rien du
comportement réel, du confort ou du plaisir de conduite. Un essai reste
indispensable avant de choisir. Un tiret signifie que la donnée est absente de
nos sources, pas qu'elle vaut zéro.</p></div>
%(bloc)s
</div>""" % {"t": e(titre), "cat": e(d["categorie"]),
             "a2": (", toutes deux compatibles permis A2" if d["a2"] == "oui" else ""),
             "duo": duo, "tab": tab, "synth": synth, "bloc": bloc}

    fil = [("Accueil", "/"), ("Duels", "/duels/"), ("%s / %s" % (na, nb), None)]
    ecrire(d["url"].lstrip("/"), page(titre, desc, corps, SITE_URL + d["url"], "", fil))
    enregistrer(d["url"], "0.7")


def menu_perso(id_sel, options, libelle, valeur_defaut=""):
    """Menu deroulant custom : bouton + liste toujours ouverte vers le bas.

    'options' est une liste de tuples (valeur, libelle_affiche), y compris
    l'entree par defaut ("", "Toutes"...) quand il y en a une. 'valeur_defaut'
    indique laquelle est presenting au chargement (une chaine vide pour la
    plupart des filtres, mais par exemple "pr" pour le tri par pertinence,
    qui n'a pas de case vide).

    Le <select> reel est conserve, masque, comme source de valeur : le script
    de filtrage (filtrer()) n'a besoin d'aucune modification, il continue de
    lire E.<champ>.value et d'ecouter l'evenement 'change'.
    """
    label_defaut = next((l for v, l in options if v == valeur_defaut), options[0][1])
    opts_select = "".join(
        '<option value="%s"%s>%s</option>'
        % (e(v), " selected" if v == valeur_defaut else "", e(l))
        for v, l in options)
    opts_liste = "".join(
        '<li role="option" data-valeur="%s"%s>%s</li>'
        % (e(v), ' aria-selected="true"' if v == valeur_defaut else "", e(l))
        for v, l in options)
    return """<div class="champ">
<label id="%(id)s-label">%(lib)s</label>
<div class="menu-deroulant" data-cible="%(id)s">
  <button type="button" class="md-bouton" id="%(id)s-btn" aria-haspopup="listbox"
    aria-expanded="false" aria-labelledby="%(id)s-label %(id)s-btn">
    <span class="md-val">%(defaut)s</span>
    <svg class="md-fleche" viewBox="0 0 20 20" aria-hidden="true" focusable="false">
      <path d="M5 7l5 6 5-6" fill="none" stroke="currentColor" stroke-width="1.6"
        stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </button>
  <ul class="md-liste" role="listbox" id="%(id)s-liste" hidden>%(opts_liste)s</ul>
  <select id="%(id)s" class="md-select-reel" tabindex="-1" aria-hidden="true">%(opts_select)s</select>
</div></div>""" % {"id": id_sel, "lib": e(libelle), "defaut": e(label_defaut),
                   "opts_liste": opts_liste, "opts_select": opts_select}


CYL_BANDES = [
    ("0-50", "50 cm³ et moins"), ("51-125", "51 à 125 cm³"),
    ("126-250", "126 à 250 cm³"), ("251-500", "251 à 500 cm³"),
    ("501-750", "501 à 750 cm³"), ("751-1000", "751 à 1000 cm³"),
    ("1001-1300", "1001 à 1300 cm³"), ("1301-999999", "Plus de 1300 cm³"),
]


def page_comparateur():
    ecoles = sorted({m["ecole"] for m in pub if m["ecole"]})
    cats = sorted({m["categorie"] for m in pub if m["categorie"]})
    marques = sorted({m["marque"] for m in pub})
    annees = sorted({int(m["annee_debut"]) for m in pub if m["annee_debut"]}, reverse=True)

    filtres = """<div class="filtres">
<div class="champ"><label for="f-q">Recherche</label>
  <input id="f-q" type="search" placeholder="MT-07, Africa Twin…" autocomplete="off"></div>
%(md_ecole)s
%(md_cat)s
%(md_marque)s
%(md_annee)s
%(md_a2)s
%(md_cyl)s
%(md_selle)s
%(md_tri)s
</div>""" % {
        "md_ecole": menu_perso("f-ecole", [("", "Toutes")] + [(v, v) for v in ecoles], "École"),
        "md_cat": menu_perso("f-cat", [("", "Toutes")] + [(v, v) for v in cats], "Catégorie"),
        "md_marque": menu_perso("f-marque", [("", "Toutes")] + [(v, v) for v in marques], "Marque"),
        "md_annee": menu_perso("f-annee", [("", "Indifférente")]
                               + [(str(a), str(a)) for a in annees], "Année"),
        "md_a2": menu_perso("f-a2", [("", "Indifférent"), ("oui", "Compatible A2")], "Permis A2"),
        "md_cyl": menu_perso("f-cyl", [("", "Indifférente")] + CYL_BANDES, "Cylindrée"),
        "md_selle": menu_perso("f-selle", [("", "Indifférente"), ("780", "780 mm"),
                                           ("810", "810 mm"), ("840", "840 mm")],
                               "Hauteur de selle max."),
        "md_tri": menu_perso("f-tri", [("pr", "Pertinence"), ("an", "Derniers modèles"),
                                       ("p", "Puissance"), ("kg", "Poids"),
                                       ("cy", "Cylindrée"), ("s", "Hauteur de selle")],
                             "Trier par", valeur_defaut="pr"),
    }

    corps = """<div class="conteneur section">
<h1>Comparateur de motos</h1>
<p class="chapo">Filtrez %d modèles par école, catégorie, année, cylindrée, hauteur
de selle et compatibilité permis A2. Le filtrage est instantané et ne demande
aucun compte.</p>
%s
<p class="compteur" id="compteur" role="status"></p>
<div class="grille" id="resultats"></div>
<p class="vide" id="vide" hidden>Aucun modèle ne correspond à ces critères.
Élargissez la sélection.</p>
</div>""" % (len(pub), filtres)

    ecrire("comparateur.html",
           page("Comparateur de motos : filtrer par école, cylindrée et permis A2",
                "Comparez %d motos par école, catégorie, année, cylindrée, hauteur "
                "de selle et compatibilité permis A2." % len(pub),
                corps, SITE_URL + "/comparateur.html", "",
                [("Accueil", "/"), ("Comparateur", None)],
                '<script src="/assets/comparateur.js" defer></script>'))
    enregistrer("/comparateur.html", "0.9")

    slim = [{"n": m["nom_affichage"], "m": m["marque"], "e": m["ecole"],
             "c": m["categorie"], "a2": m["a2_compatible"],
             "cy": float(m["cylindree_cc"] or 0), "p": float(m["puissance_ch"] or 0),
             "kg": float(m["poids_kg"] or 0), "s": float(m["hauteur_selle_mm"] or 0),
             "pr": float(m["priorite"] or 0), "u": m["url"],
             "an": int(m["annee_debut"]) if m["annee_debut"] else 0,
             "af": int(m["annee_fin"]) if m["annee_fin"] else 0,
             "i": m["image_url"] if m["image_utilisable"] == "oui" else ""}
            for m in pub]
    ecrire("assets/data.json",
           json.dumps(slim, ensure_ascii=False, separators=(",", ":")))


JS = r"""
(function(){
  // Menu deroulant maison pour ecole / categorie / marque : la liste est
  // toujours positionnee sous le bouton (voir CSS .md-liste), donc s'ouvre
  // toujours vers le bas, contrairement au <select> natif dont le sens
  // d'ouverture depend de la place disponible a l'ecran.
  document.querySelectorAll('.menu-deroulant').forEach(function(menu){
    var bouton=menu.querySelector('.md-bouton'),
        liste=menu.querySelector('.md-liste'),
        val=menu.querySelector('.md-val'),
        reel=menu.querySelector('.md-select-reel'),
        options=Array.prototype.slice.call(liste.querySelectorAll('li')),
        surlignee=-1;

    function fermer(rendreFocus){
      menu.classList.remove('ouvert');
      liste.hidden=true;
      bouton.setAttribute('aria-expanded','false');
      if(rendreFocus) bouton.focus();
    }
    function ouvrir(){
      menu.classList.add('ouvert');
      liste.hidden=false;
      bouton.setAttribute('aria-expanded','true');
      var i=options.findIndex(function(o){return o.getAttribute('aria-selected')==='true';});
      surligner(i<0?0:i);
    }
    function surligner(i){
      if(surlignee>=0) options[surlignee].classList.remove('md-surlignee');
      surlignee=Math.max(0,Math.min(options.length-1,i));
      options[surlignee].classList.add('md-surlignee');
      options[surlignee].scrollIntoView({block:'nearest'});
    }
    function choisir(opt){
      options.forEach(function(o){o.setAttribute('aria-selected',o===opt?'true':'false');});
      val.textContent=opt.textContent;
      reel.value=opt.getAttribute('data-valeur');
      reel.dispatchEvent(new Event('change',{bubbles:true}));
      fermer(false);
    }

    bouton.addEventListener('click',function(){
      menu.classList.contains('ouvert')?fermer(false):ouvrir();
    });
    options.forEach(function(o){
      o.addEventListener('click',function(){choisir(o);});
      o.addEventListener('mouseenter',function(){surligner(options.indexOf(o));});
    });
    bouton.addEventListener('keydown',function(ev){
      if(ev.key==='ArrowDown'||ev.key==='Enter'||ev.key===' '){
        ev.preventDefault();
        menu.classList.contains('ouvert')?surligner(surlignee+1):ouvrir();
      }else if(ev.key==='ArrowUp'){
        ev.preventDefault();
        if(!menu.classList.contains('ouvert')) ouvrir(); else surligner(surlignee-1);
      }
    });
    liste.addEventListener('keydown',function(ev){
      if(ev.key==='ArrowDown'){ev.preventDefault();surligner(surlignee+1);}
      else if(ev.key==='ArrowUp'){ev.preventDefault();surligner(surlignee-1);}
      else if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();choisir(options[surlignee]);}
      else if(ev.key==='Escape'){ev.preventDefault();fermer(true);}
      else if(ev.key==='Home'){ev.preventDefault();surligner(0);}
      else if(ev.key==='End'){ev.preventDefault();surligner(options.length-1);}
    });
    document.addEventListener('click',function(ev){
      if(!menu.contains(ev.target)) fermer(false);
    });
  });

  var D=[],res=document.getElementById('resultats'),cpt=document.getElementById('compteur'),
      vide=document.getElementById('vide');
  var F={q:'f-q',ecole:'f-ecole',cat:'f-cat',marque:'f-marque',annee:'f-annee',
         a2:'f-a2',cyl:'f-cyl',selle:'f-selle',tri:'f-tri'},E={};
  for(var k in F){E[k]=document.getElementById(F[k]);}

  function norm(s){return (s||'').toLowerCase()
    .normalize('NFD').replace(/[̀-ͯ]/g,'');}

  function carte(m){
    var img=m.i?'<div class="carte-img"><img src="'+m.i+'" alt="'+m.n+
      '" loading="lazy" decoding="async"></div>':'<div class="carte-img"></div>';
    var b=[];
    if(m.cy)b.push(Math.round(m.cy)+' cm³');
    if(m.p)b.push(Math.round(m.p)+' ch');
    if(m.kg)b.push(Math.round(m.kg)+' kg');
    var a2=m.a2==='oui'?'<span class="etiq a2">A2</span>':'';
    return '<a class="carte" href="'+m.u+'">'+img+'<div class="carte-corps">'+
      '<span class="carte-marque">'+m.m+'</span>'+
      '<span class="carte-nom">'+m.n+'</span>'+
      '<span class="carte-specs">'+b.join(' · ')+' '+a2+'</span></div></a>';
  }

  function filtrer(){
    var q=norm(E.q.value.trim()),tri=E.tri.value;
    var out=D.filter(function(m){
      if(q && norm(m.n+' '+m.m).indexOf(q)<0) return false;
      if(E.ecole.value && m.e!==E.ecole.value) return false;
      if(E.cat.value && m.c!==E.cat.value) return false;
      if(E.marque.value && m.m!==E.marque.value) return false;
      if(E.a2.value==='oui' && m.a2!=='oui') return false;
      if(E.annee.value){
        var an=+E.annee.value;
        if(!m.an || m.an>an) return false;
        if(m.af && m.af<an) return false;
      }
      if(E.cyl.value){
        var bornes=E.cyl.value.split('-'),cmin=+bornes[0],cmax=+bornes[1];
        if(!m.cy || m.cy<cmin || m.cy>cmax) return false;
      }
      if(E.selle.value && (!m.s || m.s>+E.selle.value)) return false;
      return true;
    });
    out.sort(function(x,y){
      if(tri==='kg'||tri==='s'){
        var a=x[tri]||1e9,b=y[tri]||1e9; return a-b;
      }
      return (y[tri]||0)-(x[tri]||0);
    });
    cpt.textContent=out.length+(out.length>1?' modèles trouvés':' modèle trouvé');
    vide.hidden=out.length>0;
    res.innerHTML=out.slice(0,180).map(carte).join('');
    if(out.length>180){
      cpt.textContent=out.length+' modèles trouvés, les 180 premiers sont affichés';
    }
  }

  for(var k2 in E){
    E[k2].addEventListener(E[k2].tagName==='INPUT'?'input':'change',filtrer);
  }

  fetch('/assets/data.json').then(function(r){return r.json();}).then(function(j){
    D=j; filtrer();
  }).catch(function(){
    cpt.textContent='Impossible de charger les données. Rechargez la page.';
  });
})();
"""


def page_accueil():
    top = sorted(pub, key=lambda x: -float(x["priorite"] or 0))[:12]
    a2 = [m for m in pub if m["a2_compatible"] == "oui"][:8]
    duels_top = duels_ok[:9]

    ecoles_html = "".join(
        carte_ecole(k, v)
        for k, v in sorted(par_ecole.items(), key=lambda x: -len(x[1]))[:8])
    cats_html = "".join(
        '<li><a href="/categories/%s.html"><span>%s</span>'
        '<span class="n">%d</span></a></li>' % (slug(k), e(k), len(v))
        for k, v in sorted(par_cat.items(), key=lambda x: -len(x[1])))
    duels_html = "".join(
        '<li><a href="%s"><span>%s ou %s</span></a></li>'
        % (e(d["url"]), e(d["modele_a"]), e(d["modele_b"])) for d in duels_top)

    vedette = next((m for m in top
                    if (m.get("image_vignette") or m.get("image_url"))
                    and m.get("image_utilisable") == "oui"), None)
    fond_accueil = ""
    credit_accueil = ""
    if vedette:
        fond_accueil = ('<div class="hero-fond" style="background-image:url(%s)" '
                        'aria-hidden="true"></div>'
                        % e(vedette.get("image_vignette") or vedette["image_url"]))
        credit_accueil = ('<p class="hero-credit">En photo : <a href="%s%s">%s</a>'
                          '%s</p>'
                          % (RACINE, e(vedette["url"]), e(vedette["nom_affichage"]),
                             ", © " + e(vedette["image_auteur"])
                             if vedette.get("image_auteur") else ""))

    corps = """<section class="hero-accueil">
%(fond)s
<div class="conteneur hero-corps">
<p class="hero-eyebrow">Annuaire moto</p>
<h1>Les fiches techniques moto, sans le bruit</h1>
<p class="hero-chapo">%(n)d modèles documentés, un comparateur qui filtre vraiment, et des
duels chiffrés pour trancher entre deux motos. Compatibilité permis A2 calculée
pour chaque machine.</p>
<div class="chiffres">
  <div class="chiffre"><span class="v">%(n)d</span><span class="l">modèles</span></div>
  <div class="chiffre"><span class="v">%(m)d</span><span class="l">marques</span></div>
  <div class="chiffre"><span class="v">%(a2)d</span><span class="l">compatibles A2</span></div>
  <div class="chiffre"><span class="v">%(d)d</span><span class="l">duels</span></div>
</div>
<p class="hero-actions">
  <a class="bouton" href="%(racine)s/comparateur.html">Ouvrir le comparateur</a>
  <a class="bouton-secondaire" href="%(racine)s/guides/">Voir les guides d'achat</a>
</p>
%(credit)s
</div>
</section>

<div class="conteneur section">
<h2>Guides d&rsquo;achat</h2>
<p class="chapo">Des sélections argumentées, croisant caractéristiques
constructeur et retours de motards qui roulent ces machines.</p>
<div class="grille-guides-index">%(guides)s</div>

<h2>Les modèles les plus consultés</h2>
%(top)s

<h2>Trancher entre deux motos</h2>
<ul class="liste-liens">%(duels)s</ul>

<h2>Par école</h2>
<p class="chapo">Chaque pays a sa façon de concevoir une moto. La fiabilité
japonaise, le caractère italien, le twin américain : trois philosophies, trois
manières de rouler.</p>
<div class="grille-ecoles">%(ecoles)s</div>

<h2>Par catégorie</h2>
<ul class="liste-liens">%(cats)s</ul>

<h2>Accessibles au permis A2</h2>
<p class="chapo">Moins de 35 kW et un rapport poids/puissance sous 0,2 kW/kg :
le calcul est fait pour chaque modèle à partir des données constructeur.</p>
%(bloca2)s
</div>""" % {"n": len(pub), "m": len(par_marque), "d": len(duels_ok),
             "a2": sum(1 for m in pub if m["a2_compatible"] == "oui"),
             "top": grille(top, 6), "duels": duels_html,
             "guides": "".join(
                 '<a class="carte-guide-lien" href="/guides/%s.html">'
                 '<span class="cgl-titre">%s</span>'
                 '<span class="cgl-desc">%s</span></a>'
                 % (e(x["slug"]), e(x["h1"]), e(x["desc"])) for x in GUIDES),
             "ecoles": ecoles_html, "cats": cats_html, "bloca2": grille(a2),
             "fond": fond_accueil, "credit": credit_accueil, "racine": RACINE}

    ecrire("index.html", page("%s, fiches techniques, comparateur et duels moto"
                              % SITE_NOM, SITE_DESC, corps, SITE_URL + "/"))
    enregistrer("/", "1.0")


def pages_hubs():
    # marques
    li = "".join('<li><a href="/marques/%s.html"><span>%s</span>'
                 '<span class="n">%d</span></a></li>' % (slug(k), e(k), len(v))
                 for k, v in sorted(par_marque.items()))
    corps = ('<div class="conteneur section"><h1>Toutes les marques</h1>'
             '<p class="chapo">%d constructeurs représentés.</p>'
             '<ul class="liste-liens">%s</ul></div>' % (len(par_marque), li))
    ecrire("marques/index.html",
           page("Marques de motos : %d constructeurs" % len(par_marque),
                "Toutes les marques de motos documentées, du Japon à l'Italie.",
                corps, SITE_URL + "/marques/", "",
                [("Accueil", "/"), ("Marques", None)]))
    enregistrer("/marques/", "0.8")

    for marque, liste in par_marque.items():
        s = slug(marque)
        ecole = liste[0]["ecole"]
        intro = ("Les %d modèles %s documentés, avec leurs caractéristiques "
                 "techniques et leur compatibilité permis A2."
                 % (len(liste), e(marque)))
        if ecole:
            intro += " Marque de l'école %s." % e(ecole)
        page_liste("/marques/%s.html" % s,
                   "Motos %s : tous les modèles et fiches techniques" % marque,
                   "Motos %s" % marque, intro, liste,
                   [("Accueil", "/"), ("Marques", "/marques/"), (marque, None)], "0.8")

    # ecoles
    corps = ('<div class="conteneur section"><h1>Les écoles de la moto</h1>'
             '<p class="chapo">Japonaise, italienne, américaine, britannique : '
             'chaque tradition industrielle a façonné une manière de concevoir '
             'une machine. Un classement que personne d\'autre ne propose.</p>'
             '<div class="grille-ecoles">%s</div></div>'
             % "".join(carte_ecole(k, v)
                       for k, v in sorted(par_ecole.items(), key=lambda x: -len(x[1]))))
    ecrire("ecoles/index.html",
           page("Les écoles de la moto : japonaise, italienne, américaine",
                "Classement des motos par école nationale : japonaise, italienne, "
                "américaine, britannique, allemande.",
                corps, SITE_URL + "/ecoles/", "",
                [("Accueil", "/"), ("Écoles", None)]))
    enregistrer("/ecoles/", "0.9")

    for ecole, liste in par_ecole.items():
        s = slug(ecole)
        ident = ECOLES.get(s, ECOLE_DEFAUT)
        intro = ident["texte"] or ("Les modèles de l'école %s." % e(ecole))
        intro += (" %d modèles répertoriés, de %s." %
                  (len(liste), ", ".join(sorted({m["marque"] for m in liste})[:6])))
        page_liste("/ecoles/%s.html" % s,
                   "Motos de l'école %s : modèles et caractéristiques" % ecole,
                   "L'école %s" % ecole, intro, liste,
                   [("Accueil", "/"), ("Écoles", "/ecoles/"), (ecole.capitalize(), None)],
                   "0.85", entete=hero_ecole(ecole, liste))

    # categories
    for cat, liste in par_cat.items():
        s = slug(cat)
        intro = (CAT_TEXTES.get(cat, "") + " ") if CAT_TEXTES.get(cat) else ""
        intro += ("%d modèles classés par pertinence. Filtrez par cylindrée et "
                  "hauteur de selle dans le "
                  "<a href=\"/comparateur.html\">comparateur</a>." % len(liste))
        page_liste("/categories/%s.html" % s,
                   "%s : tous les modèles et fiches techniques" % cat,
                   cat, intro, liste,
                   [("Accueil", "/"), (cat, None)], "0.8",
                   entete=hero_categorie(cat, liste))

    # duels : entree par modele
    impliques = {}
    for d in duels_ok:
        for cle in ("modele_a_id", "modele_b_id"):
            m = par_id[d[cle]]
            impliques[m["modele_id"]] = m

    par_marque_sel = defaultdict(list)
    for m in impliques.values():
        par_marque_sel[m["marque"]].append(m)
    groupes = []
    for marque in sorted(par_marque_sel):
        opts = "".join('<option value="%s">%s</option>'
                       % (e(m["modele_id"]), e(m["nom_affichage"]))
                       for m in sorted(par_marque_sel[marque],
                                       key=lambda x: x["nom_affichage"]))
        groupes.append('<optgroup label="%s">%s</optgroup>' % (e(marque), opts))

    selecteur = """<div class="selecteur">
  <label for="d-modele">Quelle moto vous intéresse ?</label>
  <select id="d-modele">
    <option value="">Choisissez un modèle</option>
    %s
  </select>
  <p class="selecteur-aide">%d modèles ont au moins un duel.
     Sélectionnez-en un pour voir uniquement ses comparatifs.</p>
</div>""" % ("".join(groupes), len(impliques))

    # rendu statique : lisible sans JavaScript et indexable
    defaut = "".join(carte_duel(d) for d in duels_ok[:24])

    corps = """<div class="conteneur section">
<h1>Duels</h1>
<p class="chapo">%(n)d comparaisons chiffrées entre deux motos de même catégorie et
de cylindrée voisine. Choisissez la moto qui vous intéresse pour voir directement
les machines auxquelles elle se mesure.</p>
%(sel)s
<h2 id="titre-res">Les duels les plus consultés</h2>
<div class="grille-duels" id="res-duels">%(def)s</div>
<p class="vide" id="d-vide" hidden>Aucun duel pour ce modèle.</p>
<div class="encart"><p class="encart-titre">Comment sont formés les duels</p>
<p>Deux motos ne sont confrontées que si elles partagent la catégorie, une cylindrée
proche à 25 %% près et le même statut permis A2. Chaque modèle est limité à six
duels pour éviter les comparaisons redondantes.</p></div>
</div>""" % {"n": len(duels_ok), "sel": selecteur, "def": defaut}

    ecrire("duels/index.html",
           page("Duels moto : comparer deux modèles face à face",
                "Choisissez votre moto et découvrez à quelles machines elle se "
                "compare : puissance, poids, hauteur de selle, permis A2.",
                corps, SITE_URL + "/duels/", "",
                [("Accueil", "/"), ("Duels", None)],
                '<script src="/assets/duels.js" defer></script>'))
    enregistrer("/duels/", "0.9")

    # donnees pour le filtrage cote navigateur
    charge = []
    for d in duels_ok:
        a, b = par_id[d["modele_a_id"]], par_id[d["modele_b_id"]]
        charge.append({
            "u": d["url"], "c": d["categorie"], "a2": d["a2"],
            "ia": a["modele_id"], "ib": b["modele_id"],
            "a": _cote(a), "b": _cote(b)})
    ecrire("assets/duels.json",
           json.dumps(charge, ensure_ascii=False, separators=(",", ":")))


JS_DUELS = r"""
(function(){
  var sel=document.getElementById('d-modele'),
      res=document.getElementById('res-duels'),
      titre=document.getElementById('titre-res'),
      vide=document.getElementById('d-vide'),
      D=null;

  function cote(c){
    var img=c.i?'<img src="'+c.i+'" alt="'+c.n+'" loading="lazy" decoding="async">':'';
    var b=[];
    if(c.cy)b.push(Math.round(c.cy)+' cm³');
    if(c.p)b.push(Math.round(c.p)+' ch');
    if(c.kg)b.push(Math.round(c.kg)+' kg');
    return '<div class="cd-cote"><div class="cd-img">'+img+'</div>'+
      '<span class="cd-marque">'+c.m+'</span>'+
      '<span class="cd-nom">'+c.n+'</span>'+
      '<span class="cd-spec">'+b.join(' · ')+'</span></div>';
  }
  function carte(d){
    var t='<span class="etiq">'+d.c+'</span>';
    if(d.a2==='oui')t+=' <span class="etiq a2">A2</span>';
    return '<a class="carte-duel" href="'+d.u+'">'+
      '<div class="cd-cotes">'+cote(d.a)+'<span class="cd-vs">contre</span>'+
      cote(d.b)+'</div><div class="cd-pied">'+t+'</div></a>';
  }
  function afficher(id){
    if(!D)return;
    if(!id){
      titre.textContent='Les duels les plus consultés';
      res.innerHTML=D.slice(0,24).map(carte).join('');
      vide.hidden=true;
      return;
    }
    var lot=D.filter(function(d){return d.ia===id||d.ib===id;});
    // la moto choisie toujours a gauche
    lot=lot.map(function(d){
      return d.ib===id?{u:d.u,c:d.c,a2:d.a2,ia:d.ib,ib:d.ia,a:d.b,b:d.a}:d;
    });
    var nom=lot.length?lot[0].a.n:sel.options[sel.selectedIndex].text;
    titre.textContent=lot.length+(lot.length>1?' duels pour la ':' duel pour la ')+nom;
    res.innerHTML=lot.map(carte).join('');
    vide.hidden=lot.length>0;
    if(history.replaceState){
      history.replaceState(null,'',id?('#'+id):location.pathname);
    }
  }
  sel.addEventListener('change',function(){afficher(sel.value);});

  fetch('/assets/duels.json').then(function(r){return r.json();}).then(function(j){
    D=j;
    var h=location.hash.slice(1);
    if(h){sel.value=h;}
    if(sel.value){afficher(sel.value);}
  });
})();
"""


def fichiers_techniques():
    ecrire("assets/style.css", CSS)
    ecrire("assets/duels.js", JS_DUELS)
    ecrire("assets/comparateur.js", JS)
    ecrire("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE_URL)
    items = "".join(
        "<url><loc>%s%s</loc><priority>%s</priority></url>"
        % (SITE_URL, html.escape(u), p) for u, p in urls)
    ecrire("sitemap.xml",
           '<?xml version="1.0" encoding="UTF-8"?>'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>'
           % items)




# ================================================================= GUIDES
def _fiche_lien(modele_id):
    """Fiche liee a un modele cite dans un guide.

    Appariement STRICT par identifiant. Une correspondance approximative sur le
    nom renverrait vers la mauvaise machine : 'Honda CB500 Hornet' (2023) avait
    ainsi ete lie a la CB500 Four de 1971.
    """
    if not modele_id:
        return None
    m = par_id.get(modele_id)
    if not m:
        print("  ! guide : identifiant inconnu '%s'" % modele_id)
        return None
    # un guide d'achat 2026 ne doit jamais pointer vers une machine ancienne
    # homonyme (la Z650 de 1977, la CB500 Four de 1971...)
    try:
        an = int(m["annee_debut"]) if m["annee_debut"] else 0
    except ValueError:
        an = 0
    if an and an < 2005:
        print("  ! guide : lien refuse vers '%s' (%d), trop ancien"
              % (m["nom_affichage"], an))
        return None
    return m


def carte_guide(c, rang):
    m = _fiche_lien(c.get("modele"))
    img = ""
    if m and (m.get("image_vignette") or m["image_url"]) and m["image_utilisable"] == "oui":
        img = ('<div class="cg-img"><img src="%s" alt="%s" loading="lazy" '
               'decoding="async"></div>'
               % (e(m.get("image_vignette") or m["image_url"]), e(c["nom"])))
    chiffres = "".join(
        '<div><span class="cg-l">%s</span><span class="cg-v">%s</span></div>' % (lib, e(val))
        for lib, val in (("Prix", c.get("prix")), ("Puissance", c.get("puissance")),
                         ("Poids", c.get("poids"))) if val)
    forts = "".join("<li>%s</li>" % x for x in c.get("forts", []))
    res = "".join("<li>%s</li>" % x for x in c.get("reserves", []))
    if m:
        lien = ('<a class="cg-lien" href="%s%s">Voir la fiche technique complète</a>'
                % (RACINE, e(m["url"])))
    else:
        lien = ('<span class="cg-absent">Fiche technique pas encore disponible '
                'sur le site</span>')
    return """<article class="carte-guide" id="%(id)s">
  <div class="cg-tete"><span class="cg-rang">%(rang)02d</span>
    <h3>%(nom)s</h3></div>
  %(img)s
  <p class="cg-pour"><strong>Pour qui :</strong> %(pour)s</p>
  <div class="cg-chiffres">%(chiffres)s</div>
  <div class="cg-listes">
    <div><p class="cg-sl">Ce qui plaît</p><ul class="cg-plus">%(forts)s</ul></div>
    <div><p class="cg-sl">Ce qui coince</p><ul class="cg-moins">%(res)s</ul></div>
  </div>
  <p class="cg-verdict">%(verdict)s</p>
  %(lien)s
</article>""" % {"id": slug(c["nom"]), "rang": rang, "nom": e(c["nom"]),
                 "img": img, "pour": c.get("pour", ""), "chiffres": chiffres,
                 "forts": forts, "res": res,
                 "verdict": e(c.get("verdict", "")), "lien": lien}


def page_guide(g):
    corps = []
    sommaire = []
    for s in g["sections"]:
        aid = slug(s["h2"])
        sommaire.append('<li><a href="#%s">%s</a></li>' % (aid, e(s["h2"])))
        corps.append('<h2 id="%s">%s</h2>' % (aid, e(s["h2"])))
        if s.get("html"):
            corps.append(s["html"])
        if s.get("cartes"):
            corps.append('<div class="grille-guide">%s</div>'
                         % "".join(carte_guide(c, i + 1)
                                   for i, c in enumerate(s["cartes"])))

    faq_html = ""
    if g.get("faq"):
        items = "".join(
            '<details class="faq"><summary>%s</summary><p>%s</p></details>'
            % (e(q), e(r)) for q, r in g["faq"])
        faq_html = '<h2 id="questions-frequentes">Questions fréquentes</h2>%s' % items
        sommaire.append('<li><a href="#questions-frequentes">Questions fréquentes</a></li>')

    src = "".join('<li><a href="%s" rel="nofollow">%s</a></li>' % (e(u), e(t))
                  for t, u in g.get("sources", []))
    sources_html = ('<h2 id="sources">Sources</h2>'
                    '<p class="mention">Les impressions de conduite citées dans ce '
                    'guide proviennent des essais et retours de propriétaires '
                    'ci-dessous. Elles sont résumées, jamais recopiées.</p>'
                    '<ol class="sources">%s</ol>' % src)

    ld = {"@context": "https://schema.org", "@type": "Article",
          "headline": g["titre"], "description": g["desc"],
          "inLanguage": "fr-FR", "dateModified": "2026-08-25",
          "author": {"@type": "Organization", "name": SITE_NOM},
          "publisher": {"@type": "Organization", "name": SITE_NOM}}
    extra = ('<script type="application/ld+json">%s</script>'
             % json.dumps(ld, ensure_ascii=False))
    if g.get("faq"):
        fq = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": r}}
                             for q, r in g["faq"]]}
        extra += ('<script type="application/ld+json">%s</script>'
                  % json.dumps(fq, ensure_ascii=False))

    html_corps = """<div class="conteneur section guide">
<p class="guide-meta">Guide d'achat · Mis à jour le %(maj)s</p>
<h1>%(h1)s</h1>
<p class="chapo">%(chapo)s</p>
<div class="encart"><p class="encart-titre">Notre méthode</p>%(methode)s</div>
<nav class="sommaire" aria-label="Sommaire"><p class="sommaire-t">Au sommaire</p>
<ol>%(sommaire)s</ol></nav>
%(corps)s
%(faq)s
%(sources)s
</div>""" % {"maj": DATE_MAJ, "h1": e(g["h1"]), "chapo": e(g["chapo"]),
             "methode": METHODE, "sommaire": "".join(sommaire),
             "corps": "".join(corps), "faq": faq_html, "sources": sources_html}

    url = "/guides/%s.html" % g["slug"]
    ecrire(url.lstrip("/"),
           page(g["titre"], g["desc"], html_corps, SITE_URL + url, extra,
                [("Accueil", "/"), ("Guides d'achat", "/guides/"), (g["h1"], None)]))
    enregistrer(url, "0.95")


EDITEUR_NOM = "Daniel Krisha"
EDITEUR_EMAIL = "cylindree.moto.comparateur@gmail.com"


def page_legal():
    corps_ml = """<div class="conteneur section article">
<h1>Mentions légales</h1>

<h2>Éditeur du site</h2>
<p>Le site %(site)s est édité à titre personnel, non professionnel, par :</p>
<p>%(nom)s<br>
Contact : <a href="mailto:%(email)s">%(email)s</a></p>
<p>S'agissant d'un particulier (personne physique) et non d'une activité
commerciale immatriculée, l'adresse postale n'est pas publiée ici,
conformément à la loi n°2004-575 du 21 juin 2004 pour la confiance dans
l'économie numérique (LCEN) ; elle peut être communiquée à l'hébergeur sur
demande d'une autorité judiciaire compétente.</p>
<p>Directeur de la publication : %(nom)s.</p>

<h2>Hébergement</h2>
<p>Le site est hébergé par Vercel Inc. (États-Unis) — <a href="https://vercel.com"
rel="nofollow">vercel.com</a>. Le nom de domaine est enregistré chez IONOS.</p>

<h2>Propriété intellectuelle et contenu</h2>
<p>Les fiches techniques du site s'appuient sur des données issues de
Wikipédia, publiées sous licence
<a href="https://creativecommons.org/licenses/by-sa/4.0/deed.fr" rel="license nofollow">CC&nbsp;BY-SA&nbsp;4.0</a>.
Chaque fiche renvoie vers son ou ses articles sources. Les photographies
conservent la licence et l'auteur indiqués sur la fiche concernée.</p>
<p>Le reste du contenu éditorial (guides d'achat, mise en forme, comparateur,
duels) est la production propre du site et ne peut être reproduit sans
autorisation, hors citation courte avec lien vers la source.</p>

<h2>Liens affiliés et publicité</h2>
<p>Le site contient des liens affiliés (notamment le programme Amazon
Partenaires) : un achat réalisé via ces liens peut générer une commission,
sans surcoût pour l'acheteur. Le site diffuse également des publicités via
Google AdSense. Voir la <a href="/politique-de-confidentialite.html">politique
de confidentialité</a> pour le détail des cookies utilisés.</p>

<h2>Responsabilité</h2>
<p>Les caractéristiques techniques, prix et informations présentés sont
fournis à titre indicatif et peuvent comporter des erreurs ou être obsolètes.
Vérifiez toute information auprès du constructeur ou d'un concessionnaire
avant un achat. L'éditeur ne saurait être tenu responsable des décisions
prises sur la seule base du contenu de ce site.</p>

<h2>Contact</h2>
<p>Pour toute question, signalement d'erreur ou demande relative aux données
personnelles : <a href="mailto:%(email)s">%(email)s</a>.</p>
</div>""" % {"site": e(SITE_NOM), "nom": e(EDITEUR_NOM), "email": e(EDITEUR_EMAIL)}

    ecrire("mentions-legales.html",
           page("Mentions légales", "Mentions légales du site %s : éditeur, "
                "hébergement, propriété intellectuelle et contact." % SITE_NOM,
                corps_ml, SITE_URL + "/mentions-legales.html", "",
                [("Accueil", "/"), ("Mentions légales", None)]))
    enregistrer("/mentions-legales.html", "0.2")

    corps_pc = """<div class="conteneur section article">
<h1>Politique de confidentialité</h1>
<p class="chapo">Mise à jour : %(maj)s.</p>

<h2>Qui traite vos données ?</h2>
<p>%(nom)s, éditeur du site %(site)s (voir les
<a href="/mentions-legales.html">mentions légales</a>). Pour toute question :
<a href="mailto:%(email)s">%(email)s</a>.</p>

<h2>Données collectées et cookies</h2>
<p><strong>Mesure d'audience — Google Analytics (GA4).</strong> Utilisé pour
savoir combien de pages sont consultées et par où arrivent les visiteurs.
Dépose des cookies et traite votre adresse IP (traitée par Google).</p>
<p><strong>Publicité — Google AdSense.</strong> Diffuse des annonces sur le
site et peut déposer des cookies publicitaires, y compris pour proposer des
annonces personnalisées selon votre navigation, sur ce site et d'autres.</p>
<p><strong>Liens affiliés — Amazon Partenaires.</strong> Les liens vers des
produits Amazon contiennent un identifiant d'affiliation permettant de
tracer qu'un achat provient de ce site ; Amazon peut déposer un cookie de
suivi lors du clic.</p>
<p>Aucun compte utilisateur, formulaire ou newsletter n'existe sur ce site à
ce jour : il n'y a pas d'autre collecte de données personnelles que celle
décrite ci-dessus.</p>

<h2>Base légale et durée de conservation</h2>
<p>Les cookies de mesure d'audience et de publicité sont soumis à votre
consentement. Les paramètres de votre navigateur permettent de refuser ou
supprimer ces cookies à tout moment ; les outils de gestion des annonces de
Google (<a href="https://myadcenter.google.com/" rel="nofollow">Ad Center
Google</a>) permettent également de limiter la personnalisation
publicitaire. Les données conservées par Google le sont selon la durée
définie par leurs propres politiques.</p>

<h2>Vos droits</h2>
<p>Conformément au Règlement général sur la protection des données (RGPD)
et à la loi Informatique et Libertés, vous disposez d'un droit d'accès, de
rectification, d'opposition et de suppression des données vous concernant.
Pour l'exercer : <a href="mailto:%(email)s">%(email)s</a>. Vous pouvez
également introduire une réclamation auprès de la CNIL
(<a href="https://www.cnil.fr" rel="nofollow">cnil.fr</a>).</p>
</div>""" % {"maj": DATE_MAJ, "nom": e(EDITEUR_NOM), "site": e(SITE_NOM),
             "email": e(EDITEUR_EMAIL)}

    ecrire("politique-de-confidentialite.html",
           page("Politique de confidentialité", "Politique de confidentialité "
                "du site %s : cookies, mesure d'audience, publicité et droits "
                "RGPD." % SITE_NOM, corps_pc,
                SITE_URL + "/politique-de-confidentialite.html", "",
                [("Accueil", "/"), ("Politique de confidentialité", None)]))
    enregistrer("/politique-de-confidentialite.html", "0.2")


def page_guides_index():
    li = []
    for g in GUIDES:
        li.append('<a class="carte-guide-lien" href="/guides/%s.html">'
                  '<span class="cgl-titre">%s</span>'
                  '<span class="cgl-desc">%s</span></a>'
                  % (e(g["slug"]), e(g["h1"]), e(g["desc"])))
    corps = ('<div class="conteneur section"><h1>Guides d&rsquo;achat</h1>'
             '<p class="chapo">Des sélections argumentées, croisant les '
             'caractéristiques constructeur et les retours de motards qui '
             'roulent ces machines. Sans essai maison : nous le disons '
             'clairement sur chaque page.</p>'
             '<div class="grille-guides-index">%s</div></div>' % "".join(li))
    ecrire("guides/index.html",
           page("Guides d'achat moto : bien choisir sa machine",
                "Guides d'achat moto : permis A2, première moto, routière de "
                "voyage. Sélections argumentées et retours de propriétaires.",
                corps, SITE_URL + "/guides/", "",
                [("Accueil", "/"), ("Guides d'achat", None)]))
    enregistrer("/guides/", "0.95")


# ----------------------------------------------------------------- execution
if os.path.isdir(SITE):
    shutil.rmtree(SITE)

os.makedirs(os.path.join(SITE, "assets"), exist_ok=True)
for _f in ("favicon.png", "og-image.jpg"):
    shutil.copy(os.path.join(BASE, "scripts", "assets_source", _f),
                os.path.join(SITE, "assets", _f))

print("Generation des fiches modeles...")
for m in pub:
    page_modele(m)
print("Generation des hubs...")
pages_hubs()
print("Generation des duels...")
for d in duels_ok:
    page_duel(d)
print("Generation du comparateur...")
page_comparateur()
print("Generation des guides...")
page_legal()
page_guides_index()
for _g in GUIDES:
    page_guide(_g)
page_accueil()
fichiers_techniques()

n_fic = sum(len(files) for _, _, files in os.walk(SITE))
taille = sum(os.path.getsize(os.path.join(r, f))
             for r, _, fs in os.walk(SITE) for f in fs)
print("\n=== SITE GENERE ===")
print("  %d pages HTML" % len(urls))
print("  %d fichiers, %.1f Mo" % (n_fic, taille / 1e6))
print("  dossier : %s" % os.path.abspath(SITE))
