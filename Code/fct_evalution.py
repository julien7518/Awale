from awale import Awale

def evaluation(jeu: Awale, joueur_actuel : int) -> int:
    """Première fonction d'évaluation.

    Prends en compte le score ainsi que le nombre de prises possibles à un instant
    
    :param jeu: Partie d'awale à analyser
    :type jeu: Awale
    :param joueur_actuel: Joueur dont c'est le tour
    :type joueur_actuel: int
    :return: Score du plateau actuel
    :rtype: int
    """
    prises_pos = [0,0]

    for i in range(4,8):
        if (jeu.plateau[i] == 1) or (jeu.plateau[i] == 2):
            prises_pos[1] += 1 
    for i in range(0,4):
        if (jeu.plateau[i] == 1) or (jeu.plateau[i] == 2):
            prises_pos[0] += 1 

    total = 2*(jeu.score[joueur_actuel]) + prises_pos[joueur_actuel] - 2*(jeu.score[1-joueur_actuel]) + prises_pos[1-joueur_actuel] 

    return total

def nbrGraine(jeu: Awale, joueur_actuel: int) -> int:
    """Deuxième fonction d'évaluation.
    
    Variante de la fonction `evaluation` en prenant ici le nombre de graines prises

    :param jeu: Partie d'awale à analyser
    :type jeu: Awale
    :param joueur_actuel: Joueur dont c'est le tour
    :type joueur_actuel: int
    :return: Score du plateau actuel
    :rtype: int
    """
    prises_pos = [0,0]

    for i in range(4,8):
        if (jeu.plateau[i] == 1) or (jeu.plateau[i] == 2):
            prises_pos[1] += jeu.plateau[i] + 1
    for i in range(0,4):
        if (jeu.plateau[i] == 1) or (jeu.plateau[i] == 2):
            prises_pos[0] += jeu.plateau[i] + 1

    total = 2*(jeu.score[joueur_actuel]) + prises_pos[joueur_actuel] - 2*(jeu.score[1-joueur_actuel]) + prises_pos[1-joueur_actuel] 

    return total