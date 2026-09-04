# -*- coding: utf-8 -*-
"""
Contenu editorial des guides d'achat.

Separe du generateur : c'est ici qu'on ecrit et qu'on corrige les textes,
sans toucher au code. Chaque guide est un dictionnaire.

Regle de redaction appliquee :
  - aucun ressenti de conduite invente. Les impressions rapportees viennent
    d'essais et de retours de proprietaires publies, resumes et references
    en fin de guide. Rien n'est recopie mot pour mot.
  - les prix sont indicatifs, dates, et donnes en tarif public constate.
  - quand une donnee manque, on l'ecrit.
"""

from affiliation import bloc_achat

DATE_MAJ = "25 août 2026"

# --- briques reutilisables ------------------------------------------------

METHODE = """<p>Ce guide ne repose pas sur un essai que nous aurions conduit :
nous ne roulons pas les motos que nous décrivons. Il croise trois sources,
les caractéristiques constructeur de notre base, les essais publiés par la
presse spécialisée, et les retours de propriétaires sur les forums français.
Les impressions de conduite rapportées ici sont donc <strong>celles des
motards qui roulent ces machines</strong>, résumées et référencées en fin de
page. Les points faibles sont mentionnés au même titre que les qualités.</p>"""

REGLE_A2 = """<p>Une moto est autorisée au permis A2 si elle respecte
<strong>trois conditions cumulatives</strong> :</p>
<ul class="tick">
<li>puissance maximale de <strong>35 kW</strong>, soit 47,5 ch ;</li>
<li>rapport puissance/poids inférieur ou égal à <strong>0,2 kW/kg</strong> ;</li>
<li>si la moto est bridée, la version d'origine ne doit pas dépasser
<strong>70 kW</strong> (95 ch).</li>
</ul>
<p>Ce troisième point est celui qu'on oublie le plus souvent : toutes les grosses
motos ne sont pas bridables. Vérifiez toujours qu'une <strong>version A2
homologuée existe pour le millésime précis</strong> qui vous intéresse. La
réponse change d'une année à l'autre chez un même constructeur.</p>"""


GUIDES = [

# =====================================================================
{
 "slug": "meilleure-moto-permis-a2",
 "titre": "Meilleure moto permis A2 en 2026 : le guide d'achat",
 "h1": "Quelle moto choisir avec le permis A2 ?",
 "desc": ("Les motos A2 qui valent le coup en 2026 : natives 47 ch ou grosses "
          "cylindrées bridées, prix, coût d'assurance et retours de propriétaires."),
 "chapo": ("Le permis A2 vous limite à 47,5 chevaux pendant deux ans. Cette "
           "contrainte n'interdit ni le plaisir ni le choix, à condition de "
           "comprendre qu'il existe deux stratégies d'achat très différentes, "
           "et que la seconde est celle que choisissent la plupart des motards "
           "français."),
 "sections": [

  {"h2": "Ce que la loi autorise vraiment", "html": REGLE_A2},

  {"h2": "Les deux stratégies, et pourquoi ça change tout",
   "html": """<p>C'est la décision qui structure tout le reste, bien avant le
choix d'un modèle.</p>

<div class="encart"><p class="encart-titre">Stratégie 1. La moto nativement A2</p>
<p>Une machine conçue pour développer 47 ch. Vous l'achetez, vous roulez, rien
à modifier. Moins chère à l'achat comme à l'assurance, plus légère, plus facile.
Le revers : dans deux ans, quand vous passerez en A, vous devrez la revendre
pour monter en gamme.</p></div>

<div class="encart"><p class="encart-titre">Stratégie 2. La grosse cylindrée bridée</p>
<p>Vous achetez une moto plus puissante vendue en version A2 homologuée. Après
deux ans, un professionnel la débride et vous récupérez la puissance intégrale.
Vous achetez une seule fois. Le revers : coût d'achat et d'assurance plus élevés
d'emblée, machine plus lourde à manœuvrer pendant l'apprentissage.</p></div>

<p>En France, la seconde domine largement le marché : la Yamaha MT-07 en version
A2 est la moto la plus vendue de la catégorie depuis des années. Mais elle n'est
pas le bon choix pour tout le monde. Un gabarit léger ou un usage exclusivement
urbain trouvera plus de confort sur une native.</p>"""},

  {"h2": "Les natives A2 : simples et honnêtes", "cartes": [
    {"modele": "honda-500-twins", "nom": "Honda CB500 Hornet",
     "prix": "6 199 €", "puissance": "47 ch", "poids": "190 kg",
     "pour": "Le premier achat sans mauvaise surprise.",
     "forts": ["Bicylindre très souple qui tolère les erreurs d'embrayage",
               "Selle basse et guidon naturel, le poids se fait oublier",
               "Fiabilité Honda et révisions espacées (12 000 km)",
               "Coût des pièces raisonnable"],
     "reserves": ["Le moteur manque de caractère face à une MT-07",
                  "Plusieurs propriétaires disent s'en lasser avant la fin des deux ans"],
     "verdict": ("Le choix rationnel, assumé comme tel. Une machine qui rassure "
                 "plutôt qu'elle n'électrise.")},

    {"modele": "ktm-390-series", "nom": "KTM 390 Duke",
     "prix": "≈ 6 000 €", "puissance": "44 ch", "poids": "≈ 165 kg",
     "pour": "La ville et les petites routes, avec un budget serré.",
     "forts": ["Très légère, donc facile à manœuvrer à l'arrêt",
               "Monocylindre vif, joueuse en usage urbain",
               "Tarif contenu"],
     "reserves": ["Monocylindre vibrant et moins à l'aise sur long trajet",
                  "Position sportive fatigante en duo ou sur autoroute"],
     "verdict": "La plus amusante à petit prix, la moins polyvalente sur route."},

    {"modele": "royal-enfield-interceptor-650", "nom": "Royal Enfield Interceptor 650",
     "prix": "≈ 6 500 €", "puissance": "47 ch", "poids": "≈ 202 kg",
     "pour": "Ceux qui veulent du style sans jouer la performance.",
     "forts": ["Twin 650 nativement A2, couple disponible bas",
               "Look néo-rétro très abouti pour le prix",
               "Selle à 804 mm, position droite et détendue"],
     "reserves": ["Freinage et suspensions en retrait de la concurrence japonaise",
                  "Poids élevé pour la catégorie"],
     "verdict": "Un choix d'esthète, à condition d'accepter des performances modestes."},

    {"modele": "yamaha-yzf-r3", "nom": "Yamaha YZF-R3 / MT-03",
     "prix": "≈ 6 500 €", "puissance": "42 ch", "poids": "≈ 170 kg",
     "pour": "Petits gabarits et amateurs de sportives.",
     "forts": ["Selle à 780 mm, parmi les plus accessibles",
               "Machine légère et maniable",
               "Deux carrosseries : carénée (R3) ou roadster (MT-03)"],
     "reserves": ["321 cm³ seulement : à l'aise en ville, juste sur voie rapide",
                  "Position de conduite engagée sur la R3"],
     "verdict": "Le meilleur compromis quand la hauteur de selle est le critère n°1."},
   ]},

  {"h2": "Les bridables : acheter une fois pour dix ans", "cartes": [
    {"modele": "yamaha-mt-07", "nom": "Yamaha MT-07 (version A2)",
     "prix": "≈ 8 300 €", "puissance": "47 ch bridée, 73 ch libre", "poids": "184 kg",
     "pour": "Le choix par défaut du marché français, et ce n'est pas un hasard.",
     "forts": ["Le twin CP2 conserve son couple et son caractère même bridé",
               "Les propriétaires rapportent qu'on ne s'y ennuie pas, sauf à haute vitesse",
               "Moins de 5 L/100 km, y compris en conduite dynamique",
               "Entretien peu coûteux, vidanges accessibles, réputation de fiabilité",
               "Énorme offre en occasion"],
     "reserves": ["Suspensions d'origine jugées trop souples par beaucoup",
                  "Échappement d'origine sans caractère sonore",
                  "Bridée, elle plafonne autour de 170 km/h compteur"],
     "verdict": ("Si vous n'avez ni contrainte de gabarit ni budget très serré, "
                 "c'est le choix le plus difficile à prendre en défaut.")},

    {"modele": "kawasaki-z650-2017", "nom": "Kawasaki Z650 (version A2)",
     "prix": "≈ 7 700 €", "puissance": "47 ch bridée, 68 ch libre", "poids": "188 kg",
     "pour": "La rivale directe de la MT-07, pour les jambes plus courtes.",
     "forts": ["Selle à 790 mm, l'une des plus basses de la catégorie",
               "Twin agréable et bien fini",
               "Tarif un peu inférieur à la MT-07"],
     "reserves": ["Pas d'antipatinage : prudence sur chaussée mouillée",
                  "Électronique plus pauvre que la concurrence récente"],
     "verdict": "Le même programme que la MT-07, en plus accessible physiquement."},

    {"modele": "triumph-trident-660", "nom": "Triumph Trident 660 (version A2)",
     "prix": "≈ 8 700 €", "puissance": "47 ch bridée, 81 ch libre", "poids": "189 kg",
     "pour": "Ceux qui veulent sortir du duel japonais.",
     "forts": ["Trois cylindres : une sonorité et une allonge que les twins n'ont pas",
               "Finition et présentation nettement au-dessus du segment",
               "Se débride vers 81 ch, de quoi tenir longtemps"],
     "reserves": ["Assurance sensiblement plus chère pour un jeune permis : "
                  "les assureurs tiennent compte du positionnement premium "
                  "et du coût des pièces",
                  "Réseau moins dense que Honda ou Yamaha"],
     "verdict": ("Le plus de caractère du lot, à condition d'avoir intégré "
                 "le surcoût d'assurance dans le budget.")},

    {"modele": "honda-cb650r", "nom": "Honda CB650R (version A2)",
     "prix": "≈ 9 000 €", "puissance": "47 ch bridée, 95 ch libre", "poids": "202 kg",
     "pour": "Ceux qui veulent un quatre-cylindres.",
     "forts": ["Quatre cylindres : montée en régime et sonorité spécifiques",
               "Qualité de fabrication et finition soignées",
               "Gros potentiel une fois débridée"],
     "reserves": ["Plus lourde et plus chère que les twins",
                  "Bridée, le quatre-cylindres perd une partie de son intérêt : "
                  "son agrément se situe dans les hauts régimes"],
     "verdict": "Excellente après débridage, un peu frustrante pendant deux ans."},
   ]},

  {"h2": "Le budget que personne ne calcule",
   "html": """<p>Le prix de la moto n'est qu'une partie de la dépense. Pour un
jeune permis A2, l'assurance pèse lourd et surprend souvent.</p>

<div class="tableau-large"><table class="specs">
<caption>Assurance moto, jeune conducteur A2, ordres de grandeur 2026</caption>
<tbody>
<tr><th scope="row">Au tiers (minimum légal)</th><td>≈ 455 €/an</td></tr>
<tr><th scope="row">Intermédiaire (vol et incendie)</th><td>≈ 648 €/an</td></tr>
<tr><th scope="row">Tous risques</th><td>≈ 907 €/an</td></tr>
<tr><th scope="row">Moyenne constatée, tous contrats</th><td>≈ 1 000 €/an</td></tr>
<tr><th scope="row">Motard expérimenté, à titre de comparaison</th><td>≈ 540 €/an</td></tr>
</tbody></table></div>

<p>À cela s'ajoute la <strong>surprime jeune conducteur</strong> : 100 % la
première année, 50 % la deuxième, 25 % la troisième. Autrement dit, votre
première année d'assurance coûte le double du tarif de référence.</p>

<p>Conséquence concrète sur le choix du modèle : une moto premium ou puissante
peut vous coûter plusieurs centaines d'euros de plus par an que sa rivale
japonaise, à usage identique. <strong>Demandez trois devis avant de signer le
bon de commande</strong>, pas après.</p>""" + bloc_achat(
       ["assurance"], "Demander vos devis")},

  {"h2": "Notre lecture",
   "html": """<p>Il n'y a pas de meilleure moto A2 dans l'absolu, mais il y a
des réponses nettes selon le profil :</p>
<ul class="tick">
<li><strong>Vous voulez garder la moto après le passage en A</strong> : MT-07 en
version bridée. C'est le choix le plus défendable du marché.</li>
<li><strong>Vous mesurez moins d'1 m 70</strong> : Z650 (790 mm) ou MT-03 /
YZF-R3 (780 mm).</li>
<li><strong>Vous voulez dépenser le moins possible</strong> : CB500 Hornet neuve
à 6 199 €, ou une MT-07 d'occasion de trois ans.</li>
<li><strong>Vous roulez surtout en ville</strong> : 390 Duke, légère et vive.</li>
<li><strong>Le style prime</strong> : Interceptor 650, en acceptant ses limites
de freinage.</li>
</ul>
<p>Et un conseil qui revient chez tous les formateurs : le modèle compte moins
que le fait de pouvoir poser les pieds au sol avec confiance. Une moto qui vous
intimide à l'arrêt est une moto que vous sortirez moins.</p>"""},
 ],

 "faq": [
  ("Peut-on débrider une moto A2 avant deux ans ?",
   "Non. Le bridage doit être maintenu pendant toute la durée du permis A2, "
   "soit deux ans. Rouler débridé avant l'échéance vous expose à une absence "
   "de couverture d'assurance en cas d'accident, en plus des sanctions."),
  ("Toutes les grosses motos peuvent-elles être bridées en A2 ?",
   "Non. La version d'origine ne doit pas dépasser 70 kW (95 ch), et le "
   "constructeur doit proposer une homologation A2 pour le millésime concerné. "
   "Vérifiez modèle par modèle et année par année auprès du concessionnaire."),
  ("Combien coûte le débridage après deux ans ?",
   "Le passage en pleine puissance se fait chez un professionnel et suppose une "
   "mise à jour de la carte grise. Les tarifs varient selon le modèle et le "
   "réseau : demandez un devis à votre concessionnaire, nous ne disposons pas "
   "de chiffre fiable à l'échelle du marché."),
  ("Neuve ou d'occasion pour une première moto A2 ?",
   "L'occasion est le choix rationnel : une moto neuve perd 20 à 30 % de sa "
   "valeur la première année, et les petites chutes des premiers mois sont "
   "fréquentes. Voir notre guide dédié à la première moto."),
 ],

 "sources": [
  ("Le Repaire des Motards, essai comparatif Honda CB500 Hornet",
   "https://www.lerepairedesmotards.com/essais/comparo/honda-cb500-hornet-cfmoto-450nk.php"),
  ("Jeune Motard, test Yamaha MT-07 A2 : prix, bridage, carte grise",
   "https://jeunemotard.fr/choisir-sa-moto-articles/test-yamaha-mt-07/"),
  ("Jeune Motard, test Kawasaki Z650 A2",
   "https://jeunemotard.fr/test-kawasaki-z650-a2"),
  ("Jeune Motard, test Triumph Trident 660 A2",
   "https://jeunemotard.fr/choisir-sa-moto-articles/test-triumph-trident-660/"),
  ("Jeune Motard, prix de l'assurance moto A2 en 2026",
   "https://jeunemotard.fr/assurance-articles/prix-assurance-moto-a2/"),
  ("Forum Le Repaire des Motards, retours de propriétaires MT-07 en A2",
   "https://www.lerepairedesmotards.com/forum/read.php?3,3100328"),
  ("Le Repaire des Motards, Honda baisse les prix de la gamme 500",
   "https://www.lerepairedesmotards.com/actualites/2026/promos-baisses-prix-honda-forza-500-hornet-nx-cbr.php"),
 ],
},

# =====================================================================
{
 "slug": "choisir-sa-premiere-moto",
 "titre": "Première moto : le guide pour ne pas se tromper",
 "h1": "Choisir sa première moto",
 "desc": ("Budget réel, poids, hauteur de selle, neuve ou occasion : ce qu'il "
          "faut savoir avant d'acheter sa première moto, sans les clichés."),
 "chapo": ("La question n'est pas « quelle est la meilleure moto pour débuter » "
           "mais « quelle moto vais-je réellement oser sortir du garage ». "
           "Trois critères comptent avant la marque et le style : le poids, la "
           "hauteur de selle, et le budget total, celui qui inclut ce que "
           "personne ne compte."),
 "sections": [

  {"h2": "Le budget réel d'une première année",
   "html": """<p>C'est le poste le plus sous-estimé. Le prix affiché de la moto
représente rarement plus des deux tiers de la dépense réelle.</p>

<div class="tableau-large"><table class="specs">
<caption>Trois scénarios de première année, ordres de grandeur constatés</caption>
<tbody>
<tr><th scope="row">Budget serré (occasion âgée, équipement minimum)</th><td>≈ 6 500 €</td></tr>
<tr><th scope="row">Confort (occasion récente, équipement complet)</th><td>≈ 10 100 €</td></tr>
<tr><th scope="row">Premium (moto neuve, équipement haut de gamme)</th><td>13 600 € et plus</td></tr>
</tbody></table></div>

<p>Ces montants incluent le permis, la moto, l'équipement, l'assurance de
première année et l'entretien. Retenez surtout un ratio qui revient dans tous
les retours : <strong>un motard dépense en moyenne 30 % du prix de sa moto en
équipement la première année</strong>.</p>"""},

  {"h2": "L'équipement passe avant la moto",
   "html": """<p>C'est le conseil le plus unanime, et le plus souvent ignoré.
Une formule résume bien l'arbitrage : mieux vaut une moto à 3 000 € avec
1 500 € d'équipement que l'inverse.</p>
<ul class="tick">
<li><strong>Minimum fonctionnel et homologué</strong> : environ 500 €.</li>
<li><strong>Ensemble crédible neuf</strong>, casque certifié, blouson CE avec
dorsale, gants CE, bottes, pantalon renforcé : 800 à 1 500 €.</li>
</ul>
<p>La tentation de rouler « juste pour cinq minutes » en jean et baskets est le
piège classique des premiers mois. À basse vitesse comme à haute, l'équipement
est la seule barrière entre vous et le bitume.</p>""" + bloc_achat(
       ["casque", "casque-amazon", "blouson", "blouson-amazon", "gants",
        "gants-amazon", "bottes", "bottes-amazon"])},

  {"h2": "Neuve ou d'occasion : la réponse est assez nette",
   "html": """<p>Pour une première moto, l'occasion s'impose pour deux raisons
concrètes.</p>
<p>D'abord la décote : une moto neuve perd <strong>20 à 30 % de sa valeur la
première année</strong>. Ensuite les chutes. Elles sont fréquentes les premiers
mois, un pied qui glisse à l'arrêt, une manœuvre ratée dans un parking, une
béquille mal posée. Sur une machine d'occasion, une rayure se digère. Sur une
moto sortie de concession trois semaines plus tôt, beaucoup moins.</p>
<p>Un budget d'environ 1 500 € permet déjà de trouver une machine en état
correct ; à partir de 3 500 à 4 500 €, l'offre en occasion récente devient
confortable.</p>
<div class="encart"><p class="encart-titre">Le contre-argument honnête</p>
<p>La moto neuve apporte la garantie constructeur et l'absence d'historique
douteux. Si vous n'avez aucun moyen de faire évaluer une occasion par quelqu'un
de compétent, le neuf achète de la tranquillité. C'est un arbitrage
défendable.</p></div>"""},

  {"h2": "Les trois critères qui comptent vraiment",
   "html": """<h3>1. La hauteur de selle</h3>
<p>C'est le critère le plus déterminant et le plus négligé. La règle communément
admise : vous devez pouvoir poser <strong>au moins la pointe des deux pieds au
sol</strong>, et idéalement un pied à plat. En dessous, chaque arrêt devient un
calcul, et vous sortirez la moto moins souvent.</p>
<p>Essayez toujours à l'arrêt, en tenue, avant d'acheter. Une selle annoncée à
800 mm sur le papier peut se ressentir très différemment selon la largeur de la
machine à hauteur de cuisses.</p>

<h3>2. Le poids</h3>
<p>Sous-estimer le poids est l'erreur la plus fréquente des débutants. Ce n'est
pas un problème en roulant. C'est un problème à l'arrêt, en marche arrière,
dans un parking en pente, ou pour relever la machine après une chute. Une moto
de 180 kg pardonne beaucoup plus qu'une de 230 kg.</p>

<h3>3. La souplesse du moteur</h3>
<p>Un moteur qui reprend proprement à bas régime et ne cale pas au moindre
relâchement d'embrayage vous fera progresser plus vite qu'un moteur pointu.
C'est précisément ce que les propriétaires apprécient sur les bicylindres de
moyenne cylindrée : ils tolèrent les manipulations brusques des premiers mois.</p>"""},

  {"h2": "Quelle cylindrée pour débuter ?",
   "html": """<p>Les formateurs convergent : entre <strong>125 et 500 cm³</strong>
pour un premier apprentissage serein. Au-delà, la moto reste maîtrisable mais
demande plus d'attention pendant que vous construisez vos automatismes.</p>
<p>Cela dit, le marché français réel s'écarte de cette recommandation : la
majorité des jeunes permis A2 achètent des motos de 650 à 700 cm³ en version
bridée. Ce n'est pas absurde. Bridées, elles délivrent la même puissance qu'une
native, mais elles sont plus lourdes, et c'est le poids qui pose problème au
début, pas la puissance.</p>"""},

  {"h2": "Quelques modèles régulièrement conseillés", "cartes": [
    {"modele": "honda-500-twins", "nom": "Honda CB500 Hornet",
     "prix": "6 199 €", "puissance": "47 ch", "poids": "190 kg",
     "pour": "Le débutant qui veut zéro mauvaise surprise.",
     "forts": ["Moteur souple qui tolère les erreurs d'embrayage",
               "Selle basse, poids contenu, prise en main immédiate",
               "Entretien espacé et peu coûteux"],
     "reserves": ["Peu de caractère : certains s'en lassent avant deux ans"],
     "verdict": "La référence du premier achat rationnel."},

    {"modele": "yamaha-mt-03", "nom": "Yamaha MT-03",
     "prix": "≈ 6 500 €", "puissance": "42 ch", "poids": "≈ 170 kg",
     "pour": "Petits gabarits, usage urbain et périurbain.",
     "forts": ["Selle à 780 mm et faible poids : très rassurante à l'arrêt",
               "Maniable en ville"],
     "reserves": ["321 cm³ : un peu juste sur voie rapide et en duo"],
     "verdict": "Le meilleur choix quand poser les pieds est votre inquiétude n°1."},

    {"modele": "honda-cmx500-rebel", "nom": "Honda CMX500 Rebel",
     "prix": "≈ 6 800 €", "puissance": "46 ch", "poids": "≈ 191 kg",
     "pour": "Ceux que la hauteur de selle inquiète le plus.",
     "forts": ["Selle très basse, parmi les plus accessibles du marché",
               "Position détendue, centre de gravité bas",
               "Même moteur 500 que la CB500, réputé fiable"],
     "reserves": ["Style custom qui ne conviendra pas à tout le monde",
                  "Suspension arrière au débattement limité sur mauvais revêtement"],
     "verdict": "La solution quand tous les roadsters semblent trop hauts."},
   ]},

  {"h2": "Les erreurs qui reviennent le plus",
   "html": """<ul class="tick">
<li><strong>Économiser sur l'équipement</strong> pour s'offrir une plus belle
moto. C'est l'arbitrage inverse de celui qu'il faut faire.</li>
<li><strong>Choisir sur le style sans essayer à l'arrêt.</strong> Une moto trop
haute ou trop lourde finit au garage.</li>
<li><strong>Freiner brutalement de l'avant</strong> ou oublier le frein arrière.
Cela s'entraîne, idéalement sur un parking vide avant la première sortie.</li>
<li><strong>Oublier l'assurance dans le budget.</strong> Un jeune permis A2 paie
en moyenne près de 1 000 € par an, avec une surprime de 100 % la première
année.</li>
<li><strong>Acheter trop gros « pour ne pas racheter dans deux ans ».</strong>
Le raisonnement se défend, mais pas au prix d'une machine que vous n'osez pas
manœuvrer.</li>
</ul>"""},
 ],

 "faq": [
  ("Quel budget minimum pour commencer la moto ?",
   "En comptant une occasion abordable, un équipement homologué d'entrée de "
   "gamme et l'assurance de première année, il faut prévoir environ 6 500 € "
   "tout compris, permis inclus. L'équipement seul représente 500 € au minimum "
   "absolu, 800 à 1 500 € pour un ensemble complet et crédible."),
  ("Faut-il pouvoir poser les deux pieds à plat au sol ?",
   "Non, ce n'est pas indispensable. La règle communément admise est de pouvoir "
   "poser au moins la pointe des deux pieds, et idéalement un pied à plat. En "
   "dessous, les manœuvres à l'arrêt deviennent stressantes."),
  ("Vaut-il mieux une 125 ou directement une A2 ?",
   "Si vous avez le permis A2, la question du 125 ne se pose que pour le budget "
   "ou un usage strictement urbain. Une A2 de 400 à 500 cm³ est plus polyvalente "
   "et se revend mieux."),
  ("Combien de temps garde-t-on sa première moto ?",
   "Beaucoup de motards changent à la fin des deux ans de permis A2. C'est "
   "précisément l'argument des grosses cylindrées bridées : on achète une fois "
   "et on débride ensuite."),
 ],

 "sources": [
  ("3AS Racing, budget moto débutant 2026, le vrai coût tout compris",
   "https://blog.3as-racing.com/budget-moto-debutant-vrai-cout-tout-compris-2026/"),
  ("Passion Moto Sécurité, quelle moto pour débuter",
   "https://moto-securite.fr/moto-debuter/"),
  ("Liberty Rider, les erreurs des débutants à moto",
   "https://liberty-rider.com/blog/mood-motard/debutants/top-8-des-erreurs-commises-par-les-debutants-a-moto"),
  ("Honda Moto France, erreurs courantes des motards débutants",
   "https://honda-moto.fr/erreurs-courantes-motards-debutants-comment-eviter/"),
  ("Caradisiac, acheter votre première moto, le guide d'achat",
   "https://www.caradisiac.com/acheter-votre-premiere-moto-le-guide-d-achat-215596.htm"),
  ("Jeune Motard, prix de l'assurance moto A2 en 2026",
   "https://jeunemotard.fr/assurance-articles/prix-assurance-moto-a2/"),
 ],
},

# =====================================================================
{
 "slug": "meilleure-moto-routiere-voyage",
 "titre": "Meilleure moto routière pour voyager en 2026",
 "h1": "Quelle moto routière pour partir loin ?",
 "desc": ("Confort, protection au vent, capacité en duo et autonomie : les "
          "routières qui tiennent la distance, avec les retours de propriétaires."),
 "chapo": ("Une routière se juge sur quatre points, et aucun n'est la puissance : "
           "la protection au vent, le confort de selle après trois heures, la "
           "capacité à emmener un passager chargé, et l'autonomie. Les retours "
           "de propriétaires sont ici bien plus utiles que les fiches techniques."),
 "sections": [

  {"h2": "Ce qui fait vraiment une bonne moto de voyage",
   "html": """<ul class="tick">
<li><strong>La protection au vent.</strong> C'est ce qui fait la différence
entre trois heures d'autoroute reposantes et trois heures d'épuisement. Une
bulle réglable en hauteur change tout.</li>
<li><strong>La selle.</strong> Le point le plus critiqué sur presque tous les
modèles, y compris haut de gamme. Prévoyez que vous devrez peut-être la
remplacer, c'est fréquent, et c'est un budget.</li>
<li><strong>Le débattement de suspension.</strong> Un critère peu regardé mais
déterminant sur les routes dégradées : 150 mm apporte un confort nettement
supérieur à 130 mm, surtout chargé.</li>
<li><strong>L'autonomie.</strong> En dessous de 300 km réels, le voyage devient
une succession d'arrêts subis.</li>
<li><strong>Le duo.</strong> Si le passager est assis nettement plus haut, la
moto devient instable au freinage. Regardez la géométrie de la selle passager
autant que son rembourrage.</li>
</ul>"""},

  {"h2": "La sélection", "cartes": [
    {"modele": "honda-nt1100", "nom": "Honda NT1100",
     "prix": "≈ 13 500 €", "puissance": "102 ch", "poids": "≈ 238 kg",
     "pour": "Rouler loin, souvent, et chargé.",
     "forts": ["Souvent citée comme le meilleur rapport qualité/prix du segment",
               "Bicylindre parallèle calé à 270° : du caractère malgré la vocation GT",
               "Ergonomie soignée et confort en duo",
               "Débattement de suspension de 150 mm, sensiblement supérieur "
               "à celui de plusieurs rivales"],
     "reserves": ["Machine lourde, à considérer si vous manœuvrez souvent à l'arrêt",
                  "Look consensuel, peu de personnalité visuelle"],
     "verdict": ("La routière rationnelle par excellence. Peu de compromis "
                 "réels pour l'usage auquel elle est destinée.")},

    {"modele": None, "nom": "Yamaha Tracer 9 GT",
     "prix": "15 799 €", "puissance": "119 ch", "poids": "≈ 220 kg",
     "pour": "Garder une moto vive au quotidien et partir loin de temps en temps.",
     "forts": ["Le trois-cylindres est unanimement salué : disponible partout",
               "Excellente sur route sinueuse, « du bonheur » en montagne "
               "selon les propriétaires",
               "Équipement complet en finition GT"],
     "reserves": ["La selle est le reproche principal : plusieurs propriétaires "
                  "signalent que même la selle confort en option reste "
                  "inconfortable sur longue distance",
                  "Protection au vent jugée insuffisante sur autoroute, "
                  "bulle d'origine trop basse",
                  "Débattement de suspension de 130/131 mm seulement, court "
                  "sur petites routes dégradées",
                  "Centre de gravité haut, signalé par des pilotes d'1 m 77"],
     "verdict": ("Le meilleur moteur du comparatif, mais la moins aboutie sur "
                 "les critères propres au voyage. Prévoyez le budget selle et "
                 "bulle.")},

    {"modele": "kawasaki-versys-650", "nom": "Kawasaki Versys 650",
     "prix": "8 449 €", "puissance": "68 ch", "poids": "≈ 218 kg",
     "pour": "Voyager sans y mettre le prix d'une grosse GT.",
     "forts": ["Confort de voyage et protection au vent souvent salués",
               "Position droite et détendue",
               "Le duo est un vrai point fort : passager assis quasiment à la "
               "même hauteur, sans instabilité notable",
               "Environ 5 L/100 km à 130 km/h, soit près de 320 km d'autonomie",
               "Existe en version A2"],
     "reserves": ["68 ch seulement : à l'aise partout, jamais démonstrative",
                  "Finition en retrait des modèles premium",
                  "Machine encombrante malgré sa cylindrée modeste"],
     "verdict": ("Le choix rationnel et le meilleur rapport prestations/prix "
                 "pour qui voyage souvent en duo.")},

    {"modele": "triumph-tiger-sport-660", "nom": "Triumph Tiger Sport 660",
     "prix": "9 995 €", "puissance": "81 ch", "poids": "≈ 206 kg",
     "pour": "Un compromis route-sport avec du caractère moteur.",
     "forts": ["Trois cylindres de 660 cm³ : plus de caractère que les twins rivaux",
               "Jantes de 17 pouces et suspensions calibrées pour la route",
               "Plus légère que la plupart des routières"],
     "reserves": ["Capacité de charge et protection en retrait des vraies GT",
                  "Réseau moins dense que les japonaises"],
     "verdict": "La plus agréable à conduire au quotidien du lot, un cran en dessous pour le grand voyage."},
   ]},

  {"h2": "Tableau de synthèse",
   "html": """<div class="tableau-large"><table class="tab-duel">
<thead><tr><th>Critère</th><th>NT1100</th><th>Tracer 9 GT</th>
<th>Versys 650</th><th>Tiger Sport 660</th></tr></thead>
<tbody>
<tr><th scope="row">Prix indicatif</th><td>≈ 13 500 €</td><td>15 799 €</td>
<td class="gagne">8 449 €</td><td>9 995 €</td></tr>
<tr><th scope="row">Puissance</th><td>102 ch</td><td class="gagne">119 ch</td>
<td>68 ch</td><td>81 ch</td></tr>
<tr><th scope="row">Débattement susp.</th><td class="gagne">150 mm</td><td>130 mm</td>
<td>150 mm</td><td>150 mm</td></tr>
<tr><th scope="row">Confort selle</th><td>Bon</td><td>Critiqué</td>
<td>Bon</td><td>Correct</td></tr>
<tr><th scope="row">Protection vent</th><td class="gagne">Très bonne</td><td>Insuffisante d'origine</td>
<td>Bonne</td><td>Correcte</td></tr>
<tr><th scope="row">Aptitude duo</th><td class="gagne">Très bonne</td><td>Bonne</td>
<td class="gagne">Très bonne</td><td>Correcte</td></tr>
<tr><th scope="row">Accessible en A2</th><td>Non</td><td>Non</td>
<td class="gagne">Oui</td><td>Oui (bridée)</td></tr>
</tbody></table></div>
<p class="mention">Les appréciations qualitatives résument les retours de
propriétaires et d'essais publiés, référencés en bas de page. Elles ne
résultent pas d'un essai que nous aurions conduit.</p>"""},

  {"h2": "Notre lecture",
   "html": """<ul class="tick">
<li><strong>Vous partez souvent et chargé, en duo</strong> : NT1100. C'est la
plus complète sur les critères qui comptent en voyage.</li>
<li><strong>Budget contenu, usage voyage régulier</strong> : Versys 650. À
8 449 €, elle offre l'essentiel de ce qu'apportent des machines à 15 000 €.</li>
<li><strong>Vous voulez une moto vive au quotidien qui sait voyager</strong> :
Tracer 9 GT, en intégrant le budget d'une selle et d'une bulle plus hautes.</li>
<li><strong>Vous roulez surtout seul, sur petites routes</strong> : Tiger
Sport 660.</li>
</ul>
<p>Une remarque qui vaut pour toutes : la selle d'origine est le compromis le
plus systématiquement critiqué du segment, y compris sur des machines à plus de
15 000 €. Si vous prévoyez des étapes de plus de 400 km, considérez d'emblée une
selle confort d'un spécialiste comme faisant partie du prix d'achat.</p>"""},
 ],

 "faq": [
  ("Faut-il un gros moteur pour voyager à moto ?",
   "Non. Une Versys 650 de 68 ch avale les kilomètres aussi bien qu'une machine "
   "de 120 ch. Ce qui fatigue sur long trajet, c'est le vent, la selle et les "
   "vibrations, pas le manque de puissance."),
  ("Peut-on voyager avec une moto accessible en A2 ?",
   "Oui. La Kawasaki Versys 650 existe en version A2, et la Triumph Tiger "
   "Sport 660 se bride également. Ce sont les deux entrées les plus crédibles "
   "dans le voyage à moto avec un permis A2."),
  ("Quelle autonomie viser pour voyager sereinement ?",
   "Environ 300 km réels entre deux pleins. En dessous, les arrêts dictent "
   "l'itinéraire. La Versys 650 tourne autour de 320 km à allure d'autoroute."),
  ("La selle d'origine suffit-elle pour les longues étapes ?",
   "Rarement au-delà de 300 à 400 km. C'est le reproche le plus fréquent du "
   "segment, y compris sur les modèles haut de gamme et sur les selles confort "
   "proposées en option par les constructeurs."),
 ],

 "sources": [
  ("Le Repaire des Motards, routière Honda NT1100 2026",
   "https://www.lerepairedesmotards.com/actualites/2025/routiere-honda-nt1100-2026.php"),
  ("Forum MT09.net, 30 000 km en 9 mois sur Tracer 9 GT, avis propriétaire",
   "https://www.mt09.net/t15142-apres-30000km-en-9-mois-mon-avis-sur-la-tracer-9-gt"),
  ("Caradisiac, avis de propriétaires sur la gamme Yamaha Tracer",
   "https://www.caradisiac.com/gamme-moto--yamaha-tracer/avis/"),
  ("Le Repaire des Motards, essai Kawasaki Versys 650",
   "https://www.lerepairedesmotards.com/essais/motos/kawasaki-versys-650-abs.php"),
  ("A2 Riders, test Versys 650, le trail pour voyager en A2",
   "https://a2riders.com/essais/test-kawasaki-versys-650-2022-trail-routier-gt-voyage-duo-a2/"),
  ("Emoto, comparatif Tracer 9 GT, Tiger Sport 800, F900XR, V100",
   "https://www.emoto.com/comparatifs/tracer-9-gt-tiger-sport-800-f900xr-v100-et-turismo-veloce-10537.php"),
  ("Moto-Net, fiche technique Triumph Tiger Sport 660 2026",
   "https://www.moto-net.com/article/fiche-technique-moto-triumph-tiger-sport-660-2026.html"),
 ],
},

# =====================================================================
{
 "slug": "cylindree-couple-puissance",
 "titre": "Cylindrée, couple et puissance : comprendre les chiffres d'une fiche moto",
 "h1": "Cylindrée, couple et puissance : ce que disent vraiment les chiffres",
 "desc": ("Cylindrée, chevaux, Newton-mètres : à quoi correspond chaque chiffre "
          "d'une fiche technique moto, et pourquoi ils ne mesurent pas la même chose."),
 "chapo": ("Trois chiffres reviennent sur toutes les fiches techniques : la "
           "cylindrée, la puissance et le couple. Ce ne sont pas trois façons de "
           "dire la même chose. Une fois qu'on sait ce que chacun mesure, une "
           "fiche technique devient beaucoup plus lisible."),
 "sections": [

  {"h2": "La cylindrée : un volume, pas une performance",
   "html": """<p>La cylindrée est le volume total balayé par les pistons à
l'intérieur des cylindres, mesuré en centimètres cubes (cm³). Un bicylindre de
649 cm³ correspond, grosso modo, à deux cylindres d'environ 325 cm³ chacun.</p>
<p>C'est une mesure de <strong>volume</strong>, pas de puissance : elle donne une
idée du potentiel du moteur, mais deux motos de même cylindrée peuvent avoir des
puissances très différentes selon l'architecture, le taux de compression ou la
gestion électronique. À l'inverse, un petit moteur très poussé peut dépasser un
plus gros moteur réglé pour la souplesse.</p>"""},

  {"h2": "La puissance : la vitesse à laquelle le travail est fait",
   "html": """<p>La puissance, exprimée en chevaux (ch) ou en kilowatts (kW),
mesure la quantité de travail que le moteur peut fournir par unité de temps.
C'est elle qui conditionne surtout la <strong>vitesse de pointe</strong> et les
relances à haut régime.</p>
<p>Sur une fiche technique, la puissance est presque toujours donnée avec le
régime auquel elle est atteinte (par exemple « 74 ch à 8&nbsp;500 tr/min ») : au
régime maximal du moteur, pas à n'importe quel moment. En dessous de ce régime,
la moto ne délivre pas ce chiffre.</p>"""},

  {"h2": "Le couple : la force qui fait la reprise",
   "html": """<p>Le couple, exprimé en Newton-mètres (Nm), mesure la force de
rotation disponible sur le vilebrequin. C'est lui qui donne la sensation de
« pousser dans le dos » à l'accélération, et qui permet de reprendre sans
rétrograder.</p>
<p>Contrairement à la puissance, le couple maximal est en général atteint à un
régime <strong>bas ou moyen</strong>. Une moto au couple généreux dès les bas
régimes se conduit sans avoir besoin de faire hurler le moteur ; c'est souvent
le cas des gros roadsters et des trails routiers.</p>"""},

  {"h2": "Comment les deux se rejoignent : la courbe moteur",
   "html": """<p>Couple et puissance ne sont pas deux mesures indépendantes : la
puissance se déduit du couple et du régime moteur, selon une relation directe.
Convertie en kilowatts et en Newton-mètres, cette relation a une conséquence
visuelle très pratique : <strong>quand les deux courbes sont tracées sur le
même graphique, avec les mêmes graduations, elles se croisent toujours au même
régime : 9&nbsp;550 tr/min</strong>, quel que soit le moteur.</p>

<figure class="schema-fig">
<svg viewBox="0 0 640 380" role="img" aria-labelledby="titre-schema-cp desc-schema-cp" xmlns="http://www.w3.org/2000/svg">
  <title id="titre-schema-cp">Courbes schématiques de couple et de puissance en fonction du régime moteur</title>
  <desc id="desc-schema-cp">Le couple culmine vers 6 000 tr/min puis redescend. La puissance monte progressivement, dépasse le couple après leur croisement à 9 550 tr/min, puis plafonne avant de retomber en fin de plage.</desc>

  <line x1="60" y1="320" x2="600" y2="320" stroke="var(--trait-fort)" stroke-width="1.5"/>
  <line x1="60" y1="40" x2="60" y2="320" stroke="var(--trait-fort)" stroke-width="1.5"/>

  <g stroke="var(--trait)" stroke-width="1">
    <line x1="150" y1="40" x2="150" y2="320"/>
    <line x1="240" y1="40" x2="240" y2="320"/>
    <line x1="330" y1="40" x2="330" y2="320"/>
    <line x1="420" y1="40" x2="420" y2="320"/>
    <line x1="510" y1="40" x2="510" y2="320"/>
  </g>

  <g fill="var(--doux)" font-size="12" text-anchor="middle" font-family="inherit">
    <text x="60" y="338">0</text>
    <text x="150" y="338">2 000</text>
    <text x="240" y="338">4 000</text>
    <text x="330" y="338">6 000</text>
    <text x="420" y="338">8 000</text>
    <text x="510" y="338">10 000</text>
    <text x="600" y="338">12 000</text>
    <text x="330" y="362" font-size="12.5">Régime moteur (tr/min)</text>
  </g>

  <polyline points="60,301.8 105,232.5 150,175.8 195,131.7 240,100.2 285,81.3 330,75 375,81.3 420,100.2 465,131.7 489.75,154.38 510,175.8 555,232.5 600,301.8"
    fill="none" stroke="var(--accent)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <polyline points="60,320 105,310.8 150,289.8 195,260.85 240,227.95 285,195.05 330,166.07 375,145.03 420,135.9 465,142.55 489.75,154.38 510,169.01 555,219.2 600,297.14"
    fill="none" stroke="var(--petrole)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>

  <line x1="489.75" y1="154.38" x2="489.75" y2="320" stroke="var(--doux)" stroke-width="1" stroke-dasharray="4 4"/>
  <circle cx="489.75" cy="154.38" r="5" fill="var(--texte)"/>
  <text x="489.75" y="130" text-anchor="middle" font-size="12.5" fill="var(--texte)" font-weight="600">9 550 tr/min</text>

  <g font-size="13" font-weight="600">
    <line x1="330" y1="55" x2="352" y2="55" stroke="var(--accent)" stroke-width="3"/>
    <text x="358" y="59" fill="var(--texte)">Couple (Nm)</text>
    <line x1="330" y1="75" x2="352" y2="75" stroke="var(--petrole)" stroke-width="3"/>
    <text x="358" y="79" fill="var(--texte)">Puissance (kW)</text>
  </g>
</svg>
<figcaption>Schéma illustratif (pas une courbe réelle d'un modèle précis) :
avant 9&nbsp;550 tr/min le couple est au-dessus de la puissance sur ce graphique,
après il repasse en dessous. C'est une propriété mathématique de la conversion
Nm/kW, valable pour n'importe quel moteur.</figcaption>
</figure>

<p class="mention">Sur une fiche technique en chevaux plutôt qu'en kilowatts, le
croisement ne tombe plus pile sur un chiffre rond (le ch et le kW n'ont pas la
même valeur), mais le principe reste identique : le couple domine en dessous
d'un certain régime, la puissance au-dessus.</p>"""},

  {"h2": "Ce que ça change pour choisir sa moto",
   "html": """<ul class="tick">
<li><strong>Beaucoup de couple bas et médian</strong> : moto agréable en usage
courant, qui reprend sans avoir besoin de rétrograder ni de monter dans les
tours. Typique des roadsters et trails routiers de moyenne cylindrée.</li>
<li><strong>Pic de puissance à haut régime</strong> : moto qui demande de « faire
tourner » le moteur pour exploiter son potentiel. Gratifiant sur route sportive
ou circuit, moins reposant en usage quotidien ou en ville.</li>
<li><strong>La cylindrée seule ne prédit ni l'un ni l'autre</strong> : elle donne
une idée du potentiel global, mais c'est la courbe couple/puissance, pas le
chiffre de cylindrée, qui dit comment la moto se comporte réellement sur la
route.</li>
</ul>"""},
 ],

 "faq": [
  ("Une grosse cylindrée a-t-elle toujours plus de couple ?",
   "En général oui à architecture égale, mais pas systématiquement : un moteur "
   "de plus petite cylindrée mais bien préparé peut dépasser en couple un plus "
   "gros moteur réglé pour la douceur ou la sobriété."),
  ("Pourquoi le couple et la puissance se croisent-ils à 9 550 tr/min ?",
   "C'est une conséquence directe de la conversion entre Newton-mètres et "
   "kilowatts : la formule qui relie les deux fait apparaître ce nombre comme "
   "point de croisement, quel que soit le moteur, dès lors que le couple est "
   "en Nm et la puissance en kW sur le même graphique."),
  ("Le croisement tombe-t-il aussi à 9 550 tr/min en chevaux (ch) ?",
   "Non. Le ch et le kW n'ont pas la même valeur (1 kW ≈ 1,36 ch), donc le "
   "croisement en Nm/ch se produit à un régime différent. Le principe reste "
   "le même : le couple domine en dessous, la puissance au-dessus."),
  ("Faut-il regarder la puissance max ou le couple max pour choisir une moto ?",
   "Le couple, et surtout le régime auquel il est disponible, renseigne mieux "
   "sur l'agrément au quotidien. La puissance max renseigne surtout sur la "
   "vitesse de pointe et le potentiel à haut régime."),
 ],

 "sources": [
  ("Blog Automobile, puissance et couple : des courbes",
   "https://blogautomobile.fr/puissance-couple-courbes-137910"),
  ("Blog Automobile, puissance et couple, du côté du moteur",
   "https://blogautomobile.fr/puissance-couple-cote-moteur-137052"),
  ("Astuces Pratiques, courbe de couple et de puissance moteur",
   "https://www.astuces-pratiques.fr/auto-moto/courbe-couple-puissance-moteur"),
  ("CBpower, la différence entre couple et puissance",
   "https://www.cbpower.be/blog/difference-entre-couple-et-puissance/"),
 ],
},

]
