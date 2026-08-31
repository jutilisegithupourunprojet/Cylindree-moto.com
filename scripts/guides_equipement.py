# -*- coding: utf-8 -*-
"""
Guides equipement et assurance (10 a 12).

Meme regle de redaction que guides_contenu.py : rien d'invente, tout est
source. On ne recommande aucun produit precis qu'on ne pourrait pas justifier.
"""
from affiliation import bloc_achat

GUIDES_EQUIPEMENT = [

# =====================================================================
{
 "slug": "quel-casque-moto-choisir",
 "titre": "Quel casque moto choisir en 2026 : le guide complet",
 "h1": "Quel casque moto choisir ?",
 "desc": ("Intégral, modulable ou jet, norme ECE 22.06, taille et budget : "
          "tout ce qu'il faut savoir avant d'acheter un casque moto."),
 "chapo": ("Le casque est le seul équipement obligatoire qui protège la partie "
           "du corps qu'on ne peut pas réparer. Bonne nouvelle : les études "
           "indépendantes montrent que payer plus cher n'achète pas forcément "
           "une meilleure protection. Ce qui compte, c'est la taille, le type "
           "et l'homologation."),
 "sections": [

  {"h2": "La règle qui devrait changer votre budget",
   "html": """<div class="encart"><p class="encart-titre">Le prix ne mesure pas la protection</p>
<p>Une étude de l'UFC-Que Choisir portant sur 22 casques a établi que certains
modèles vendus plusieurs centaines d'euros protègent <strong>moins bien</strong>
que des casques nettement moins chers. Plusieurs des mieux notés coûtaient moins
de 200 €.</p></div>

<p>Ce que le prix achète réellement : le confort, la légèreté, l'insonorisation,
la qualité de l'écran, la ventilation, la finition. Ce sont de vrais arguments.
Un casque confortable est un casque que vous portez correctement, mais ce ne
sont pas des arguments de sécurité.</p>

<p>Conséquence pratique : <strong>un budget de 150 à 300 € suffit pour un casque
sûr et bien homologué</strong>. Au-delà, vous achetez du confort. Ce n'est pas
inutile, mais sachez ce que vous payez.</p>"""},

  {"h2": "ECE 22.06 : ce que dit vraiment la réglementation",
   "html": """<p>Depuis le 1er janvier 2024, seuls les casques homologués
<strong>ECE 22.06</strong> peuvent être commercialisés neufs. Cette norme impose
des tests d'absorption des chocs et de résistance à l'impact plus exigeants que
la précédente.</p>

<div class="encart"><p class="encart-titre">Devez-vous remplacer votre casque ?</p>
<p><strong>Non.</strong> Aucun texte n'impose de remplacer un casque ECE 22.05
encore en service. Vous pouvez continuer à l'utiliser à condition qu'il soit en
bon état : pas de fissure, pas de déformation, étiquette de certification
lisible. En revanche, vous ne trouverez plus de 22.05 en magasin.</p></div>

<p>Deux autres règles souvent ignorées :</p>
<ul class="tick">
<li>Le casque doit être <strong>correctement attaché</strong>. Une jugulaire
non bouclée équivaut à l'absence de casque aux yeux de la loi.</li>
<li>Les <strong>gants certifiés CE</strong> sont également obligatoires, pour
le conducteur comme pour le passager, ainsi qu'un gilet de haute visibilité
rangé à bord.</li>
</ul>"""},

  {"h2": "Intégral, modulable ou jet : le vrai arbitrage",
   "html": """<div class="tableau-large"><table class="tab-duel">
<thead><tr><th>Critère</th><th>Intégral</th><th>Modulable</th><th>Jet</th></tr></thead>
<tbody>
<tr><th scope="row">Protection du menton</th><td class="gagne">Complète</td>
<td>Complète mentonnière fermée</td><td>Aucune</td></tr>
<tr><th scope="row">Poids moyen</th><td class="gagne">1 150 à 1 500 g</td>
<td>≈ 1 600 g, jusqu'à 1 800 g</td><td>Le plus léger</td></tr>
<tr><th scope="row">Bruit</th><td class="gagne">Le mieux insonorisé</td>
<td>Jonctions de mentonnière moins étanches</td><td>Très exposé</td></tr>
<tr><th scope="row">Praticité au quotidien</th><td>Moyenne</td>
<td class="gagne">Excellente</td><td class="gagne">Excellente</td></tr>
<tr><th scope="row">Usage conseillé</th><td>Route, autoroute, sportive</td>
<td>Ville, trajets mixtes</td><td>Ville, faible vitesse</td></tr>
</tbody></table></div>

<p>Le modulable a un atout que l'intégral n'a pas : la <strong>double
homologation P/J</strong>, qui l'autorise mentonnière fermée (P) comme relevée
(J). C'est ce qui rend le quotidien plus simple, ouvrir à la station-service,
respirer dans les embouteillages, parler à quelqu'un sans se déséquiper.</p>

<div class="encart"><p class="encart-titre">Le chiffre à connaître sur les modulables</p>
<p>Près de <strong>40 % des accidents graves impliquant un casque modulable</strong>
surviennent avec la mentonnière relevée. La souplesse d'usage se paie si vous
prenez l'habitude de rouler ouvert. Un modulable n'est protecteur que fermé.</p></div>

<p>Sur autoroute, plusieurs motards rapportent que le modulable est plus bruyant
et légèrement moins stable que l'intégral. Si vous faites beaucoup de kilomètres
à vitesse soutenue, l'intégral reste le choix le plus sûr et le plus
reposant.</p>"""},

  {"h2": "Prendre la bonne taille : la seule étape qu'on ne peut pas rater",
   "html": """<p>Un casque trop grand peut se déchausser au moment du choc, ce
qui annule toute protection. C'est le point le plus critique de l'achat, avant
la marque et avant le prix.</p>

<h3>Mesurer son tour de tête</h3>
<p>Avec un mètre de couturière, mesurez la circonférence du crâne
<strong>environ 2,5 cm au-dessus des sourcils</strong>, à l'endroit le plus
large. Reportez cette mesure sur le guide des tailles du fabricant.</p>

<h3>Les trois règles qui suivent</h3>
<ul class="tick">
<li><strong>En cas d'hésitation entre deux tailles, prenez la plus petite.</strong>
Les mousses se tassent et s'adaptent à votre morphologie avec l'usage ; elles ne
se resserrent jamais.</li>
<li><strong>Les tailles ne sont pas transposables d'une marque à l'autre.</strong>
Un M chez un fabricant ne vaut pas un M chez un autre. Consultez systématiquement
le guide du fabricant concerné.</li>
<li><strong>Essayez en magasin, même si vous achetez en ligne ensuite.</strong>
La forme de la calotte varie : certaines marques taillent plutôt rond, d'autres
plutôt ovale. Un casque de bonne taille mais de mauvaise forme reste
inconfortable.</li>
</ul>

<p>Un casque neuf doit être ferme sans créer de point de pression douloureux.
Gardez-le une dizaine de minutes en magasin : les points durs se révèlent
rarement en trente secondes.</p>"""},

  {"h2": "Quel budget prévoir",
   "html": """<div class="tableau-large"><table class="specs">
<caption>Ce que chaque gamme apporte réellement</caption>
<tbody>
<tr><th scope="row">150 à 300 €</th><td>Casques fiables et bien homologués.
Suffisant pour rouler en sécurité. Confort et insonorisation perfectibles.</td></tr>
<tr><th scope="row">300 à 500 €</th><td>Coques multi-composites, écran Pinlock
souvent inclus, meilleure ventilation. Le meilleur compromis pour un usage
quotidien.</td></tr>
<tr><th scope="row">600 à 900 €</th><td>Légèreté, finition et silence. Confort
haut de gamme, pas nécessairement plus de protection.</td></tr>
</tbody></table></div>

<p>Un accessoire mérite d'être budgété d'emblée : l'<strong>écran Pinlock</strong>
anti-buée. Sur beaucoup de casques de gamme intermédiaire il est fourni ; sinon
comptez une trentaine d'euros. En hiver, il fait une différence de sécurité
réelle.</p>""" + bloc_achat(["casque", "casque-amazon"])},

  {"h2": "Quand remplacer son casque",
   "html": """<ul class="tick">
<li><strong>Après tout choc</strong>, même sans dommage visible et même si le
casque est tombé seul du guidon. Les matériaux absorbants travaillent une fois.</li>
<li><strong>Si la coque est fissurée ou déformée</strong>, ou si l'étiquette
d'homologation n'est plus lisible.</li>
<li><strong>Quand les mousses sont tassées</strong> au point que le casque bouge
sur la tête.</li>
</ul>
<p>N'achetez jamais un casque d'occasion : vous ne pouvez pas savoir s'il a
encaissé un choc.</p>"""},
 ],

 "faq": [
  ("Un casque ECE 22.05 est-il encore autorisé en 2026 ?",
   "Oui. Aucun texte n'impose de remplacer un casque ECE 22.05 en bon état. "
   "Seule la vente de casques neufs est limitée à la norme 22.06 depuis le "
   "1er janvier 2024."),
  ("Faut-il mettre plus de 300 € dans un casque ?",
   "Pas pour la sécurité. Une étude de l'UFC-Que Choisir sur 22 casques a montré "
   "que certains modèles à moins de 200 € protègent mieux que des références "
   "vendues plus de 400 €. Au-delà de 300 €, vous achetez du confort, de la "
   "légèreté et du silence."),
  ("Modulable ou intégral pour rouler tous les jours ?",
   "Le modulable est plus pratique en ville et bénéficie de la double "
   "homologation P/J. Mais il est plus lourd, plus bruyant, et près de 40 % des "
   "accidents graves le concernant surviennent mentonnière relevée. Pour "
   "beaucoup d'autoroute, l'intégral reste préférable."),
  ("Quelle taille prendre en cas d'hésitation ?",
   "La plus petite. Les mousses se tassent avec l'usage et ne se resserrent "
   "jamais. Un casque trop grand peut se déchausser lors d'un choc."),
 ],

 "sources": [
  ("UFC-Que Choisir, casques moto et scooter : les plus chers ne sont pas les plus sûrs",
   "https://www.quechoisir.org/actualite-casques-moto-et-scooter-les-plus-chers-ne-sont-pas-les-plus-surs-n65299/"),
  ("Le Repaire des Motards, comment bien choisir son casque moto",
   "https://www.lerepairedesmotards.com/dossiers/casques.php"),
  ("Motoblouz, casques modulables : avantages et inconvénients",
   "https://www.motoblouz.com/enjoytheride/conseils-equipement/23332-casques-modulables-les-avantages-et-les-inconvenients-2023-06-26"),
  ("France Moto Quad, norme ECE 22.06, homologation et choix en 2026",
   "https://france-moto-quad.fr/blog/casque-moto-homologation-ece-22-06/"),
  ("Dafy Moto, guide des tailles de casque",
   "https://www.dafy-moto.com/comment-choisir-la-taille-de-son-casque-moto.html"),
 ],
},

# =====================================================================
{
 "slug": "protection-auditive-moto",
 "titre": "Protection auditive à moto : bouchons d'oreille, le guide complet",
 "h1": "Quelle protection auditive choisir à moto ?",
 "desc": ("Bruit du vent, seuils de danger, types de bouchons et prix : comment "
          "protéger son audition à moto sans perdre en sécurité."),
 "chapo": ("Ce n'est pas le moteur qui abîme l'audition d'un motard, c'est le "
           "vent. Passé 100 km/h, le niveau sonore sous un casque dépasse "
           "largement les seuils de danger, et les dégâts sont irréversibles. "
           "C'est aussi l'équipement le plus simple à s'offrir : quelques "
           "euros suffisent pour une vraie protection."),
 "sections": [

  {"h2": "Le bruit qui abîme vraiment l'audition",
   "html": """<p>Le réflexe est de penser au bruit du moteur. C'est une erreur :
à vitesse d'autoroute, le bruit qui endommage l'audition vient des
<strong>turbulences aérodynamiques</strong>, le flux d'air qui frappe la
coque du casque, contourne l'écran et entre en résonance à l'intérieur.</p>

<div class="tableau-large"><table class="specs">
<caption>Niveau sonore mesuré sous un casque, selon la vitesse</caption>
<tbody>
<tr><th scope="row">90 km/h</th><td>≈ 90 dB</td></tr>
<tr><th scope="row">100 km/h</th><td>95 à 105 dB</td></tr>
<tr><th scope="row">110 km/h</th><td>≈ 98 dB</td></tr>
<tr><th scope="row">120 à 130 km/h</th><td>95 à 100 dB</td></tr>
</tbody></table></div>

<p>Le seuil de danger reconnu pour une exposition quotidienne est fixé à
<strong>80 à 85 dB</strong>. Au-delà, le risque de lésion augmente avec la
durée d'exposition : à 100 dB, la tolérance tombe à environ 8 minutes. Une
heure d'autoroute sans protection peut suffire à causer des dommages
permanents.</p>

<div class="encart"><p class="encart-titre">Le signal qu'il ne faut pas ignorer</p>
<p>Des oreilles qui sifflent ou bourdonnent après un trajet ne sont pas
normales : ce sont des <strong>acouphènes</strong>, le symptôme d'une
oreille déjà abîmée. Si cela vous arrive régulièrement, l'exposition est
trop forte, pas seulement inconfortable.</p></div>"""},

  {"h2": "Ce que le code de la route autorise",
   "html": """<p>Deux catégories d'objets se ressemblent mais n'ont rien à
voir juridiquement, et la confusion est fréquente.</p>

<div class="encart"><p class="encart-titre">Autorisés</p>
<p>Les <strong>bouchons d'oreille</strong>, passifs ou filtrants, sont
parfaitement légaux à moto. Ils n'émettent aucun son : ce sont des
protections auditives, pas des dispositifs de diffusion. Klaxons, sirènes
et bruit de la circulation restent perceptibles au travers.</p></div>

<div class="encart"><p class="encart-titre">Interdits</p>
<p>Le code de la route interdit au conducteur d'un véhicule motorisé l'usage
d'<strong>écouteurs, oreillettes ou casques audio</strong> diffusant du son
(musique, appels). Une oreillette Bluetooth de téléphone tombe sous le coup
de cette interdiction ; un bouchon filtrant, non.</p></div>

<p>Les bouchons destinés à un usage routier doivent répondre à la norme
<strong>EN 352-2</strong>, qui encadre les équipements de protection
auditive individuels. Leur efficacité se lit sur l'indice <strong>SNR</strong>
(Signal to Noise Ratio), exprimé en décibels : plus il est élevé, plus
l'atténuation est forte.</p>"""},

  {"h2": "Les quatre types de protection, et ce qu'ils valent",
   "html": """<div class="tableau-large"><table class="tab-duel">
<thead><tr><th>Type</th><th>Atténuation</th><th>Prix indicatif</th>
<th>Limite</th></tr></thead>
<tbody>
<tr><th scope="row">Mousse jetable</th><td>30 à 40 dB</td>
<td class="gagne">Quelques centimes à 1 €</td>
<td>Bloque tout uniformément, y compris les sons utiles à la sécurité</td></tr>
<tr><th scope="row">Silicone plein réutilisable</th><td>jusqu'à 90 dB</td>
<td>Quelques euros</td>
<td>Isole trop : on n'entend plus la circulation</td></tr>
<tr><th scope="row">Filtrant spécialisé moto</th><td class="gagne">15 à 30 dB</td>
<td>15 à 28 €</td>
<td>Aucune, c'est le compromis recherché</td></tr>
<tr><th scope="row">Sur-mesure (audioprothésiste)</th><td>18 à 25 dB</td>
<td>100 à 150 €</td>
<td>Prix, délai de fabrication</td></tr>
</tbody></table></div>

<p>Le point contre-intuitif : <strong>un bouchon qui bloque tout n'est pas le
plus sûr.</strong> Un silicone plein à 90 dB d'atténuation supprime aussi le
bruit des voitures autour de vous. Les bouchons filtrants sont conçus
spécifiquement pour couper les basses fréquences du moteur et le sifflement
aérodynamique, tout en laissant passer les médiums, la parole et la
circulation.</p>

<p>Les bouchons sur-mesure, moulés sur votre conduit auditif chez un
audioprothésiste, offrent le meilleur confort sur de longues durées. Certains
motards en rapportent <strong>moins de fatigue et une disparition des
sifflements</strong> en fin de journée par rapport aux modèles filtrants du
commerce. Le prix inclut la prise d'empreinte, et l'équipement peut être
partiellement remboursé par certaines mutuelles sur ordonnance.</p>""" +
   bloc_achat(["bouchons", "bouchons-amazon", "bouchons-amazon-2"])},

  {"h2": "Bien les mettre, et les entretenir",
   "html": """<ul class="tick">
<li><strong>Mousse jetable</strong> : se roule entre les doigts avant
insertion, se laisse quelques secondes pour reprendre sa forme dans le
conduit. À usage limité, une paire ne se réutilise pas indéfiniment.</li>
<li><strong>Filtrants réutilisables</strong> : se nettoient à l'eau tiède et
au savon doux entre les sorties ; remplacez-les dès que le silicone durcit
ou se fissure.</li>
<li><strong>Sur-mesure</strong> : entretien identique aux appareils auditifs,
suivez les consignes de l'audioprothésiste.</li>
</ul>
<div class="encart"><p class="encart-titre">Une précaution avant de rouler</p>
<p>Certaines personnes ressentent des vertiges à l'insertion de bouchons
occlusifs. Testez-les chez vous, à l'arrêt, avant votre première sortie
avec.</p></div>"""},

  {"h2": "Et avec un intercom Bluetooth ?",
   "html": """<p>Les bouchons filtrants et sur-mesure sont compatibles avec la
plupart des systèmes d'intercom (Sena, Cardo) : le son des haut-parleurs du
casque traverse la mousse du casque et reste audible par-dessus
l'atténuation. En pratique, beaucoup d'utilisateurs remontent légèrement le
volume de leur intercom une fois équipés.</p>
<p>Les bouchons sur-mesure avec embout creux (permettant le passage du son)
existent chez certains audioprothésistes spécialisés moto : à préciser
explicitement lors de la prise d'empreinte si vous utilisez un intercom au
quotidien.</p>"""},

  {"h2": "Notre lecture",
   "html": """<ul class="tick">
<li><strong>Trajets urbains occasionnels</strong> : la mousse jetable suffit,
pour quelques centimes.</li>
<li><strong>Utilisation régulière, route et autoroute</strong> : un
filtrant spécialisé moto. C'est le meilleur rapport protection/prix pour la
majorité des motards.</li>
<li><strong>Gros rouleurs, longues distances, tous les jours</strong> : le
sur-mesure amortit vite son prix en confort, surtout si une mutuelle en
prend une partie en charge.</li>
<li><strong>Jamais de silicone plein en usage routier</strong> : la sécurité
passe par le fait d'entendre la circulation, pas par l'isolation totale.</li>
</ul>"""},
 ],

 "faq": [
  ("Porter des bouchons d'oreille à moto est-il légal en France ?",
   "Oui, sans restriction. Le code de la route interdit les écouteurs et "
   "oreillettes qui diffusent du son, pas les protections auditives passives "
   "ou filtrantes, qui n'émettent rien."),
  ("Les bouchons d'oreille empêchent-ils d'entendre les sirènes et klaxons ?",
   "Non, pas avec un modèle filtrant correctement dimensionné : ils atténuent "
   "le bruit du vent et du moteur tout en laissant passer les fréquences de "
   "la voix et de la circulation. Un silicone plein très occlusif peut en "
   "revanche trop isoler, ce qui n'est pas recherché sur route."),
  ("Quelle différence entre bouchons filtrants et bouchons classiques ?",
   "Un bouchon classique (mousse ou silicone) atténue toutes les fréquences "
   "de la même manière. Un bouchon filtrant est conçu pour couper "
   "sélectivement les basses fréquences du moteur et le sifflement "
   "aérodynamique, tout en laissant passer la parole et les bruits utiles."),
  ("Le sur-mesure vaut-il vraiment 100 à 150 € par rapport à un modèle à 20 € ?",
   "Le gain se joue sur le confort en usage prolongé et sur l'ajustement "
   "parfait au conduit auditif. Pour un usage occasionnel, un filtrant du "
   "commerce à 15-28 € couvre l'essentiel du besoin ; le sur-mesure se "
   "justifie surtout pour un usage quotidien ou de longues distances "
   "régulières."),
 ],

 "sources": [
  ("Le Repaire des Motards, dossier protection auditive et bruit à moto",
   "https://www.lerepairedesmotards.com/dossiers/protection-auditive-bruit-moto-bouchon-oreille-epi-picb.php"),
  ("Passion Moto Sécurité, se protéger du bruit à moto",
   "https://moto-securite.fr/silence/"),
  ("Moto-Net, comment et pourquoi se protéger du bruit à moto",
   "https://www.moto-net.com/article/comment-et-pourquoi-se-proteger-du-bruit-a-moto.html"),
  ("Nousmotards.com, protection auditive en moto : lois et options disponibles",
   "https://nousmotards.com/protection-auditive-en-moto-lois-et-options-disponibles-sur-le-marche"),
  ("hear-it.org, les motos sont dangereuses pour votre audition",
   "https://www.hear-it.org/fr/les-motos-sont-dangereuses-pour-votre-audition"),
  ("Meilleurtaux, remboursement mutuelle du bouchon d'oreille sur mesure",
   "https://www.meilleurtaux.com/comparateur-assurance/mutuelle-sante/remboursement-mutuelle/remboursement-mutuelle-bouchon-oreille-mesure.html"),
 ],
},

# =====================================================================
{
 "slug": "equipement-moto-budget-complet",
 "titre": "S'équiper à moto : le budget complet en 2026",
 "h1": "S'équiper à moto : combien ça coûte vraiment",
 "desc": ("Casque, blouson, gants, pantalon, bottes, airbag : ce qui est "
          "obligatoire, ce qui est recommandé, et le budget réel poste par poste."),
 "chapo": ("Deux équipements seulement sont obligatoires à moto en France. Le "
           "reste relève de votre jugement, et c'est précisément là que se "
           "joue la différence entre une chute sans conséquence et plusieurs "
           "semaines d'arrêt. Voici ce que chaque poste coûte réellement."),
 "sections": [

  {"h2": "Ce que la loi impose, et ce qu'elle n'impose pas",
   "html": """<div class="encart"><p class="encart-titre">Obligatoire</p>
<ul class="tick">
<li>Un <strong>casque homologué ECE 22.06</strong> (ou 22.05 en bon état),
correctement attaché.</li>
<li>Des <strong>gants certifiés CE</strong>, pour le conducteur et le passager.</li>
<li>Un <strong>gilet de haute visibilité</strong> rangé à bord, à porter en cas
d'immobilisation d'urgence.</li>
</ul></div>

<p>Le manquement expose à une amende de 11 à 135 € et jusqu'à 3 points de
permis.</p>

<div class="encart"><p class="encart-titre">Fortement recommandé, mais pas obligatoire</p>
<p>Blouson certifié CE, dorsale, pantalon renforcé et bottes montantes ne sont
<strong>pas exigés par la loi</strong>. Ils sont recommandés par la sécurité
routière, et ce sont eux qui font la différence en cas de glissade.</p></div>"""},

  {"h2": "Comprendre les normes en trente secondes",
   "html": """<p>Deux sigles à retenir sur les étiquettes.</p>

<h3>EN 17092. Les vêtements</h3>
<p>Cette norme classe blousons et pantalons selon leur résistance à l'abrasion
et aux chocs :</p>
<div class="tableau-large"><table class="specs">
<tbody>
<tr><th scope="row">AAA</th><td>Protection la plus élevée. Combinaisons et
vêtements route/piste.</td></tr>
<tr><th scope="row">AA</th><td>Protection élevée, adaptée aux trajets
quotidiens. <strong>Le bon niveau pour la plupart des motards.</strong></td></tr>
<tr><th scope="row">A</th><td>Protection standard, déplacements urbains.</td></tr>
<tr><th scope="row">B</th><td>Résistance à l'abrasion seulement, sans
protections contre les chocs.</td></tr>
</tbody></table></div>

<h3>EN 1621. Les protections</h3>
<p>Elle concerne les coques d'épaules, coudes, genoux et la dorsale
(EN 1621-2). Un blouson peut être vendu avec des emplacements vides : vérifiez
que les protections sont bien incluses, sinon ajoutez-les au budget.</p>"""},

  {"h2": "Le budget poste par poste",
   "html": """<div class="tableau-large"><table class="specs">
<caption>Ordres de grandeur constatés, neuf, 2026</caption>
<tbody>
<tr><th scope="row">Casque</th><td>150 – 300 € pour un modèle sûr ;
300 – 500 € pour le confort</td></tr>
<tr><th scope="row">Gants certifiés CE</th><td>40 – 120 €</td></tr>
<tr><th scope="row">Blouson CE avec dorsale</th><td>150 – 400 €</td></tr>
<tr><th scope="row">Pantalon renforcé</th><td>100 – 300 €</td></tr>
<tr><th scope="row">Bottes montantes</th><td>100 – 250 €</td></tr>
<tr><th scope="row"><strong>Minimum fonctionnel homologué</strong></th>
<td><strong>≈ 500 €</strong></td></tr>
<tr><th scope="row"><strong>Ensemble complet crédible</strong></th>
<td><strong>800 – 1 500 €</strong></td></tr>
</tbody></table></div>

<p>Un repère qui revient dans les retours du secteur : un motard dépense en
moyenne <strong>30 % du prix de sa moto en équipement la première année</strong>.
Et l'arbitrage le plus souvent recommandé : mieux vaut une moto à 3 000 € avec
1 500 € d'équipement que l'inverse.</p>""" + bloc_achat(
       ["blouson", "gants", "bottes", "pantalon"])},

  {"h2": "Le gilet airbag : faut-il franchir le pas ?",
   "html": """<p>C'est l'équipement dont l'apport en protection est le plus
important depuis le casque. Deux technologies coexistent, avec des modèles
économiques très différents.</p>

<div class="tableau-large"><table class="tab-duel">
<thead><tr><th>Critère</th><th>Électronique (type In&amp;motion)</th>
<th>Filaire (type Helite)</th></tr></thead>
<tbody>
<tr><th scope="row">Déclenchement</th><td class="gagne">Capteurs analysant la
position, sans liaison à la moto</td><td>Câble relié à la moto</td></tr>
<tr><th scope="row">Prix du gilet</th><td>400 – 700 €</td>
<td class="gagne">≈ 550 – 600 €</td></tr>
<tr><th scope="row">Boîtier</th><td>≈ 400 € à l'achat, ou 12 €/mois
(≈ 120 €/an)</td><td class="gagne">Aucun</td></tr>
<tr><th scope="row">Réarmement après déclenchement</th><td>Retour atelier ou
cartouche</td><td class="gagne">Cartouche remplaçable soi-même,
≈ 59 – 95 €</td></tr>
<tr><th scope="row">Contrainte</th><td>Batterie à recharger</td>
<td class="gagne">Penser à se connecter et déconnecter</td></tr>
</tbody></table></div>

<p>En pratique, le choix dépend de l'usage. L'électronique autonome est plus
adapté en ville et aux trajets courts, où l'on descend souvent de la machine.
Le filaire convient bien aux longues étapes : pas de batterie à gérer, et la
cartouche se change soi-même en quelques minutes.</p>

<p class="mention">À noter : le gilet airbag n'est obligatoire pour aucun usage
routier en France.</p>""" + bloc_achat(["airbag"])},

  {"h2": "Par quoi commencer avec un budget serré",
   "html": """<p>Si vous ne pouvez pas tout acheter d'un coup, cet ordre limite
le mieux le risque :</p>
<ul class="tick">
<li><strong>1. Le casque et les gants.</strong> Obligatoires, et les mains sont
ce qu'on pose au sol en premier.</li>
<li><strong>2. Le blouson certifié AA avec dorsale.</strong> Le poste qui
protège la plus grande surface.</li>
<li><strong>3. Les bottes montantes.</strong> La cheville se casse vite et se
répare mal.</li>
<li><strong>4. Le pantalon renforcé.</strong> Un jean ordinaire ne résiste que
quelques dixièmes de seconde à l'abrasion.</li>
<li><strong>5. Le gilet airbag</strong>, quand le budget le permet.</li>
</ul>
<p>Rappel qui vaut pour tous les postes : l'équipement d'occasion est
déconseillé pour tout ce qui absorbe un choc, casque, dorsale, protections.
Vous ne pouvez pas savoir ce qu'ils ont déjà encaissé.</p>"""},
 ],

 "faq": [
  ("Quels équipements sont réellement obligatoires à moto ?",
   "Trois seulement : un casque homologué et attaché, des gants certifiés CE "
   "pour le conducteur et le passager, et un gilet de haute visibilité rangé à "
   "bord. Le blouson, le pantalon et les bottes sont recommandés mais non "
   "imposés."),
  ("Que signifie la mention AA sur un blouson ?",
   "C'est le niveau de la norme EN 17092 : AA correspond à une protection "
   "élevée, adaptée aux trajets quotidiens. AAA est le niveau supérieur, A un "
   "niveau standard urbain, B une simple résistance à l'abrasion sans "
   "protections contre les chocs."),
  ("Quel budget minimum pour s'équiper correctement ?",
   "Environ 500 € pour un ensemble fonctionnel et homologué, et 800 à 1 500 € "
   "pour un équipement complet et crédible en neuf."),
  ("Le gilet airbag est-il obligatoire ?",
   "Non, aucun usage routier ne l'impose en France. C'est toutefois l'apport de "
   "protection le plus significatif après le casque."),
 ],

 "sources": [
  ("Le Repaire des Motards, équipement du pilote : les normes européennes",
   "https://www.lerepairedesmotards.com/dossiers/equipement-protection-moto-norme-europeenne.php"),
  ("ESR Formations, équipement obligatoire permis moto 2026",
   "https://www.esrformations.fr/equipement-obligatoire-permis-moto/"),
  ("Boutique Biker, guide de l'équipement moto 2026",
   "https://www.boutique-biker.com/blogs/blog-moto/le-guide-ultime-de-lequipement-moto-2026"),
  ("3AS Racing, budget moto débutant, le vrai coût tout compris",
   "https://blog.3as-racing.com/budget-moto-debutant-vrai-cout-tout-compris-2026/"),
  ("Belles Machines, comparatif des gilets airbag moto 2026",
   "https://bellesmachines.com/test-airbag-moto/"),
  ("Moto Scoot Services, gilets airbag sans abonnement",
   "https://moto-scoot-services.fr/meilleur-gilet-airbag-sans-abonnement"),
 ],
},

# =====================================================================
{
 "slug": "assurance-moto-payer-moins-cher",
 "titre": "Assurance moto : comment payer moins cher en 2026",
 "h1": "Assurance moto : payer moins cher",
 "desc": ("Prix moyens 2026, formules, et les leviers chiffrés pour réduire "
          "sa prime d'assurance moto sans réduire sa protection."),
 "chapo": ("L'assurance est le poste que les motards découvrent après avoir "
           "signé le bon de commande, et c'est une erreur : selon le modèle et "
           "le profil, l'écart annuel se compte en centaines d'euros. Voici les "
           "prix réels et les leviers qui fonctionnent, avec leur effet chiffré."),
 "sections": [

  {"h2": "Ce que ça coûte réellement",
   "html": """<div class="tableau-large"><table class="specs">
<caption>Tarifs annuels constatés, 2026</caption>
<tbody>
<tr><th scope="row">Au tiers (minimum légal)</th><td>≈ 455 €</td></tr>
<tr><th scope="row">Intermédiaire (vol et incendie)</th><td>≈ 648 €</td></tr>
<tr><th scope="row">Tous risques</th><td>≈ 907 €</td></tr>
<tr><th scope="row">Moyenne jeune conducteur A2</th><td>≈ 1 000 €</td></tr>
<tr><th scope="row">Moyenne motard expérimenté</th><td>≈ 540 €</td></tr>
</tbody></table></div>

<p>Le spectre complet va d'environ 230 €/an pour une petite cylindrée au tiers
à plus de 3 000 €/an pour une grosse machine en tous risques.</p>

<div class="encart"><p class="encart-titre">La surprime jeune conducteur</p>
<p>Elle s'applique par paliers dégressifs : <strong>100 % la première année,
50 % la deuxième, 25 % la troisième</strong>, puis disparaît. Votre première
année coûte donc le double du tarif de référence, un point à intégrer au budget
avant l'achat, pas après.</p></div>""" + bloc_achat(
       ["assurance"], "Comparer les tarifs")},

  {"h2": "Les leviers qui marchent, et de combien",
   "html": """<p>Chaque levier ci-dessous a un effet mesurable. Cumulés, ils
transforment la facture.</p>

<div class="tableau-large"><table class="specs">
<caption>Effet constaté sur la prime</caption>
<tbody>
<tr><th scope="row">Comparer les offres en ligne</th>
<td><strong>≈ 281 € d'économie moyenne</strong></td></tr>
<tr><th scope="row">Passer la franchise vol de 150 à 300 €</th>
<td>−10 à −15 %</td></tr>
<tr><th scope="row">Antivol homologué SRA</th><td>−5 à −10 %</td></tr>
<tr><th scope="row">Stationnement en garage fermé déclaré</th><td>−5 à −8 %</td></tr>
<tr><th scope="row">Paiement annuel plutôt que mensuel</th><td>Variable, souvent
quelques pourcents</td></tr>
<tr><th scope="row">Regrouper auto, moto et habitation</th><td>Variable selon
l'assureur</td></tr>
</tbody></table></div>

<p><strong>Le premier levier est de loin le plus rentable</strong>, et c'est
aussi le plus rapide : une comparaison en ligne prend quelques minutes pour près
de 300 € d'écart moyen. Faites-la avant chaque échéance annuelle, pas seulement
à la souscription.</p>

<h3>Le bonus-malus, le levier de long terme</h3>
<p>Chaque année sans accident responsable vous fait gagner <strong>5 % de
réduction</strong>. Après treize ans sans sinistre, vous atteignez le bonus
maximal de 50 % : votre prime est quasiment divisée par deux. C'est
l'argument le plus fort en faveur d'une conduite prudente les premières
années, au-delà de la sécurité elle-même.</p>"""},

  {"h2": "Le choix du modèle pèse lourd",
   "html": """<p>C'est le point que les guides d'achat oublient presque toujours.
À usage et profil identiques, deux motos de puissance comparable peuvent
présenter des primes très différentes. Les assureurs tiennent compte du
positionnement de la marque, du coût des pièces détachées et de l'attractivité
du modèle pour le vol.</p>

<p>Un exemple concret revient souvent : une Triumph Trident 660 coûte
sensiblement plus cher à assurer pour un jeune permis qu'une japonaise de
puissance équivalente, précisément pour ces raisons.</p>

<div class="encart"><p class="encart-titre">Le réflexe à prendre</p>
<p>Demandez <strong>trois devis d'assurance avant de signer le bon de
commande</strong>. Un écart de 300 €/an sur trois ans représente 900 €, soit
davantage que la différence de prix entre deux modèles que vous hésitez à
départager.</p></div>"""},

  {"h2": "Quelle formule choisir",
   "html": """<ul class="tick">
<li><strong>Au tiers</strong>, pertinent pour une moto d'occasion de faible
valeur, typiquement en dessous de 3 000 €. En cas de destruction, vous perdez
la machine, mais la prime reste basse.</li>
<li><strong>Intermédiaire</strong>, le bon compromis dès que le vol devient un
vrai risque : stationnement en extérieur, zone urbaine, modèle recherché.</li>
<li><strong>Tous risques</strong>, cohérent sur une moto neuve ou récente, et
souvent exigé en cas de financement à crédit.</li>
</ul>
<p>Attention à un piège classique : une formule tous risques avec une franchise
très élevée peut coûter cher tout en vous laissant supporter l'essentiel d'un
petit sinistre. Lisez le montant des franchises, pas seulement l'intitulé de la
formule.</p>"""},
 ],

 "faq": [
  ("Combien coûte une assurance moto pour un jeune permis A2 ?",
   "Environ 1 000 € par an en moyenne en 2026, contre environ 540 € pour un "
   "motard expérimenté. S'y ajoute la surprime jeune conducteur : 100 % la "
   "première année, 50 % la deuxième, 25 % la troisième."),
  ("Quel est le moyen le plus efficace de réduire sa prime ?",
   "Comparer les offres en ligne, avec une économie moyenne constatée d'environ "
   "281 €. Viennent ensuite l'augmentation de la franchise vol (−10 à −15 %), "
   "l'antivol homologué SRA (−5 à −10 %) et le stationnement en garage fermé "
   "(−5 à −8 %)."),
  ("Le modèle de moto change-t-il vraiment le prix ?",
   "Oui, sensiblement. Les assureurs tiennent compte du positionnement de la "
   "marque, du coût des pièces et du risque de vol. Demandez trois devis avant "
   "de signer le bon de commande."),
  ("Au bout de combien de temps atteint-on le bonus maximum ?",
   "Treize ans sans sinistre responsable, avec 5 % de réduction gagnés chaque "
   "année, pour un bonus maximal de 50 %."),
 ],

 "sources": [
  ("Jeune Motard, prix de l'assurance moto A2 en 2026",
   "https://jeunemotard.fr/assurance-articles/prix-assurance-moto-a2/"),
  ("Actual Assurance, assurance moto 2026 : prix, garanties et comment payer moins cher",
   "https://actualassurance.fr/blog/assurance-moto-2026-prix-garanties-et-comment-payer-moins-cher"),
  ("Leocare, prix de l'assurance moto 2026",
   "https://leocare.eu/fr/assurance-moto-scooter-en-ligne/prix/"),
  ("Tout pour la Moto, assurance moto moins chère en 2026, méthodes concrètes",
   "https://www.toutpourlamoto.fr/assurance-moto-moins-chere-2026-2"),
  ("LeLynx, assurance moto jeune conducteur : prix et garanties",
   "https://www.lelynx.fr/assurance-moto/jeune-conducteur/"),
 ],
},

]
