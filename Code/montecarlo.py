from awale import Awale
import sys, copy
from typing import Tuple, Optional
import random, math
import fct_evalution
import minmax


# Structure des données stockées dans chaque Noeud
#  {"partie": jeu, "simTot": 1, "simVic": 0} : dict[Awale, int, int]

global p_exploration
p_exploration = math.sqrt(2) # Valeur théorique (meilleur résultat avec une valeur expérimentale)

class Noeud(object):
    """Classe d'un arbre

    :param donnees: Dictionnaire contenant les données du neoud
    :type donnees: dict
    :param parent: Père du noeud actuel
    :type parent: Noeud
    """
    def __init__(self, donnees: dict, coup: Optional[int] = None, parent: Optional['Noeud'] = None) -> None:
        self.fils: list = []
        self.pere = parent
        self.donnees: dict = donnees
        self.coup: int = coup if coup != None and coup >= 0 else -1

    def ajouteNoeud(self, donnees: dict, coup: int):
        """Ajoute un fils au noeud

        :param donnees: Dictionnaire contenant les données du neoud
        :type donnees: dict
        """
        enfant = Noeud(donnees=donnees, coup=coup, parent=self)
        self.fils.append(enfant)
        return enfant

import math

def UCT(a: Noeud, fils: Noeud) -> float:
    """Calcul le score basé sur la formule UCT

    :param a: Père du noeud
    :type a: Noeud
    :param fils: Fils duquel on veit calculer le score
    :type fils: Noeud
    :return: Score UCT basé sur UCB1
    :rtype: float
    """
    exploitation = fils.donnees["simVic"] / fils.donnees["simTot"]
    exploration = p_exploration * math.sqrt(math.log2(a.donnees["simTot"]) / fils.donnees["simTot"])
    return exploitation + exploration


# def UCT(a: Noeud, fils: Noeud) -> int:
#     """Calcul le score basé sur la formule UCT

#     :param a: Père du noeud
#     :type a: Noeud
#     :param fils: Fils duquel on veit calculer le score
#     :type fils: Noeud
#     :return: Score UCT basé sur UCB1
#     :rtype: int
#     """
#     return (fils.donnees["simVic"] / fils.donnees["simTot"]) + (p_exploration * math.sqrt(math.log2(a.donnees["simTot"]) / fils.donnees["simTot"]))

def selection(a: Noeud) -> Tuple[Noeud, int]:
    """Phase de sélection dans l'algorithme de Monte-Carlo

    :param a: L'arbre sur lequel on recherche
    :type a: Noeud
    :return: Le noeud choisit avec son score correspondant (ou -1 si racine choisit et donc pas de score)
    :rtype: Tuple[Noeud,int]
    """
    choix = a
    score = -1.0
    while choix.fils:
        meilleur_score = -float('inf')
        best_fils = None
        for fils in choix.fils:
            scoreFils = UCT(choix, fils)
            if scoreFils > meilleur_score:
                meilleur_score = scoreFils
                meilleur_fils = fils
        choix = meilleur_fils
        score = meilleur_score
    return choix, score

# def selection(a: Noeud) -> Tuple[Noeud, int]:
#     """Phase de sélection dans l'algorithme de Monte-Carlo

#     :param a: L'arbre sur lequel on recherche
#     :type a: Noeud
#     :param f: Fonction à utiliser pour choisir le fils
#     :type f: Callable[[Noeud,Noeud],int]
#     :return: Le noeud choisit avec son score correspondant (ou -1 si racine choisit et donc pas de score)
#     :rtype: Tuple[Noeud,int]
#     """
#     choix = a
#     score = -1.0
#     while choix.fils != []:
#         for fils in a.fils:
#             scoreFils = UCT(a, fils)    
#             if scoreFils > score:
#                 score = scoreFils
#                 choix = fils    
#     return choix, score

def epsilonSelection(a: Noeud, epsilon: int) -> Tuple[Noeud, int]:
    choix = a
    score = -1.0
    while choix.fils != []:
        r = random.random()
        if r <= epsilon:
            choix = random.choice(a.coupsPossibles)
        else:
            for fils in a.fils:
                scoreFils = fils.donnees["simVic"] / fils.donnees["simTot"]
                if scoreFils > score:
                    score = scoreFils
                    choix = fils
    return choix, score

# A revoir
def expansion(a: Noeud) -> Noeud:
    """Permet de créer un nouveau fils si c'est possible

    :param a: Noeud auquel on rajoute un fils
    :type a: Noeud
    :return: Le fils ajouté
    :rtype: Noeud
    """
    if (a.donnees["partie"].fin):
        return a
    else:
        copie = copy.deepcopy(a.donnees["partie"])
        if copie.coupsPossibles() == []:
            copie.fin = True 
            return a 
        else:
            coup = random.choice(copie.coupsPossibles())
            copie.joue(coup)
            data = {"partie": copie, "simTot": 0, "simVic": 0}
            return a.ajouteNoeud(data, coup)


def simulationRandom(a: Noeud) -> int:
    """Simule une partie aléatoire

    :param a: Noeud à partir du quel on doit simuler
    :type a: Noeud
    :return: 1 si l'ordinateur gagne à la fin de la simulation, ou 0 sinon
    :rtype: int
    """    
    copie = copy.deepcopy(a.donnees["partie"])
    while not copie.fin:
        if copie.coupsPossibles() == []:
            copie.fin = True 
        else:
            copie.joue(random.choice(copie.coupsPossibles()))
            copie.actualiseEtat()
    
    if copie.score[0] > copie.score[1]:
        return a, 1
    else:
        return a, 0

def retropropagation(a: Noeud, victoire: int) -> None:
    """Propage la valeur de la simulation aux parents du noeud

    :param a: Noeud duquel on part pour propager
    :type a: Noeud
    :param victoire: Indique s'il y a eu une victoire au bout de la simulation
    :type victoire: int
    """
    while a.pere is not None:
        a.donnees["simTot"] += 1
        a.donnees["simVic"] += victoire
        a = a.pere
    a.donnees["simTot"] += 1
    a.donnees["simVic"] += victoire
    

def meilleurFils(a: Noeud) -> int:
    choix = a.coup
    score = -1
    for fils in a.fils:
        scoreFils = fils.donnees["simVic"] / fils.donnees["simTot"]
        if scoreFils > score:
            choix = fils.coup
            score = scoreFils
    return choix, score

def monteCarlo(jeu: Awale, repetition: int, uct: Optional[bool] = True) -> int:
    arbre = Noeud({"partie": jeu, "simTot": 0, "simVic": 0})
    for i in range(0, repetition):
        if uct:
            positionArbre = selection(arbre)[0]
        else:
            positionArbre = epsilonSelection(arbre)[0]
        noeud, victoire = simulationRandom(expansion(positionArbre))
        retropropagation(noeud, victoire)

    return meilleurFils(arbre)[0]

# def jouer_partie():
#     jeu = Awale()
#     while not jeu.fin:
#         if jeu.joueur == 0:  # Monte Carlo Player
#             coup = monteCarlo(jeu, repetition=3)
#             jeu.joue(coup)
#         else:  # Random Player
#             jeu.joue(random.choice(jeu.coupsPossibles()))
#         jeu.actualiseEtat()
#     return jeu.score

# def simulation_monteCarlo_vs_random(n: int):
#     monteCarlo_victoire = 0
#     random_victoire = 0
#     for i in range(n):
#         score = jouer_partie()
#         if score[0] > score[1]:
#             monteCarlo_victoire += 1
#         else:
#             random_victoire += 1
#     print(f"Victoire Monte Carlo: {monteCarlo_victoire}, Victoire Random: {random_victoire}")

# simulation_monteCarlo_vs_random(3)
