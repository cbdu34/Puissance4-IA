import numpy as np
import random
import math
import tkinter as tk
from tkinter import messagebox

# Configurations du jeu
LIGNES = 6
COLONNES = 7
VIDE = 0
JOUEUR = 1
IA = 2
LONGUEUR_ALIGNEMENT = 4

# Dimensions de l'interface
TAILLE_CASE = 80
LARGEUR_CANVAS = COLONNES * TAILLE_CASE
HAUTEUR_CANVAS = LIGNES * TAILLE_CASE
RAYON = (TAILLE_CASE // 2) - 5

# Couleurs
COULEUR_FOND = "#1E3A8A"  # Bleu foncé pour la grille
COULEUR_VIDE = "#374151"  # Gris foncé pour les cases vides
COULEUR_JOUEUR = "#EF4444"  # Rouge pour le joueur (X)
COULEUR_IA = "#FBBF24"      # Jaune pour l'IA (O)

# =====================================================================
# MOTEUR DE JEU (LOGIQUE)
# =====================================================================

def creer_grille():
    return np.zeros((LIGNES, COLONNES), dtype=int)

def coup_valide(grille, col):
    return grille[LIGNES-1][col] == VIDE

def obtenir_ligne_dispo(grille, col):
    for l in range(LIGNES):
        if grille[l][col] == VIDE:
            return l

def jouer_pion(grille, ligne, col, pion):
    grille[ligne][col] = pion

def verifier_victoire(grille, pion):
    # Horizontal
    for l in range(LIGNES):
        for c in range(COLONNES - 3):
            if all(grille[l][c+i] == pion for i in range(LONGUEUR_ALIGNEMENT)):
                return True
    # Vertical
    for l in range(LIGNES - 3):
        for c in range(COLONNES):
            if all(grille[l+i][c] == pion for i in range(LONGUEUR_ALIGNEMENT)):
                return True
    # Diagonale (/)
    for l in range(LIGNES - 3):
        for c in range(COLONNES - 3):
            if all(grille[l+i][c+i] == pion for i in range(LONGUEUR_ALIGNEMENT)):
                return True
    # Diagonale (\)
    for l in range(3, LIGNES):
        for c in range(COLONNES - 3):
            if all(grille[l-i][c+i] == pion for i in range(LONGUEUR_ALIGNEMENT)):
                return True
    return False

def evaluer_segment(segment, pion):
    score = 0
    adversaire = JOUEUR if pion == IA else IA
    nb_pion = segment.count(pion)
    nb_vide = segment.count(VIDE)
    nb_adv = segment.count(adversaire)

    if nb_pion == 4:
        score += 1000
    elif nb_pion == 3 and nb_vide == 1:
        score += 50
    elif nb_pion == 2 and nb_vide == 2:
        score += 10

    if nb_adv == 3 and nb_vide == 1:
        score -= 80  
    return score

def evaluer_grille(grille, pion):
    score = 0
    col_centrale = [int(i) for i in list(grille[:, COLONNES//2])]
    score += col_centrale.count(pion) * 3

    for l in range(LIGNES):
        ligne_complete = [int(i) for i in list(grille[l, :])]
        for c in range(COLONNES - 3):
            segment = ligne_complete[c:c+LONGUEUR_ALIGNEMENT]
            score += evaluer_segment(segment, pion)

    for c in range(COLONNES):
        col_complete = [int(i) for i in list(grille[:, c])]
        for l in range(LIGNES - 3):
            segment = col_complete[l:l+LONGUEUR_ALIGNEMENT]
            score += evaluer_segment(segment, pion)

    for l in range(LIGNES - 3):
        for c in range(COLONNES - 3):
            segment = [grille[l+i][c+i] for i in range(LONGUEUR_ALIGNEMENT)]
            score += evaluer_segment(segment, pion)

    for l in range(3, LIGNES):
        for c in range(COLONNES - 3):
            segment = [grille[l-i][c+i] for i in range(LONGUEUR_ALIGNEMENT)]
            score += evaluer_segment(segment, pion)
    return score

def obtenir_coups_valides(grille):
    return [c for c in range(COLONNES) if coup_valide(grille, c)]

def ordonner_coups(grille, coups_valides):
    return sorted(coups_valides, key=lambda c: abs(c - (COLONNES // 2)))

def est_noeud_terminal(grille):
    return verifier_victoire(grille, JOUEUR) or verifier_victoire(grille, IA) or len(obtenir_coups_valides(grille)) == 0

def minimax(grille, profondeur, alpha, beta, maximisant):
    coups_valides = obtenir_coups_valides(grille)
    terminal = est_noeud_terminal(grille)

    if profondeur == 0 or terminal:
        if terminal:
            if verifier_victoire(grille, IA):
                return (None, 10000000 + profondeur)
            elif verifier_victoire(grille, JOUEUR):
                return (None, -10000000 - profondeur)
            else:
                return (None, 0)
        else:
            return (None, evaluer_grille(grille, IA))

    coups_ordonnes = ordonner_coups(grille, coups_valides)

    if maximisant:
        valeur = -math.inf
        meilleure_col = random.choice(coups_valides) if coups_valides else None
        for col in coups_ordonnes:
            ligne = obtenir_ligne_dispo(grille, col)
            copie_grille = grille.copy()
            jouer_pion(copie_grille, ligne, col, IA)
            _, nouveau_score = minimax(copie_grille, profondeur - 1, alpha, beta, False)
            if nouveau_score > valeur:
                valeur = nouveau_score
                meilleure_col = col
            alpha = max(alpha, valeur)
            if alpha >= beta:
                break
        return meilleure_col, valeur
    else:
        valeur = math.inf
        meilleure_col = random.choice(coups_valides) if coups_valides else None
        for col in coups_ordonnes:
            ligne = obtenir_ligne_dispo(grille, col)
            copie_grille = grille.copy()
            jouer_pion(copie_grille, ligne, col, JOUEUR)
            _, nouveau_score = minimax(copie_grille, profondeur - 1, alpha, beta, True)
            if nouveau_score < valeur:
                valeur = nouveau_score
                meilleure_col = col
            beta = min(beta, valeur)
            if alpha >= beta:
                break
        return meilleure_col, valeur

# =====================================================================
# INTERFACE GRAPHIQUE (TKINTER)
# =====================================================================

class Puissance4Graphique:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Puissance 4 - IA Minimax")
        self.fenetre.resizable(False, False)
        
        # Zone de texte pour afficher le statut du tour
        self.label_statut = tk.Label(fenetre, text="Initialisation...", font=("Helvetica", 14, "bold"), pady=10)
        self.label_statut.pack()

        # Canvas pour dessiner le plateau
        self.canvas = tk.Canvas(fenetre, width=LARGEUR_CANVAS, height=HAUTEUR_CANVAS, bg=COULEUR_FOND)
        self.canvas.pack()
        
        # Liaison du clic de souris
        self.canvas.bind("<Button-1>", self.gestion_clic)

        self.reinitialiser_jeu()

    def reinitialiser_jeu(self):
        self.grille = creer_grille()
        self.jeu_termine = False
        self.tour = random.choice([JOUEUR, IA])
        self.dessiner_plateau()
        self.mettre_a_jour_statut()

        # Si l'IA commence, on déclenche son calcul après un léger délai
        if self.tour == IA:
            self.fenetre.after(500, self.tour_ia)

    def dessiner_plateau(self):
        self.canvas.delete("all")
        # On dessine les cases en inversant l'affichage des lignes pour que l'index 0 soit en bas
        for l in range(LIGNES):
            for c in range(COLONNES):
                x1 = c * TAILLE_CASE + (TAILLE_CASE // 2) - RAYON
                y1 = (LIGNES - 1 - l) * TAILLE_CASE + (TAILLE_CASE // 2) - RAYON
                x2 = x1 + 2 * RAYON
                y2 = y1 + 2 * RAYON

                if self.grille[l][c] == VIDE:
                    couleur = COULEUR_VIDE
                elif self.grille[l][c] == JOUEUR:
                    couleur = COULEUR_JOUEUR
                else:
                    couleur = COULEUR_IA

                self.canvas.create_oval(x1, y1, x2, y2, fill=couleur, outline="")

    def mettre_a_jour_statut(self):
        if self.jeu_termine:
            return
        if self.tour == JOUEUR:
            self.label_statut.config(text="Votre tour (Rouge)", fg=COULEUR_JOUEUR)
        else:
            self.label_statut.config(text="L'IA réfléchit... (Jaune)", fg=COULEUR_IA)

    def gestion_clic(self, event):
        # Bloquer le clic si le jeu est fini ou si c'est le tour de l'IA
        if self.jeu_termine or self.tour != JOUEUR:
            return

        # Déterminer la colonne cliquée
        col = event.x // TAILLE_CASE

        if coup_valide(self.grille, col):
            ligne = obtenir_ligne_dispo(self.grille, col)
            jouer_pion(self.grille, ligne, col, JOUEUR)
            self.dessiner_plateau()

            if verifier_victoire(self.grille, JOUEUR):
                self.fin_de_partie("Félicitations ! Vous avez gagné !")
                return

            if len(obtenir_coups_valides(self.grille)) == 0:
                self.fin_de_partie("Match nul ! La grille est pleine.")
                return

            # Passer le tour à l'IA
            self.tour = IA
            self.mettre_a_jour_statut()
            self.fenetre.after(100, self.tour_ia)

    def tour_ia(self):
        if self.jeu_termine:
            return

        # Calcul du meilleur coup (Profondeur 5 ou 6 recommandée)
        choix, _ = minimax(self.grille, 5, -math.inf, math.inf, True)

        if choix is not None and coup_valide(self.grille, choix):
            ligne = obtenir_ligne_dispo(self.grille, choix)
            jouer_pion(self.grille, ligne, choix, IA)
            self.dessiner_plateau()

            if verifier_victoire(self.grille, IA):
                self.fin_de_partie("L'IA a gagné. Dommage !")
                return

            if len(obtenir_coups_valides(self.grille)) == 0:
                self.fin_de_partie("Match nul ! La grille est pleine.")
                return

            # Retour au joueur
            self.tour = JOUEUR
            self.mettre_a_jour_statut()

    def fin_de_partie(self, message):
        self.jeu_termine = True
        self.label_statut.config(text=message, fg="#10B981") # Vert pour la fin
        
        # Fenêtre pop-up de confirmation pour rejouer
        rejouer = messagebox.askyesno("Fin de partie", f"{message}\n\nVoulez-vous rejouer ?")
        if rejouer:
            self.reinitialiser_jeu()
        else:
            self.fenetre.quit()

# Lancement de l'application
if __name__ == "__main__":
    racine = tk.Tk()
    application = Puissance4Graphique(racine)
    racine.mainloop()