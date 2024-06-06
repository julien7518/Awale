from awale import Awale
import sys, copy
from typing import Tuple, Optional
import random, math


# Structure des données stockées dans chaque Noeud
#  {"partie": jeu, "simTot": 1, "simVic": 0, "dernierCoup"} : dict[Awale, int, int, int]

global p_exploration
p_exploration = math.sqrt(2) # Valeur théorique (meilleur résultat avec une valeur expérimentale)

class Noeud(object):
    """Classe d'un arbre

    :param donnees: Dictionnaire contenant les données du neoud
    :type donnees: dict
    :param parent: Père du noeud actuel
    :type parent: Noeud
    """
    def __init__(self, donnees: dict, parent: Optional = None) -> None:
        self.fils: list = []
        self.pere = parent
        self.donnees: dict = donnees

    def ajouteNoeud(self, donnees: dict):
        """Ajoute un fils au noeud

        :param donnees: Dictionnaire contenant les données du neoud
        :type donnees: dict
        """
        enfant = Arbre(donnees=donnees, parent=self)
        self.fils.append(enfant)
        return enfant


def UCT(a: Noeud, fils: Noeud) -> int:
    """Calcul le score basé sur la formule UCT

    :param a: Père du noeud
    :type a: Noeud
    :param fils: Fils duquel on veit calculer le score
    :type fils: Noeud
    :return: Score UCT basé sur UCB1
    :rtype: int
    """
    return (fils.donnees["simVic"] / fils.donnees["simTot"]) + (p_exploration * math.sqrt(math.log2(a.donnees["simTot"]) / fils.donnees["simTot"]))

def selection(a: Noeud) -> Tuple[Noeud, int]:
    """Phase de sélection dans l'algorithme de Monte-Carlo

    :param a: L'arbre sur lequel on recherche
    :type a: Noeud
    :param f: Fonction à utiliser pour choisir le fils
    :type f: Callable[[Noeud,Noeud],int]
    :return: Le noeud choisit avec son score correspondant (ou -1 si racine choisit et donc pas de score)
    :rtype: Tuple[Noeud,int]
    """
    choix = a
    score = -1.0
    while choix.fils != []:
        for fils in a.fils:
            scoreFils = UCT(a, fils)
            if scoreFils > score:
                score = scoreFils
                choix = fils
    return choix, score

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
        coup = random.choice(copie.coupsPossibles)
        copie.joue(coup)
        data = {"partie": copie, "simTot": 0, "simVic": 0}
        a.ajouteNoeud(data)


def simulationRandom(a: Noeud) -> int:
    """Simule une partie aléatoire

    :param a: Noeud à partir du quel on doit simuler
    :type a: Noeud
    :return: 1 si l'ordinateur gagne à la fin de la simulation, ou 0 sinon
    :rtype: int
    """
    copie = copy.deepcopy(a.donnees["partie"])
    while not copie.fin:
        coup = random.choice(copie.coupsPossibles)
        copie.joue(coup)
    
    if copie.score[0] > copie.score[1]:
        return a, 1
    else:
        return a, 0


def retropopagation(a: Noeud, victoire: int) -> None:
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

def meilleurFils(a: Noeud) -> int:
    choix = -1
    score = -1
    for fils in a.fils:
        scoreFils = fils.donnees["simVic"] / fils.donnees["simTot"]
        if scoreFils > score:
            choix = "meilleur coup"
            score = scoreFils
    return choix, score

def monteCarlo(jeu: Awale, repetition: int, uct: Optional[bool] = True) -> int:
    arbre = Noeud({"partie": jeu, "simTot": 0, "simVic": 0})
    for i in range(0, repetition):
        if uct:
            positionArbre = selectoin(arbre)
        else:
            positionArbre = epsilonSelection(arbre)

        noeud, victoire = simualation(expansion(positionArbre))
        retropropagation(noeud, victoire)

    return meilleurFils(arbre)[0]