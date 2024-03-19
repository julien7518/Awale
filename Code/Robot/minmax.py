from ..Jeu.awale import Awale
import sys, copy
from typing import Callable

def minMax(jeu: Awale, profondeur: int, evaluation: Callable[[list[int]], int]) -> int:
    """Calculer une position.

    Permet de calculer un plateau en se basant sur un algorithme MinMax qui évalue l'arbre des possibilités.

    :param jeu: Partie d'awale à analyser
    :type jeu: Awale
    :param profondeur: Profondeur maximale à laquelle chercher
    :type profondeur: int
    :param evaluation: Fonction d'évaluation d'une position
    :type evaluation: Callable[[list[int]], int]
    :return: Valeur d'évaluation du noeud
    :rtype: int
    """
    if (profondeur == 0) or jeu.fin:
        return evaluation(jeu.plateau)
    if jeu.joueur:
        resultat = - sys.maxsize
        for i in range(6, 12):
            copie = copy.deepcopy(jeu)
            copie.joue(i)
            resultat = max(resultat, minMax(copie, profondeur-1, evaluation))
            del(copie)
    else:
        resultat = sys.maxsize
        for i in range(6):
            copie = copy.deepcopy(jeu)
            copie.joue(i)
            resultat = min(resultat, minMax(copie, profondeur-1, evaluation))
            del(copie)
    return resultat