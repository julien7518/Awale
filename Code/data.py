from awale import Awale
import random
import minmax
import fct_evalution
import sys

def partieRM() -> list[int]:
    jeu = Awale()
    while not jeu.fin:
        if jeu.joueur == 0:
            meilleur_coup, _ = minmax.minMax(jeu, profondeur=4, alpha=-sys.maxsize, beta=sys.maxsize, joueuramaximiser=True, eval=fct_evalution.evaluation)
            jeu.joue(meilleur_coup)
        else:
            jeu.joue(random.choice(jeu.coupsPossibles()))
        
        jeu.actualiseEtat()
    
    if jeu.score[0] > jeu.score[1]:
        return [0, jeu.score[0], jeu.score[1], jeu.tour]
    elif jeu.score[0] < jeu.score[1]:
        return [1, jeu.score[0], jeu.score[1], jeu.tour]

def simulationRM(k: int, p: int) -> list[int]:
    """
    
    :param k: Nombre de simulation à faire
    :type k: int
    :param p: Profondeur de la recherche dans un arbre MinMax
    :type p: int
    """
    res = [0, 0, 0, 0, 0] # [victoire 1, victoire 2, score moyen 1, score moyen 2, tours moyen]

    for i in range(k):
        partie = partieRM()
        res[partie[0]] += 1
        res[2] += partie[1]
        res[3] += partie[2]
        res[4] += partie[3]
    
    for i in range(2, 5):
        res[i] = res[i] / k
    
    return res
