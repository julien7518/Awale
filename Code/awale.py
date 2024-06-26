from typing import Optional
from exception import CoupImpossible

class Awale(object):
    def __init__(self) -> None:
        self.plateau: list[int] = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        self.score: list[int] = [0, 0]
        self.joueur: int = 0
        self.fin: bool = False
        self.tours: int = 0


    def actualiseEtat(self, printIt: Optional[bool] = True) -> None:
        """Actualiser la fin de jeu.

        Permet d'analyser le plateau et de déterminer si le la partie est finie.

        :param printIt: Permet de choisir si l'on doit afficher le résultat ou non
        :type printIt: Optional[bool]
        """
        if self.coupsPossibles() == []:
            self.score[0] += sum(self.plateau[:6])
            self.score[1] += sum(self.plateau[6:])
            self.fin = True
        elif sum(self.plateau) <= 5:
            self.score[0] += sum(self.plateau[:6])
            self.score[1] += sum(self.plateau[6:])
            self.fin = True
        elif self.score[0] >= 25 or self.score[1] >= 25:
            self.fin = True
        if (self.fin == True) and printIt:
            print("Gagnant:","Joueur 1" if self.score[0] > self.score[1] else "Joueur 2",
                  "Score:",self.score[0],"-",self.score[1],
                  "Tours:",self.tours)
            

    def coupsPossibles(self) -> list[int]:
        """Calculer les coups acceptables.

        :return: Liste des indices jouables
        :rtype: list[int]
        """
        liste_coups = []
        famine_adversaire = True

        if self.joueur == 0:
            cases_adversaire = self.plateau[6:]
            debut, fin = 0, 6
        else:
            cases_adversaire = self.plateau[:6]
            debut, fin = 6, 12
        for cases in cases_adversaire:
            if cases != 0:
                famine_adversaire = False

        for i in range(debut, fin):
            if famine_adversaire and self.plateau[i] > fin-1-i and self.plateau[i] != 0:
                liste_coups.append(i)
            elif self.plateau[i] != 0:
                liste_coups.append(i)
        return liste_coups

    def joue(self, depart: int) -> None:
        """Jouer un coup.

        Permet de jouer un coup, en prenant `depart` comme trou à vider et répartissant les graines sur les trous suivants.

        :param depart: Case jouée par le joueur
        :type depart: int 
        """
        if depart in self.coupsPossibles():
            graines_restantes = self.plateau[depart]
            position = (depart + 1) % 12
            future_famine = True

            # On seme les graines
            while graines_restantes != 0:
                if position != depart:
                    self.plateau[position] += 1
                    graines_restantes = graines_restantes - 1
                position = (position + 1) % 12
            self.plateau[depart] = 0

            if self.joueur == 0:
                indice_cases_adversaire = [i for i in range(6, 13)]
                derniere_case_adv = 6
            else:
                indice_cases_adversaire = [i for i in range(0, 7)]
                derniere_case_adv = 0

            # Pas le droit d'affamer l'adversaire avec des prises
            for i in range(position-1, derniere_case_adv, -1):
                if self.plateau[i] != 2 or self.plateau[i] != 3:
                    future_famine = False

            # Pour partir du trou dans laquelle la derniere graine a été posée
            position = (position-1) % 12

            while (future_famine) and (position in indice_cases_adversaire) and (self.plateau[position] == 2 or self.plateau[position] == 3):
                self.score[self.joueur] += self.plateau[position]
                self.plateau[position] = 0
                position = (position - 1) % 12
            self.joueur = 1 - self.joueur
            self.tours = self.tours + 1
        
        else:
            raise CoupImpossible

    def affichePlateau(self) -> None:
        """Affiche le plateau dans un terminal"""
        print(" "*5 + str(self.score[1]) + " "*5)
        for i in range(11, 5, -1):
            print(self.plateau[i], end=" ")
        print()
        for i in range(0, 6):
            print(self.plateau[i], end=" ")
        print()
        print(" "*5 + str(self.score[0]) + " "*5)

    def __str__(self):
        return "Utilisez la méthode affichePlateau() pour afficher le jeu"

    def __repr__(self):
        return "Utilisez la méthode affichePlateau() pour afficher le jeu"
