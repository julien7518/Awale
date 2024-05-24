from awale import Awale
import sys, copy
from typing import Tuple, Optional
import random 


#Noeud : [partie, scores, simulations victorieuses, simulations totales, personne devant jouer,
# partieFinie ? (2 pour joueurArbre a gagné, 1 s'il a perdu, 0 si la partie n'est pas finie), dernier trou joué]

#  {"partie": jeu, "simTot": 1, "simVic": 0}
#  dict[Awale, int, int]

global probaExplo
probaExplo = 0.5


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

    def ajouteNoeud(self, donnees: dict) -> None:
        """Ajoute un fils au noeud

        :param donnees: Dictionnaire contenant les données du neoud
        :type donnees: dict
        """
        self.fils.append(Arbre(donnees=donnees, parent=self))


def meilleurFils(a : Noeud) -> Noeud | None:
    """Renvoie le fils ayant le meilleur ratio de victoire par rapport au nombre de simulation

    :param a: Le noeud dans lequel on doit choisir le fils
    :type a: Noeud
    :return: Renvoie le fils s'il existe
    :rtype: Noeud|None
    """
    meilleurRatio = -1.0
    meilleurChoix = None
    for noeud in a.fils:
        if (noeud.donnees["simTot"] != 0):
            ratio = noeud.donnees["simVic"]/noeud.donnees["simTot"]
            if (ratio >= meilleurRatio):
                meilleurRatio = ratio
                meilleurChoix = noeud
    
    return meilleurChoix

def selection(a: Noeud):
    """Phase de sélection dans l'algorithme de Monte-Carlo

    :param a: L'arbre sur lequel on recherche
    :type a: Noeud
    """
    resultat = a
    noeud = a
    # Tant qu'il y a des fils on continue
    while(a.fils != []):
        valeur_aleatoire = random.random()
        mFils = meilleurFils(a)
        joueur = a.donnees["partie"].joueur
        # On choisit d'expandre un fils ou de regarder un autre fils
        if (valeur_aleatoire <= probaExplo): # !Faire attention problème avec le joueur 
            resultat = mFils
        else:
            # Choisir uniformément pour prendre un autre fils ou en créer un
            valeur_aleatoire = random.random()
            if (valeur_aleatoire <= 1/len(a.fils)):
                # On créer un nouveau fils seulement s'il exsite (partie qui donne un nouvelle état de plateau)
                if (len(noeud.donnees["partie"].coupsPossibles) == len(a.fils)):
                    # Ce n'est pas possible
                    resultat = random.choice(a.fils)
                else:
                    # C'est possible
                    for coup in noeud.donnees["partie"].coupsPossibles:
                        copie = copy.deepcopy(noeud.donnees["partie"])
                        copie.joue(coup)
                        for enfant in a.fils:


def expansion(a: Noeud) -> int:
    """Permet de créer un nouveau fils si c'est possible

    :param a: Noeud auquel on rajoute un fils
    :type a: Noeud
    :return: Le dernier coup qui a été joué, -1 si aucun coup n'a été joué
    :rtype: int 
    """
    if (a.donnees["partie"].fin):
        return -1
    else:
        copie = copy.deepcopy(a.donnees["partie"])
        coup = random.choice(copie.coupsPossibles)
        copie.joue(coup)
        data = {"partie": copie, "simTot": 0, "simVic": 0}
        a.ajouteNoeud(data)
        return coup


def simulation(a: Noeud) -> int:
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
        return 0
    else:
        return 1


def retropopagation(a: Noeud, victoire: bool) -> None:
    """Propage la valeur de la simulation aux parents du noeud

    :param a: Noeud duquel on part pour propager
    :type a: Noeud
    :param victoire: Indique s'il y a eu une victoire au bout de la simulation
    :type victoire: bool
    """
    if victoire:
        vic = 1
    else:
        vic = 0
    while a.pere is not None:
        a.donnees["simTot"] += 1
        a.donnees["simVic"] += vic
        a = a.pere