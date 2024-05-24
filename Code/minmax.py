from awale import Awale
import sys, copy
from typing import Tuple, Callable, Optional
import random

def minMax(jeu: Awale, profondeur: int, alpha: int, beta: int, joueuramaximiser: bool, eval: Callable[[Awale, int], int]) -> Tuple[Optional[int], int]:
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
    :rtype: tuple[Optional[int],int]
    """
    if (profondeur == 0) or jeu.fin:
        return None, eval(jeu,joueuramaximiser)
    # Maximisateur
    if joueuramaximiser:
        resultat = - sys.maxsize
        liste_coup_pos = jeu.coupsPossibles()
        if liste_coup_pos == []:
            return None, eval(jeu,joueuramaximiser)
        meilleur_coup = random.choice(liste_coup_pos) 
        for i in liste_coup_pos:
            copie = copy.deepcopy(jeu)
            copie.joue(i)
            nouveau_res = minMax(copie, profondeur-1, alpha, beta, False, eval)[1]
            if nouveau_res > resultat:
                resultat = nouveau_res
                meilleur_coup = i
            del(copie)
            if beta <= resultat:
                return meilleur_coup, resultat
            alpha = max(alpha, resultat)
    
    # Minimisateur
    else:
        resultat = sys.maxsize
        liste_coup_pos = jeu.coupsPossibles()
        if liste_coup_pos == []:
            return None, eval(jeu,joueuramaximiser)
        meilleur_coup = random.choice(liste_coup_pos) 
        for i in liste_coup_pos:
            copie = copy.deepcopy(jeu)
            copie.joue(i)
            nouveau_res = minMax(copie, profondeur-1, alpha, beta, True, eval)[1]
            if nouveau_res < resultat:
                resultat = nouveau_res
                meilleur_coup = i
            del(copie)
            if alpha >= resultat:
                return meilleur_coup, resultat
            beta = min(beta, resultat)

    return meilleur_coup, resultat
