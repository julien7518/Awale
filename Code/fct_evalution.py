from awale import Awale

def evaluation(jeu: Awale, joueur_actuel: int) -> int:
    """Meilleure fonction d'évaluation

    Prends en compte simplement la différence des scores

    :param jeu: Partie d'awale à analyser
    :type jeu: Awale
    :param joueur_actuel: Joueur dont c'est le tour
    :type joueur_actuel: int
    :return: Score du plateau actuel
    :rtype: int
    """
    return jeu.score[joueur_actuel] - jeu.score[1-joueur_actuel]

def rangee(jeu: Awale, joueur_actuel: int) -> int:
    """Fonction d'évaluation sur la position

    Prends en compte la somme des graines que l'on a dans son camps
    
    :param jeu: Partie d'awale à analyser
    :type jeu: Awale
    :param joueur_actuel: Joueur dont c'est le tour
    :type joueur_actuel: int
    :return: Score du plateau actuel
    :rtype: int
    """
    position = [0, 0]
    for nbr in jeu.plateau[:6]:
        position[0] += nbr
    for nbr in jeu.plateau[6:]:
        position[1] += nbr

    return 2 * evaluation(jeu, joueur_actuel) + (position[joueur_actuel] - position[1 - joueur_actuel])

def rangeeInverse(jeu: Awale, joueur_actuel: int) -> int:
    """Fonction d'évaluation sur la position n°2

    Prends en compte la somme des graines qu'il y a dans le camps adverse
    
    :param jeu: Partie d'awale à analyser
    :type jeu: Awale
    :param joueur_actuel: Joueur dont c'est le tour
    :type joueur_actuel: int
    :return: Score du plateau actuel
    :rtype: int
    """
    position = [0, 0]
    for nbr in jeu.plateau[:6]:
        position[0] += nbr
    for nbr in jeu.plateau[6:]:
        position[1] += nbr

    return 2 * evaluation(jeu, joueur_actuel) + (position[1 - joueur_actuel] - position[joueur_actuel])

def nbrPrise(jeu: Awale, joueur_actuel: int) -> int:
    """Première fonction d'évaluation

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

    return 2 * evaluation(jeu, joueur_actuel) + (prises_pos[joueur_actuel] - prises_pos[1-joueur_actuel]) 

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
    graines_pos = [0,0]

    for i in range(4,8):
        if (jeu.plateau[i] == 1) or (jeu.plateau[i] == 2):
            graines_pos[1] += jeu.plateau[i] + 1
    for i in range(0,4):
        if (jeu.plateau[i] == 1) or (jeu.plateau[i] == 2):
            graines_pos[0] += jeu.plateau[i] + 1

    return 2 * evaluation(jeu, joueur_actuel) + (graines_pos[joueur_actuel] - graines_pos[1-joueur_actuel])