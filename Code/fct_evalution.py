from awale import Awale

def evaluation(jeu: Awale, joueur_actuel : int) -> int:
    """Première fonction d'évaluation.
    
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