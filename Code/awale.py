from exception import CoupImpossible


class Awale(object):
    def __init__(self) -> None:
        self.plateau = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        self.score = [0, 0]
        self.joueur = 0
        self.fin = False

    def actualiseEtat(self) -> None:
        """_summary_

        _extended_summary_
        """
        if self.coupsPossibles() == []:
            self.fin = True
        elif sum(self.plateau) < 3:
            self.score[0] += sum(self.plateau[:6])
            self.score[1] += sum(self.plateau[6:])
            self.fin = True

    def coupsPossibles(self) -> list:
        """_summary_

        _extended_summary_

        :return: Renvoie la liste des indices jouables
        :rtype: list
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
        """_summary_

        _extended_summary_

        :param depart: Case jouee par le joueur
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
            for i in range(position, derniere_case_adv, -1):
                if self.plateau[i] != 2 or self.plateau[i] != 3:
                    future_famine = False

            # Pour partir du trou dans laquelle la derniere graine a été posée
            position = (position-1) % 12

            while not (future_famine) and (position in indice_cases_adversaire) and (self.plateau[position] == 2 or self.plateau[position] == 3):
                self.score[self.joueur] += self.plateau[position]
                self.plateau[position] = 0
                position = (position - 1) % 12
            self.joueur = 1 - self.joueur

        else:
            raise CoupImpossible

    def affichePlateau(self) -> None:
        print(" "*5 + str(self.score[1]) + " "*5)
        for i in range(11, 5, -1):
            print(self.plateau[i], end=" ")
        print()
        for i in range(0, 6):
            print(self.plateau[i], end=" ")
        print()
        print(" "*5 + str(self.score[0]) + " "*5)
