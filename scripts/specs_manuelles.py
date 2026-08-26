# -*- coding: utf-8 -*-
"""
Saisie manuelle : modeles du marche francais absents de Wikipedia.

Douze machines actuelles n'ont aucun article Wikipedia, ni en francais ni en
anglais. Leurs caracteristiques sont saisies ici depuis les fiches
constructeur et la presse specialisee, avec la source de chaque fiche.

Regles :
  - une valeur non trouvee reste absente. On n'estime rien.
  - 'poids' precise toujours s'il s'agit du poids a sec ou tous pleins faits.
  - 'a2' indique si une version A2 homologuee existe au catalogue France.

Pour ajouter un modele : copier un bloc, remplir, indiquer la source.
"""

DATE_SAISIE = "25 août 2026"

MODELES = [

 {"nom": "Triumph Daytona 660", "marque": "Triumph Motorcycles Ltd",
  "annee_debut": 2024, "categorie": "Sportive",
  "cylindree_cc": 660, "architecture": "3 cylindres", "refroidissement": "Liquide",
  "puissance_ch": 95, "puissance_tr_min": 11250,
  "couple_nm": 69, "couple_tr_min": 8250,
  "poids_tous_pleins_kg": 201, "hauteur_selle_mm": 810, "empattement_mm": 1426,
  "reservoir_l": 14, "prix_lancement_eur": 9795,
  "cadre": "Périmétrique en acier tubulaire",
  "freins": "2 disques flottants 310 mm, étriers radiaux 4 pistons, ABS / "
            "disque 220 mm, étrier coulissant, ABS",
  "pneus": "120/70 ZR17 / 180/55 ZR17",
  "a2": "version A2 non confirmée au catalogue",
  "source": "https://www.lerepairedesmotards.com/technique/fiches/tech-triumph-daytona-660.php"},

 {"nom": "Suzuki GSX-8S", "marque": "Suzuki",
  "annee_debut": 2023, "categorie": "Roadster",
  "cylindree_cc": 776, "architecture": "Twin parallèle", "refroidissement": "Liquide",
  "puissance_ch": 82.9, "puissance_tr_min": 8500,
  "couple_nm": 78, "couple_tr_min": 6800,
  "poids_tous_pleins_kg": 202, "hauteur_selle_mm": 810, "empattement_mm": 1465,
  "reservoir_l": 14, "prix_lancement_eur": 8899,
  "cadre": "Tubulaire en acier, bras oscillant en aluminium",
  "freins": "2 disques 310 mm, ABS / disque 240 mm, ABS",
  "pneus": "120/70 ZR17 / 180/55 ZR17",
  "a2": "version A2 disponible",
  "source": "https://www.lerepairedesmotards.com/technique/fiches/tech-suzuki-gsx-8s.php"},

 {"nom": "Suzuki GSX-8R", "marque": "Suzuki",
  "annee_debut": 2024, "categorie": "Sportive",
  "cylindree_cc": 776, "architecture": "Twin parallèle", "refroidissement": "Liquide",
  "puissance_ch": 82.9, "puissance_tr_min": 8500,
  "couple_nm": 78, "couple_tr_min": 6800,
  "poids_tous_pleins_kg": 205, "hauteur_selle_mm": 810, "empattement_mm": 1465,
  "reservoir_l": 14, "prix_lancement_eur": 9699,
  "cadre": "Tubulaire en acier, sous-cadre en tubes d'acier",
  "freins": "2 disques flottants 310 mm, ABS / disque 240 mm, ABS",
  "pneus": "Dunlop Roadsport 2 — 120/70 ZR17 / 180/55 ZR17",
  "a2": "version A2 disponible",
  "source": "https://www.lerepairedesmotards.com/technique/fiches/tech-suzuki-gsx-8r.php"},

 {"nom": "Honda CB650R", "marque": "Honda",
  "annee_debut": 2019, "categorie": "Roadster",
  "cylindree_cc": 649, "architecture": "4 cylindres en ligne", "refroidissement": "Liquide",
  "puissance_ch": 95, "puissance_kw": 70, "puissance_tr_min": 12000,
  "couple_nm": 63, "couple_tr_min": 9500,
  "poids_tous_pleins_kg": 207, "hauteur_selle_mm": 810, "empattement_mm": 1450,
  "reservoir_l": 15.4, "consommation": "4,9 L/100 km (WMTC)",
  "prix_lancement_eur": 9199,
  "freins": "Double disque flottant 310 mm, étrier 4 pistons / disque 240 mm, "
            "étrier 1 piston",
  "pneus": "120/70 R17 / 180/55 R17",
  "a2": "version bridée 35 kW disponible",
  "source": "https://moto.honda.fr/motorcycles/range/street/cb650r/specifications-and-price.html"},

 {"nom": "Honda CBR650R", "marque": "Honda",
  "annee_debut": 2019, "categorie": "Sportive",
  "cylindree_cc": 649, "architecture": "4 cylindres en ligne", "refroidissement": "Liquide",
  "puissance_ch": 95, "puissance_kw": 70, "puissance_tr_min": 12000,
  "couple_nm": 63, "couple_tr_min": 9500,
  "poids_tous_pleins_kg": 211, "hauteur_selle_mm": 810,
  "reservoir_l": 15.4, "prix_lancement_eur": 9949,
  "a2": "version bridée 35 kW disponible",
  "source": "https://moto.honda.fr/motorcycles/range/super-sport/cbr650r/specifications-and-price.html"},

 {"nom": "Honda CB750 Hornet", "marque": "Honda",
  "annee_debut": 2023, "categorie": "Roadster",
  "cylindree_cc": 755, "architecture": "Twin parallèle", "refroidissement": "Liquide",
  "puissance_ch": 92, "puissance_tr_min": 9500,
  "couple_nm": 75.5,
  "poids_tous_pleins_kg": 192, "hauteur_selle_mm": 795, "empattement_mm": 1420,
  "reservoir_l": 15.2, "prix_lancement_eur": 7990,
  "a2": "version bridée 35 kW disponible",
  "source": "https://moto.honda.fr/motorcycles/range/street/hornet/specifications-and-price.html"},

 {"nom": "Honda NX500", "marque": "Honda",
  "annee_debut": 2024, "categorie": "Trail / Aventure",
  "cylindree_cc": 471, "architecture": "Twin parallèle", "refroidissement": "Liquide",
  "puissance_ch": 47, "puissance_tr_min": 8500,
  "couple_nm": 43, "couple_tr_min": 6500,
  "hauteur_selle_mm": 830, "prix_lancement_eur": 6799,
  "freins": "Double disque 296 mm, étriers radiaux 4 pistons",
  "a2": "compatible A2 sans bridage",
  # reservoir : la source annonce 3,1 L, valeur manifestement erronee -> non repris
  "source": "https://moto.honda.fr/motorcycles/range/adventure/nx500/specifications-and-price.html"},

 {"nom": "Aprilia Tuono 660", "marque": "Aprilia",
  "annee_debut": 2021, "categorie": "Roadster",
  "cylindree_cc": 659, "architecture": "Twin parallèle", "refroidissement": "Liquide",
  "puissance_ch": 95, "puissance_tr_min": 10500,
  "couple_nm": 67, "couple_tr_min": 8500,
  "poids_tous_pleins_kg": 183, "poids_sec_kg": 169,
  "hauteur_selle_mm": 820, "empattement_mm": 1370,
  "reservoir_l": 15, "prix_lancement_eur": 10550,
  "cadre": "Double poutre en aluminium, sous-cadre démontable",
  "freins": "2 disques 320 mm, étriers Brembo radiaux 4 pistons, ABS en courbe / "
            "disque 220 mm, étrier Brembo 2 pistons",
  "pneus": "Pirelli Diablo Rosso Corsa II — 120/70 ZR17 / 180/55 ZR17",
  "a2": "version A2 disponible",
  "source": "https://www.lerepairedesmotards.com/technique/fiches/tech-aprilia-tuono-660.php"},

 {"nom": "Husqvarna Svartpilen 401", "marque": "Husqvarna",
  "annee_debut": 2024, "categorie": "Roadster",
  "cylindree_cc": 399, "architecture": "Monocylindre", "refroidissement": "Liquide",
  "puissance_ch": 45, "puissance_kw": 33, "puissance_tr_min": 8500,
  "couple_nm": 39, "couple_tr_min": 7000,
  "poids_sec_kg": 159, "hauteur_selle_mm": 820, "empattement_mm": 1368,
  "reservoir_l": 13, "prix_lancement_eur": 6749,
  "cadre": "Treillis en acier",
  "suspension": "WP APEX, débattement 150 mm avant et arrière",
  "freins": "Disque 320 mm, étrier ByBre, ABS en courbe / disque 230 mm",
  "pneus": "Pirelli Scorpion Rally STR — 110/70 R17 / 150/60 R17",
  "a2": "compatible A2 sans bridage",
  "source": "https://www.lerepairedesmotards.com/technique/fiches/tech-husqvarna-svartpilen-401.php"},

 {"nom": "Kawasaki Ninja 500", "marque": "Kawasaki",
  "annee_debut": 2024, "categorie": "Sportive",
  "cylindree_cc": 451, "architecture": "Twin parallèle", "refroidissement": "Liquide",
  "puissance_ch": 45.4, "puissance_tr_min": 9000,
  "couple_nm": 42.6, "couple_tr_min": 6000,
  "poids_tous_pleins_kg": 171, "hauteur_selle_mm": 785, "empattement_mm": 1375,
  "reservoir_l": 14, "prix_lancement_eur": 6499,
  "suspension": "Fourche télescopique 41 mm, débattement 120 mm / "
                "monoamortisseur Uni Trak, précontrainte réglable",
  "freins": "Disque 310 mm, ABS / disque 220 mm, ABS",
  "pneus": "110/70 R17 / 150/60 R17",
  "a2": "compatible A2 sans bridage",
  "source": "https://www.lerepairedesmotards.com/technique/fiches/tech-kawasaki-ninja-500.php"},

 {"nom": "Kawasaki Eliminator 500", "marque": "Kawasaki",
  "annee_debut": 2024, "categorie": "Custom / Cruiser",
  "cylindree_cc": 451, "architecture": "Twin parallèle", "refroidissement": "Liquide",
  "puissance_ch": 45.4, "puissance_tr_min": 9000,
  "couple_nm": 42.6, "couple_tr_min": 6000,
  "poids_sec_kg": 176, "hauteur_selle_mm": 735, "empattement_mm": 1520,
  "reservoir_l": 13, "prix_lancement_eur": 6499,
  "cadre": "Treillis tubulaire en acier",
  "transmission": "Boîte 6 rapports, embrayage multidisque, chaîne",
  "freins": "Disque 310 mm, ABS / disque 240 mm, ABS",
  "pneus": "130/70-18 / 150/80-16",
  "a2": "compatible A2 sans bridage",
  "source": "https://www.lerepairedesmotards.com/technique/fiches/tech-kawasaki-eliminator-500.php"},

 {"nom": "Kawasaki Versys 1100 S", "marque": "Kawasaki",
  "annee_debut": 2025, "categorie": "Routière / GT",
  "cylindree_cc": 1099, "architecture": "4 cylindres en ligne", "refroidissement": "Liquide",
  "puissance_ch": 106,
  "poids_tous_pleins_kg": 236,
  "reservoir_l": 21, "prix_lancement_eur": 15899,
  "a2": "non",
  "note": "135 ch dans sa version internationale, mais le mode pleine puissance "
          "est limité à 106 ch (78,2 kW) sur le marché français.",
  "source": "https://www.kawasaki.fr/fr_fr/Motorcycles/Adventure_Tourer/Versys_1100_s_2026.html"},

 {"nom": "Kawasaki Z650", "id": "kawasaki-z650-2017", "marque": "Kawasaki",
  "annee_debut": 2017, "categorie": "Roadster",
  "cylindree_cc": 649, "architecture": "Twin parallèle", "refroidissement": "Liquide",
  "puissance_ch": 68, "puissance_tr_min": 8000,
  "couple_nm": 65.7, "couple_tr_min": 6500,
  "poids_tous_pleins_kg": 188, "hauteur_selle_mm": 790, "empattement_mm": 1410,
  "reservoir_l": 15, "prix_lancement_eur": 7299,
  "transmission": "Boîte 6 rapports, embrayage multidisque à bain d'huile "
                  "avec fonction anti-dribble, chaîne",
  "freins": "2 disques 300 mm, étriers 2 pistons / disque 220 mm",
  "pneus": "Dunlop Sportmax Roadsport 2 — 120/70 R17 / 160/60 R17",
  "a2": "version A2 disponible",
  "source": "https://www.lerepairedesmotards.com/technique/fiches/tech-kawasaki-z650.php"},

 {"nom": "Yamaha MT-03", "id": "yamaha-mt-03-320", "marque": "Yamaha",
  "annee_debut": 2016, "categorie": "Roadster",
  "cylindree_cc": 321, "architecture": "Twin parallèle", "refroidissement": "Liquide",
  "puissance_ch": 42, "puissance_tr_min": 10750,
  "poids_tous_pleins_kg": 169, "hauteur_selle_mm": 780,
  "prix_lancement_eur": 6899,
  "a2": "compatible A2 sans bridage",
  "note": "À ne pas confondre avec la MT-03 de 2006, un monocylindre de 660 cm³ "
          "sans rapport avec ce modèle.",
  "source": "https://www.motoplanete.us/yamaha/11924/MT-03-320-2026/contact.html"},

]
