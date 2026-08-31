# -*- coding: utf-8 -*-
"""
Liens d'affiliation des guides d'achat.

Un seul endroit a modifier pour tout le site. Tant qu'un lien n'a pas
d'URL reelle (champ "url": None), il n'est PAS affiche : aucun faux lien,
aucun placeholder casse ne part en production.

Pour activer un programme :
  1. S'inscrire (voir PROGRAMMES ci-dessous pour le lien d'inscription).
  2. Recuperer ton lien tracke / ton identifiant affilie.
  3. Coller l'URL complete dans le champ "url" de l'entree concernee.
  4. Relancer : python scripts/20_site.py

Rien d'autre a toucher : les guides appellent bloc_achat(...) et le rendu
s'ajuste automatiquement au nombre de liens reellement actifs.
"""

# ------------------------------------------------------------- programmes
# Reseaux a rejoindre. "inscription" est le point d'entree public de
# chaque enseigne/reseau ; certains (Awin, Effiliation) sont des
# plateformes qui donnent ensuite acces a plusieurs enseignes a la fois.
PROGRAMMES = {
 "motoblouz":   {"nom": "Motoblouz", "inscription": "https://www.motoblouz.com/affiliation",
                 "commission": "4 a 8 %", "delai": "validation sous 48h en general"},
 "dafy":        {"nom": "Dafy Moto", "inscription": "https://www.awin.com/fr",
                 "commission": "3 a 6 %", "delai": "via le reseau Awin"},
 "icasque":     {"nom": "iCasque", "inscription": "https://www.icasque.com/affiliation",
                 "commission": "4 a 7 %", "delai": "variable"},
 "amazon":      {"nom": "Amazon Partenaires", "inscription": "https://partenaires.amazon.fr",
                 "commission": "1 a 4 % (bricolage/sport)", "delai": "immediat, sans minimum de trafic"},
 "allopneus":   {"nom": "Allopneus", "inscription": "https://www.awin.com/fr",
                 "commission": "2 a 5 %", "delai": "via le reseau Awin"},
 "lelynx":      {"nom": "LeLynx (assurance)", "inscription": "https://www.awin.com/fr",
                 "commission": "1 a 10 € par lead", "delai": "via le reseau Awin"},
}

# ------------------------------------------------------------- liens
# cle -> {"label", "programme" (cle de PROGRAMMES), "url" (None = inactif)}
LIENS = {
 "casque":          {"label": "Comparer les casques",        "programme": "icasque",  "url": None},
 "casque-amazon":   {"label": "Casque LS2 Advant Carbon modulable sur Amazon", "programme": "amazon",
                     "url": "https://www.amazon.fr/dp/B0BRQ828ZC?tag=66996600-20&linkCode=ll2&linkId=ea928c9e3f9620cfa29e5cf76e8c19b9"},
 "blouson":         {"label": "Voir les blousons",            "programme": "motoblouz","url": None},
 "gants":           {"label": "Voir les gants homologués",    "programme": "motoblouz","url": None},
 "bottes":          {"label": "Voir les bottes moto",         "programme": "motoblouz","url": None},
 "pantalon":        {"label": "Voir les pantalons renforcés", "programme": "motoblouz","url": None},
 "airbag":          {"label": "Voir les gilets airbag",       "programme": "motoblouz","url": None},
 "pneus":           {"label": "Comparer les pneus",           "programme": "allopneus","url": None},
 "bouchons":        {"label": "Voir les bouchons filtrants",  "programme": "motoblouz","url": None},
 "bouchons-amazon": {"label": "Bouchons EarPeace sur Amazon", "programme": "amazon",
                     "url": "https://www.amazon.fr/dp/B076VVV5WJ?tag=66996600-20&linkCode=ll2&linkId=918e9aeb67aec6622399acc4f98c49f2"},
 "bouchons-amazon-2": {"label": "Bouchons Naiicute sur Amazon", "programme": "amazon",
                     "url": "https://www.amazon.fr/dp/B0CJ7BZWKS?tag=66996600-20&linkCode=ll2&linkId=92c5b9960aa07beba7aeca6273d97f35"},
 "assurance":       {"label": "Comparer les assurances moto", "programme": "lelynx",   "url": None},
}


def _lien_html(cle):
    d = LIENS.get(cle)
    if not d or not d.get("url"):
        return ""
    return ('<a class="lien-affilie" href="%s" rel="sponsored noopener" target="_blank">'
            '%s</a>' % (d["url"], d["label"]))


def bloc_achat(cles, titre="Où l'acheter"):
    """Encart d'achat : ne rend RIEN tant qu'aucun lien de la liste n'est actif.

    'cles' est une liste de cles de LIENS. L'encart est saute silencieusement
    si aucune n'a d'URL renseignee : jamais de boite vide ni de lien mort.
    """
    liens = [_lien_html(c) for c in cles]
    liens = [l for l in liens if l]
    if not liens:
        return ""
    return ('<div class="encart encart-achat"><p class="encart-titre">%s</p>'
            '<div class="liens-affilies">%s</div>'
            '<p class="mention-affilie">Liens affiliés : nous touchons une '
            'commission sur les achats réalisés via ces liens, sans surcoût '
            'pour vous.</p></div>' % (titre, "".join(liens)))
