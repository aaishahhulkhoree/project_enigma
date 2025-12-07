# Project Enigma — Simulation de la machine Enigma (Python)

Auteur : Aaïshah HULKHOREE  
Langage : Python 3.8+  
But : Simuler de façon pédagogique les mécanismes fondamentaux de la machine Enigma (plugboard, rotors, réflecteur) pour chiffrer/déchiffrer des messages à des fins pédagogiques.

---

Table des matières
- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Structure du dépôt](#structure-du-dépôt)
- [Installation](#installation)
- [Usage](#usage)
- [Composants principaux & API](#composants-principaux--api)
- [Détails techniques & formules](#détails-techniques--formules)
- [Fichiers utiles](#fichiers-utiles)
- [Licence & crédits](#licence--crédits)

---

## Description du projet

Ce projet a pour but de **simuler le fonctionnement de la machine Enigma** utilisée durant la Seconde Guerre mondiale.  
Il permet de comprendre les principes de **substitution**, **permutation** et de **réflexion** utilisés dans le chiffrement.

L’objectif est pédagogique :  
1) Comprendre les bases de la cryptographie symétrique  
2) Reproduire les composants essentiels de la machine (Plugboard, Rotors, Reflecteur)  
3) Pouvoir chiffrer/déchiffrer un message en configurant soi-même les éléments  

---

Aperçu
-------
Project Enigma reproduit, de façon pédagogique, le comportement d'une Enigma moderne à 3..8 rotors. La machine supporte :
- plugboard (max 10 paires)
- rotors réels historiques (I..VIII) avec notch et ring setting
- réflecteur (UKW presets)
- interface CLI et GUI simple


## Structure du projet

```text
project_enigma/
├─ src/
│ ├─ components/
│ │ ├─ menu.py
│ │ └─ realtime.py
│ ├─ configuration/
│ │ ├─ configEnigma.py
│ │ └─ configuration.py
│ ├─ core/
│ │ ├─ machineEnigma.py
│ │ ├─ plugboard.py  
│ │ ├─ reflecteur.py
│ │ ├─ rotors.py
│ ├─ data/
│ │ └─ livre_code.json
│ ├─ ui/
│ │ └─ ui.py
│ ├─ utils/
│ │ ├─ formatage.py
│ │ └─ nettoyage.py
│ └─ main.py
└─ README.md
```
---

Fonctionnalités
--------------
- Chiffrement/ déchiffrement symétrique.
- Plugboard jusqu'à 10 paires de connexion (et non 13 paires car la machine Enigma de l'époque n'en avais que 10).
- Rotors historiques I-VIII
- Stepping UKW A, B et C
- Chargement automatique via un livre de code (fichier JSON). Attention, disponible seulement jusqu'à début janvier 2026. 
- Interface graphique légère (popups Tkinter) et menu interactif.
- Nettoyage de texte et groupage en blocs de 5 pour présentation.

Structure du dépôt
------------------
Arborescence principale :
- [src/main.py](src/main.py) — point d'entrée CLI / lance le menu GUI
- [src/components/](src/components/) — implémentation des composants UI & machine
- [src/configuration/configuration.py](src/configuration/configuration.py) — définitions ROTORS / REFLECTORS et utilitaires
- [src/data/livre_code.json](src/data/livre_code.json) — livre de code utilisé pour config automatique
- [src/utils/](src/utils/) — utilitaires de nettoyage/formatage
- [requirements.txt](requirements.txt)

Installation
------------
1. Cloner le dépôt :
   git clone https://github.com/aaishahhulkhoree/project_enigma && cd project_enigma

2. Créer un environnement virtuel :
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux / macOS

3. Installer les dépendances :
   pip install -r requirements.txt

Usage
-----
- Lancer l'interface interactive (GUI) :
  python src/main.py
  - Sans arguments, la UI principale sera affichée.

- Mode CLI (exemples) :
  python src/main.py --msg "HELLO WORLD" --group5
  python src/main.py --date 2025-12-01 --msg "SECRET"

- Options disponibles :
  --date : charger configuration depuis [src/data/livre_code.json](src/data/livre_code.json)  
  --msg  : message à traiter  
  --group5 : afficher la sortie en blocs de 5

Composants principaux & API
---------------------------
- Machine principale : [`core.machineEnigma.MachineEnigma`](src/core/machineEnigma.py) — class qui orchestre plugboard, rotors et réflecteur.
- Plugboard : [`core.plugboard.Plugboard`](src/core/plugboard.py)
- Réflecteur : [`core.reflecteur.Reflecteur`](src/core/reflecteur.py)
- Rotors : [`core.rotors.Rotor`](src/core/rotors.py), créateur : [`core.rotors.create_rotor`](src/core/rotors.py), utilitaire stepping : [`core.rotors.step_triple_rotors`](src/core/rotors.py)
- Config / livre de code : [`configuration.configuration.load_codebook`](src/configuration/configuration.py), parse positions : [`configuration.configuration.parse_positions`](src/configuration/configuration.py), définitions : [`configuration.configuration.ROTORS`](src/configuration/configuration.py), [`configuration.configuration.REFLECTORS`](src/configuration/configuration.py)
- Menu & GUI : [`components.menu.Menu`](src/components/menu.py), GUI helpers : [`ui.ui.demander_rotors_gui`](src/ui/ui.py), [`ui.ui.demander_positions_gui`](src/ui/ui.py), [`components.ui.popup_menu`](src/ui/ui.py), [`ui.ui.input_dialog`](src/ui/ui.py)
- Utilitaires texte : [`utils.formatage.only_letters`](src/utils/formatage.py), [`utils.formatage.group5`](src/utils/formatage.py)
- Validation : [`utils.nettoyage.est_liste_paires_valides`](src/utils/nettoyage.py), [`utils.nettoyage.est_majuscule`](src/utils/nettoyage.py)

Détails techniques & formules
-----------------------------
- Le stepping suit le double-stepping classique étendu à 3..8 rotors. 
- Espace de clés approximatif :
  - permutations d'ordre des rotors: par exemple pour n rotors pris depuis 8 disponibles → P(8,n)
  - positions initiales: $26^n$
  - plugboard : combinaison en fonction du nombre p de paires (formule factorielle utilisée dans l'UI)
- Groupage radio classique : [`utils.formatage.group5`](src/utils/formatage.py)

Fichiers utiles
---------------
- src/main.py — entrée principale CLI/GUI
- core/machineEnigma.py — cœur du chiffrement
- core/rotors.py — logique du rotor
- core/plugboard.py — permutation entrée/sortie
- configuration/configuration.py — gestion du livre de code
- data/livre_code.json — configurations journalières d’exemple
- utils/ — nettoyage & validation

Licence & crédits
-----------------
Projet éducatif — crédits à l'auteur mentionnée en entête. Voir [requirements.txt](requirements.txt) pour dépendances minimales.
© 2025 – Project Enigma Python
