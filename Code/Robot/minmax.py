from awale import Awale
import sys, copy
from typing import Callable
import random 

# Faire s'affronter methode Monte - Carlo vs MinMax et comparer les % de victoires
# Refaire avec d autres comparaisons avec des fonctions d evaluation et profondeur pour le MinMax
def evaluation(jeu: Awale, joueur_actuel : int):

    # Nombres de cases qui peuvent etre prises a l avantage du joueur d indice i 
    prises_pos = [0,0]
    for i in range(4,8):
        if (Awale.plateau(i) == 1) or (Awale.plateau(i) == 2):
            prises_pos[1] += 1 

    for i in range(0,4):
        if (Awale.plateau(i) == 1) or (Awale.plateau(i) == 2):
            prises_pos[0] += 1 
        

    total = 2*(Awale.score[joueur_actuel]) + prises_pos[joueur_actuel] - 2*(Awale.score[1-joueur_actuel]) + prises_pos[1-joueur_actuel] 
    return total


def minMax(jeu: Awale, profondeur: int, alpha: int, beta: int, joueuramaximiser : bool):
    """Calculer une position.

    Permet de calculer un plateau en se basant sur un algorithme MinMax qui évalue l'arbre des possibilités.

    :param jeu: Partie d'awale à analyser
    :type jeu: Awale
    :param profondeur: Profondeur maximale à laquelle chercher
    :type profondeur: int
    :param alpha: Valeur de alpha
    :type alpha: int
    :param beta: Valeur de beta
    :type beta: int
    :param joueuramaximiser: Booléen indiquant si c'est le joueur à maximiser
    :type joueuramaximiser: bool
    :return: Tuple contenant le meilleur coup et la valeur d'évaluation du noeud
    :rtype: tuple[int, int]
    """
    if (profondeur == 0) or jeu.fin:
        return None,evaluation(jeu.plateau,joueuramaximiser)
    if joueuramaximiser: 
        resultat = - sys.maxsize
        liste_coup_pos = jeu.coupsPossibles()
        meilleur_coup = random.choice(liste_coup_pos) #VERIF SI PAS D ERREUR ICI 
        for i in range(6, 12):
            copie = copy.deepcopy(jeu)
            copie.joue(i)
            nouveau_res = minMax(copie, profondeur-1, alpha, beta, False)[1]
            if nouveau_res > resultat:
                resultat = nouveau_res
                meilleur_coup = i 
            del(copie)
            if beta <= resultat:
                return meilleur_coup,resultat
            alpha = max(alpha, resultat)
    
    # Minimisateur
    else:
        resultat = sys.maxsize
        liste_coup_pos = jeu.coupsPossibles()
        meilleur_coup = random.choice(liste_coup_pos) #VERIF SI PAS D ERREUR ICI 
        for i in range(6):
            copie = copy.deepcopy(jeu)
            copie.joue(i)
            nouveau_res = minMax(copie, profondeur-1, alpha, beta, True)[1]
            if nouveau_res < resultat:
                resultat = nouveau_res
                meilleur_coup = i 
            del(copie)
            if alpha >= resultat:
                return meilleur_coup,resultat
            beta = min(beta, resultat)

    return meilleur_coup,resultat
