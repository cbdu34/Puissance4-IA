# Puissance 4 — IA Minimax

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-required-013243.svg?logo=numpy)](https://numpy.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

> Jeu de Puissance 4 en Python avec une interface Tkinter et une IA basée sur l'algorithme **Minimax** avec **élagage alpha-bêta** (profondeur 5).

Projet réalisé en autonomie à 12 ans.

---

## ✨ Fonctionnalités

- 🎮 **Puissance 4 classique** : grille 6 × 7, alignement de 4 pions pour gagner.
- 🧠 **IA Minimax + alpha-bêta** : exploration de 5 coups à l'avance.
- 📊 **Évaluation par segments** : détection des alignements de 2, 3 et 4 pions, blocage des menaces adverses et bonus pour la colonne centrale.
- ⚡ **Optimisations** : élagage alpha-bêta et tri des coups du centre vers les bords.
- 🖥️ **Interface graphique** : rendu Canvas, survol des colonnes et pop-up de fin de partie pour rejouer.
- 🔢 **Plateau NumPy** : calculs matriciels pour une évaluation rapide.

---

## 🚀 Installation

```bash
git clone https://github.com/cbdu34/Puissance4-IA.git
cd Puissance4-IA
pip install -r requirements.txt
```

Tkinter est inclus avec Python sous Windows et macOS. Sous Linux :

```bash
sudo apt install python3-tk
```

---

## ▶️ Lancer le jeu

```bash
python puissance4.py
```

Cliquez sur une colonne pour jouer. L'IA répond automatiquement.

---

## 🧠 Fonctionnement de l'IA

1. **Génération des coups** : seules les colonnes non pleines sont considérées.
2. **Minimax** : l'IA maximise son score, le joueur le minimise.
3. **Alpha-bêta** : coupe les branches inutiles pour accélérer la recherche.
4. **Évaluation** : chaque segment de 4 cases est noté (4 pions = victoire, 3 pions + 1 vide = menace, etc.).
5. **Profondeur 5** : l'IA anticipe 5 coups, ce qui la rend très difficile à battre.

---

## 📄 Licence

Distribué sous licence **GNU GPL v3**. Voir le fichier [LICENSE](LICENSE).
