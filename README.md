# Base de données motos

Base de 1 763 modèles construite à partir de Wikipédia (anglophone et francophone)
et d'une saisie manuelle, normalisée pour
alimenter un annuaire / comparateur moto francophone.

Générée le 24 août 2026.

## Livrables

| Fichier | Contenu | Usage |
|---|---|---|
| `data/out/modeles.csv` | 1 763 modèles × 69 colonnes | Source de vérité machine. Import WordPress / base SQL |
| `data/out/marques.csv` | 65 marques | Table de référence |
| `data/out/duels.csv` | 375 duels « A vs B » | Plan éditorial prêt à l'emploi |
| `data/out/base_motos.xlsx` | 6 feuilles | Travail manuel, tri, filtrage |

Les CSV sont en UTF-8 avec BOM (`utf-8-sig`) : ils s'ouvrent correctement dans Excel
français sans manipulation.

## Chiffres clés

- **1 763** modèles, **65** marques
- **1 290** modèles de marques distribuées en France
- **393** modèles ayant une page Wikipédia française (proxy de notoriété)
- **645** fiches à plus de 80 % de complétude — c'est ton lot de démarrage
- **437** modèles compatibles permis A2 (calculé, pas recopié)
- **1 330** modèles avec une image, **1 317** sous licence libre vérifiée
- **393** noms commerciaux français, **46** prix de lancement en euros validés
- **375** duels générés, dont **276** inter-écoles

## Répartition par école

| École | Modèles |
|---|---|
| Japonaise | 677 |
| Italienne | 228 |
| Britannique | 199 |
| Allemande | 94 |
| Indienne | 57 |
| Américaine | 44 |
| Autrichienne | 29 |
| Autres | 40 |

## Source et licence

**Origine** : Wikipédia anglophone, infobox `Motorcycle`, extraites via l'API MediaWiki.

**Licence : CC BY-SA 4.0.** Deux obligations concrètes :

1. **Créditer** Wikipédia. La colonne `url_wikipedia` contient le lien de l'article
   source pour chaque ligne — conserve-la et affiche-la sur les fiches.
2. **Partager à l'identique** les contenus dérivés du texte Wikipédia.

Point important : les **données factuelles brutes** (cylindrée, poids, puissance) ne
sont pas protégeables en elles-mêmes — c'est leur mise en forme et la structure de la
base qui le sont. En pratique : réutilise les chiffres librement, mais **ne recopie
jamais un texte de description**, réécris-le.

Les images ont **leurs propres licences**. Elles ont été récupérées une par une depuis
Commons : colonnes `image_licence`, `image_auteur` et `image_utilisable`. 1 317 images
sont sous licence libre ; 2 sont restrictives et automatiquement exclues du site.

## Fiabilité

Trois garanties méthodologiques :

**Aucune valeur inventée.** Une cellule vide signifie que la donnée est absente de la
source, jamais qu'elle vaut zéro. Aucune estimation, aucune interpolation.

**Conversions vérifiées.** 9 modèles de référence contrôlés contre les fiches
constructeur : **9 valeurs conformes, 0 écart supérieur à 6 %**. Les conversions
impériales → métriques (lb→kg, cuin→cm³, mph→km/h, hp→ch) sont fiables.

**Valeurs aberrantes effacées.** 141 valeurs hors bornes physiques détectées et
supprimées plutôt que corrigées à l'aveugle (ex. une hauteur de selle de 74 mm dans
la source). La feuille « A vérifier » du classeur liste les 78 fiches concernées.

## Colonnes à connaître

| Colonne | Rôle |
|---|---|
| `priorite` | Score éditorial : notoriété + pertinence France + qualité. **Trie dessus.** |
| `completude_pct` | Part des 15 champs clés remplis |
| `marche_fr` | Marque distribuée en France — filtre principal |
| `a_version_fr` | Une page Wikipédia française existe |
| `vues_60j` | Consultations Wikipédia sur 60 jours |
| `a2_compatible` | Calculé : ≤ 35 kW **et** ≤ 0,2 kW/kg |
| `ecole` | japonaise / italienne / américaine / britannique… |
| `alertes` | Incohérences détectées, à vérifier à la main |

Le dictionnaire complet des 68 colonnes est dans la feuille « Dictionnaire » du classeur.

## Limites connues

**Articles de famille.** Certains articles couvrent plusieurs générations (Ducati
Monster, Suzuki SV650, Honda CBR600RR). Leur infobox utilise un tableau au lieu de
valeurs uniques, donc les champs chiffrés ressortent vides. À compléter manuellement.

**Granularité modèle, pas millésime.** La base est au niveau *modèle*, pas
*année-modèle*. Un comparateur fin exigera d'éclater les générations.

**Prix : couverture très faible.** Le champ « Prix à sa sortie » de Wikipédia FR
mélange euros, francs, Reichsmark et dollars. Après validation stricte de la devise,
**46 prix seulement** ont été conservés sur 98 extraits — les autres ont été rejetés
plutôt que publiés faux. C'est un prix *au lancement*, pas un prix de marché actuel.
Pour couvrir le reste, il faudra une autre source (tarifs constructeurs, saisie manuelle).

**Noms commerciaux : 393 modèles enrichis.** La colonne `nom_affichage` donne le nom
français quand une page Wikipédia FR existe (Africa Twin, R 1200 GS…), sinon la
désignation anglophone. Les 1 072 restants gardent leur code technique.

**Complétude moyenne 60 %.** Correcte pour démarrer, insuffisante pour un comparateur
exhaustif. Les 416 fiches à ≥ 80 % sont utilisables telles quelles.

## Ordre de travail conseillé

1. Filtrer `completude_pct >= 80` et `marche_fr = oui` → ton lot 1
2. Trier par `priorite` décroissante, garder les 150 premières
3. Vérifier la colonne `alertes` sur ce lot, puis publier
4. Ouvrir `duels.csv`, prendre les 20 premières lignes comme plan éditorial

## Reproduire la chaîne

```bash
python scripts/01_collecte.py      # énumère les articles Wikipedia
python scripts/01b_completer.py    # rattrapage des catégories rate-limitées
python scripts/02_infobox.py       # récupère et parse les infobox
python scripts/07_notoriete.py     # vues Wikipedia + versions linguistiques
python scripts/08_categories.py    # catégories d'articles (typologie)
python scripts/03_normalise.py     # normalisation + conversion d'unités
python scripts/04_qa.py            # contrôle qualité + nettoyage
python scripts/09_enrichir.py      # noms FR, prix, résumés, licences d'images
python scripts/10_corriger.py      # validation stricte des devises et licences
python scripts/11_images.py        # licences d'images (correctif de normalisation)
python scripts/06_export.py        # export CSV + XLSX
python scripts/20_site.py          # génération du site statique
```

Dépendances : `requests`, `pandas`, `openpyxl`.

Les étapes 01, 02, 07 et 08 interrogent l'API Wikipédia et prennent une dizaine de
minutes au total. Les étapes 03, 04 et 06 sont instantanées et rejouables hors ligne :
c'est là que tu interviens si tu veux modifier le schéma, les règles de catégorisation
ou le scoring des duels.

---

# Le site

Généré par `scripts/20_site.py` à partir des CSV. **HTML statique pur** : pas de
base de données, pas de serveur applicatif, pas de plugin à mettre à jour.

```bash
python scripts/20_site.py
```

## Ce qui est produit

| Type de page | Nombre | Exemple |
|---|---|---|
| Fiches modèles | 1 363 | `/motos/yamaha/yamaha-mt-07.html` |
| Duels | 293 | `/duels/yamaha-mt-07-vs-suzuki-gsr-750.html` |
| Marques | 59 | `/marques/honda.html` |
| Écoles | 8 | `/ecoles/japonaise.html` |
| Catégories | 13 | `/categories/roadster.html` |
| **Guides d'achat** | **6** | `/guides/meilleure-moto-permis-a2.html` |
| Comparateur | 1 | `/comparateur.html` |
| **Total** | **1 758** | 17,2 Mo |

Seuls les modèles à plus de 45 % de complétude sont publiés : mieux vaut
1 051 fiches lisibles que 1 465 dont un tiers est vide.

## SEO

- Une page par modèle, URL propre `/motos/<marque>/<modele>.html`
- `<title>` et `<meta description>` uniques, générés depuis les données
- Données structurées **Schema.org** `Product` + `BreadcrumbList` sur chaque fiche
- `sitemap.xml` avec les 1 758 URL et leurs priorités, `robots.txt`
- Maillage interne dense : chaque fiche pointe vers ses duels, sa marque,
  son école, sa catégorie et les autres modèles du constructeur

## La page Duels

Entrée **par modèle** plutôt que par liste : un sélecteur « Quelle moto vous
intéresse ? » groupé par marque (126 modèles, 19 marques). On choisit sa moto,
la page n'affiche que ses duels — avec la machine choisie toujours à gauche.

- URL partageable : `/duels/#yamaha-mt-07` ouvre directement ses comparatifs
- Sans JavaScript, la page affiche les 24 duels les plus consultés : indexable
- Cartes avec les deux photos côte à côte plutôt que des liens textuels

**Scoring rééquilibré** vers le marché actuel : forte prime aux modèles récents
et encore au catalogue, malus pour ceux arrêtés avant 2010, et **plafond de
6 duels par modèle**. Sans ce plafond, la YZF-R7 monopolisait 18 comparatifs et
les sportives des années 1990-2000 saturaient la page — leurs articles Wikipédia
sont très complets, mais l'intention d'achat française est ailleurs.

Résultat : 375 duels générés → **235 retenus**, dominés par des modèles actuels
(Panigale V4, YZF-R9, RS 660, DesertX, R 1200 GS contre Africa Twin).

## Les guides d'achat

Trois guides rédigés, dans `scripts/guides_contenu.py` — **le contenu est séparé
du code**, c'est là qu'on écrit et qu'on corrige sans toucher au générateur.

**Six guides**, répartis en deux fichiers : `scripts/guides_contenu.py` (motos)
et `scripts/guides_equipement.py` (équipement et assurance).

| Guide | Mots | Sources |
|---|---|---|
| Meilleure moto permis A2 | 1 744 | 7 |
| Choisir sa première moto | 1 407 | 6 |
| Meilleure routière pour voyager | 1 188 | 7 |
| Quel casque moto choisir | 1 242 | 5 |
| S'équiper : le budget complet | 992 | 6 |
| Assurance moto : payer moins cher | 920 | 5 |

Les trois derniers ciblent les requêtes les plus rémunératrices en affiliation
(équipement, assurance) et ne dépendent pas de la base de données.

**Méthode assumée et affichée sur chaque page** : aucun essai maison. Les guides
croisent les caractéristiques de la base, les essais de la presse spécialisée et
les retours de propriétaires sur les forums français. Les impressions de conduite
sont résumées et référencées, jamais recopiées. Les points faibles figurent au
même titre que les qualités.

Chaque guide comporte des données structurées `Article` + `FAQPage` (éligible aux
résultats enrichis Google), un sommaire ancré, et des liens vers les fiches du site.

⚠️ **Les liens vers les fiches sont explicites, par identifiant.** Un appariement
approximatif sur le nom avait lié la « Honda CB500 Hornet » (2023) à la CB500 Four
de 1971. Quand aucune fiche ne correspond, la carte l'indique plutôt que de créer
un lien faux — c'est le cas pour la Z650, la Trident 660, la CB650R, la MT-03 et
la Tracer 9 GT, absentes ou non publiées.

## Wikipédia FR comme source principale

La collecte initiale partait de Wikipédia anglophone. Or la version **française
couvre mieux le marché européen** : la Yamaha Tracer 9 y figure alors qu'elle
est absente de la version anglaise.

Les scripts `14_collecte_fr.py` et `15_fusion_fr.py` énumèrent les 26 catégories
constructeur de Wikipédia FR (693 articles), en retiennent 594 avec une infobox
moto, et après dédoublonnage ajoutent **285 modèles inédits**.

Leur complétude moyenne est de **69 %, supérieure à celle de la base anglophone**
— les infobox françaises sont plus systématiquement renseignées.

| | Avant | Après |
|---|---|---|
| Modèles | 1 465 | **1 750** |
| Publiables | 1 165 | **1 423** |
| Fiches à ≥ 80 % | 545 | **636** |
| Compatibles A2 | 349 | **425** |
| Avec prix vérifié | 46 | **78** |
| Duels | 272 | **293** |
| Pages du site | 1 481 | **1 744** |

## Le plafond de Wikipédia

Neuf modèles actuels du marché français **n'ont aucun article Wikipédia**, ni en
français ni en anglais :

Triumph Daytona 660 · Suzuki GSX-8S · Suzuki GSX-8R · Honda CB650R ·
Honda CB750 Hornet · Kawasaki Ninja 500 · Aprilia Tuono 660 ·
Husqvarna Svartpilen 401 · Yamaha MT-09 SP

Aucun réglage du pipeline ne les fera apparaître. Ils ont donc été **saisis à la
main** — voir ci-dessous.

## Saisie manuelle

`scripts/specs_manuelles.py` contient **14 fiches saisies depuis les fiches
constructeur et la presse spécialisée**, chacune avec sa source. Complétude
moyenne : **78 %**, soit au-dessus de la base automatique.

Daytona 660 · GSX-8S · GSX-8R · CB650R · CBR650R · CB750 Hornet · NX500 ·
Tuono 660 · Svartpilen 401 · Ninja 500 · Eliminator 500 · Versys 1100 S ·
Z650 · MT-03

Les 14 ont un **prix constructeur France**, 12 une image libre, 12 un statut A2
confirmé au catalogue.

**Pour en ajouter une** : copier un bloc dans `specs_manuelles.py`, remplir, et
indiquer la source. Puis relancer `16_manuel.py`, `06_export.py`, `20_site.py`.

Trois règles appliquées :

- **Aucune estimation.** Le réservoir de la NX500 est annoncé à « 3,1 L » par la
  source — valeur manifestement erronée, donc laissée vide plutôt que corrigée
  au jugé.
- **Le poids précise toujours** s'il s'agit du poids à sec ou tous pleins faits.
- **Une saisie manuelle prime** sur une fiche automatique du même modèle, jamais
  l'inverse.

Un cas documenté : la Versys 1100 développe 135 ch à l'international mais son
mode pleine puissance est **limité à 106 ch en France**. C'est la valeur retenue,
avec la nuance indiquée sur la fiche.

## Comblement par Wikipédia FR

Les infobox françaises contiennent les caractéristiques **déjà en unités
métriques**, et les descriptions (cadre, suspensions, freins) directement en
français. Le script `13_specs_fr.py` s'en sert pour combler les trous de la
base anglophone : **343 fiches enrichies**.

Résultat : complétude moyenne **60 % → 65 %**, fiches à plus de 80 %
**416 → 545**, modèles publiables **1 107 → 1 165**.

⚠️ **Le champ « Couple » des infobox FR mélange N·m et m·kg selon les articles.**
Sans marqueur d'unité explicite dans le texte, la valeur n'est pas importée :
**198 valeurs rejetées, 30 conservées**. Une case vide vaut mieux qu'un couple
faux d'un facteur 10.

## Garde-fou sur les liens de guide

Les guides pointent vers les fiches par **identifiant explicite**, jamais par
correspondance de nom. Un appariement approximatif avait lié la « CB500 Hornet »
(2023) à la CB500 Four de 1971, puis la « Z650 » (2017) à la Z650 de 1977.

Le générateur refuse désormais tout lien vers une machine antérieure à 2005 et
l'signale en console. Quand aucune fiche récente ne correspond, la carte affiche
« fiche pas encore disponible » plutôt qu'un lien faux.

## Images

Les fiches pointaient vers les **fichiers originaux** de Wikimedia, jusqu'à 1 Mo
pièce. Elles utilisent désormais les **vignettes 800-960 px** (~180 Ko), récupérées
via l'API : Wikimedia refuse les largeurs construites à la main (HTTP 400), seule
l'API fournit une URL valide. 1 330 vignettes sur 1 465 modèles.

⚠️ Les images restent **hébergées chez Wikimedia** (hotlink). C'est acceptable au
démarrage, mais déconseillé à l'échelle : pour un site en production il faudra les
télécharger et les servir soi-même. Toutes les URL sont dans la colonne
`image_vignette`, le téléchargement est donc trivial à automatiser.

## Identité visuelle

Palette réchauffée façon atelier (papier brut, sable, oil-black) plutôt que le
gris froid par défaut, avec un accent orange course affirmé (`#b93f0a` en clair,
`#ff7a33` en sombre) et le pétrole déjà présent en secondaire. Les titres, noms
de modèles et boutons passent en **Oswald** (condensé, façon plaque signalétique
d'atelier), auto-hébergée en base64 dans le CSS : zéro requête externe.

Touches mécaniques : bandeau à rayures diagonales sous l'en-tête (référence au
flanc de pneu), badges de rang circulaires sur les cartes de guide, bandes aux
couleurs nationales sur les pages école. Toutes les couleurs (accent y compris)
ont été revérifiées au seuil AA après ce changement de palette.

Ponctuation : le tiret cadratin (—) est banni du contenu éditorial, remplacé
par un point ou une virgule selon le sens de la phrase. Un filet de sécurité
(`sans_emdash()` dans `20_site.py`) nettoie aussi les données brutes issues de
Wikipédia qui en contiendraient encore un.

## Performance

Aucune police externe chargée au runtime (Oswald est auto-hébergée en base64),
aucune bibliothèque JavaScript, aucun appel réseau tiers. Le CSS fait 51 Ko
police incluse, le script du comparateur 2,5 Ko. Les pages pèsent entre 8 et
65 Ko. Les images sont en `loading="lazy"` sauf celles visibles d'emblée.

Le comparateur filtre côté navigateur sur un fichier de 325 Ko chargé une fois :
filtrage instantané, sans appel serveur.

## Conformité

- Crédit photo (auteur + licence + lien) sur chaque fiche
- Mention CC BY-SA et lien vers l'article source en pied de page
- Avertissement sur l'usage indicatif des caractéristiques
- Les 2 images sous licence restrictive sont exclues automatiquement
- Accessibilité : lien d'évitement, focus visible, `aria-label`, contraste,
  thème clair et sombre

## Déployer

Le dossier `site/` est autonome. Trois options gratuites :

```bash
npx wrangler pages deploy site --project-name=cylindree
```

Ou glisser-déposer le dossier `site/` sur [app.netlify.com/drop](https://app.netlify.com/drop).
Ou pousser sur GitHub et brancher Cloudflare Pages / Netlify sur le dépôt.

**Avant de publier**, changer `SITE_URL` en haut de `scripts/20_site.py` pour
mettre le vrai domaine — cette valeur alimente les balises canoniques et le sitemap.

## Prévisualiser en local

```bash
python -m http.server 8899 --directory site
```

Puis ouvrir http://localhost:8899

## Le compromis à connaître

Un site statique n'a pas d'interface d'administration. Pour ajouter un article
ou corriger une fiche, on modifie le CSV (ou le générateur) puis on relance
`python scripts/20_site.py` et on redéploie.

C'est plus simple qu'un WordPress à maintenir, mais moins immédiat qu'un
back-office. Si tu veux écrire des articles régulièrement sans passer par un
fichier, il faudra brancher un CMS externe (Decap CMS, qui fonctionne sur du
statique) ou basculer sur WordPress.
