# Project Enigma — Simulation de la machine Enigma avec 3 rotors en Python

> **Auteur** : *Aaïshah HULKHOREE*  
> **Langage** : Python 3.8+  
> **Objectif** : Recréer le processus de chiffrement de la célèbre machine Enigma.

---

## Description du projet

Ce projet a pour but de **simuler le fonctionnement de la machine Enigma** utilisée durant la Seconde Guerre mondiale.  
Il permet de comprendre les principes de **substitution**, **permutation** et de **réflexion** utilisés dans le chiffrement.

L’objectif est pédagogique :  
1)Comprendre les bases de la cryptographie symétrique  
2)Reproduire les composants essentiels de la machine (Plugboard, Rotors, Reflecteur)  
3)Pouvoir chiffrer/déchiffrer un message en configurant soi-même les éléments  

---

## Structure du projet

project_enigma/
├─ src/
│ ├─ components/
│ │ ├─ plugboard.py # Module de câblage initial 
│ │ ├─ reflecteur.py # Module de réflexion 
│ │ └─ rotor.py # (à créer)
│ ├─ configuration/
│ │ └─ settings.py
│ ├─ utils/
│ │ ├─ formatage.py
│ │ └─ nettoyage.py
│ └─ main.py
├─ tests/
│ └─ test_plugboard.py
└─ README.md

---

---

## Installation

### Cloner le dépôt
```bash
git clone https://github.com/aaishahhulkhoree/project_enigma
cd project_enigma
```
### Créer un environnement virtuel 
```
python -m venv .venv
source .venv/bin/activate       # Linux / macOS
.venv\Scripts\activate          # Windows
```
### Installer les dépendances 
```
pip install -r requirements.txt
```
## Execution 
Pour lancer le projet 
```
python src/main.py
```

© 2025 – Project Enigma Python




