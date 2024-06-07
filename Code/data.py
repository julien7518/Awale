from awale import Awale
from typing import Callable
import minmax, fct_evalution
import random, sys, json, time, datetime
import montecarlo

def partieRM(p: int, eval: Callable[[Awale, int], int], optiAB: bool) -> list[int]:
    """Simule une partie entre un joueur aléatoire et MinMax
    
    :param p: Profondeur de la recherche dans un arbre MinMax
    :type p: int
    :param eval: Fonction d'évaluation à utiliser
    :type eval: Callable[[Awale,int],int]
    :param optiAB: Utiliser Alpha-Bêta
    :type optiAB: bool
    :return: Liste de la forme `[gagnant (0 si MinMax 1 sinon), score de MinMax, score de Random, tours joués]`
    :rtype: list[int]
    """
    jeu = Awale()
    while not jeu.fin:
        if jeu.joueur == 0:
            meilleur_coup, _ = minmax.minMax(jeu, profondeur=p, alpha=-sys.maxsize, beta=sys.maxsize, joueuramaximiser=True, eval=eval, optiAB=optiAB)
            jeu.joue(meilleur_coup)
        else:
            jeu.joue(random.choice(jeu.coupsPossibles()))
        
        jeu.actualiseEtat(printIt=False)
    
    if jeu.score[0] > jeu.score[1]:
        return [0, jeu.score[0], jeu.score[1], jeu.tours]
    elif jeu.score[0] < jeu.score[1]:
        return [1, jeu.score[0], jeu.score[1], jeu.tours]

def simulationRM(k: int, p: int, eval: Callable[[Awale, int], int], optiAB: bool) -> list[int]:
    """Calcule les simulations de jeu
    
    :param k: Nombre de simulation à faire
    :type k: int
    :param p: Profondeur de la recherche dans un arbre MinMax
    :type p: int
    :param optiAB: Utiliser Alpha-Bêta
    :type optiAB: bool
    :param eval: Fonction d'évaluation à utiliser
    :type eval: Callable[[Awale,int],int]
    """
    debut = time.time()
    res = [0, 0, 0, 0, 0, 0, 0] # [victoire 1, victoire 2, score moyen 1, score moyen 2, tours moyen, tours moyen victoire, tours moyen defaites, temps d'exécution (append après)]

    for i in range(k):
        partie = partieRM(p, eval, optiAB)

        if partie is not None:
            res[partie[0]] += 1
            res[2] += partie[1]
            res[3] += partie[2]
            res[4] += partie[3]
            res[5 + partie[0]] += partie[3]

    for i in range(2, 5):
        res[i] = res[i] / k

    res[5] = res[5] / (res[0] if res[0] != 0 else 1)
    res[6] = res[6] / (res[1] if res[1] != 0 else 1)

    total = time.time() - debut
    res.append(total)

    return res

def extractMinmaxRandom(nbr_sim: int, profondeur: int, fct_eval: Callable[[Awale, int], int], optiAB: bool = True) -> None:
    """Permet d'extraire des données

    Extrait les données au format JSON (`..data/resultat.json`), de simulation de parties entre un joueur aléatoire et l'IA MinMax

    :param nbr_sim: Nombre de simulation effectué
    :type nbr_sim: int
    :param profondeur: Profondeur de la recherche dans le MinMax
    :type profondeur: int
    :param fct_eval: Fonction d'évaluation utiliser dans MinMax
    :type fct_eval: Callable[[Awale,int],int]
    :param optiAB: Permet d'activer ou non l'optimisation alpha-bêta
    :type optiAB: bool
    """
    if optiAB:
        opti = "elagage alpha-beta"
    else:
        opti = "aucune"

    res = simulationRM(nbr_sim, profondeur, fct_eval, optiAB)

    chemin_fichier = '../data/resultat.json'

    try:
        with open(chemin_fichier, 'r') as fichier:
            data = json.load(fichier)
    except FileNotFoundError:
        data = []

    dico = {
        "simID": len(data)+1,
        "date": datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
        "ia": "MinMax",
        "optimisation": opti,
        "fonction": fct_eval.__qualname__,
        "profondeur": profondeur,
        "nbrSimulation": nbr_sim,
        "temps_sec": res[7],
        "temps_format": str(datetime.timedelta(seconds=res[7])),
        "resultat": {
            "minmaxVictoire": res[0],
            "randomVictoire": res[1],
            "reussite" : (res[0] / nbr_sim) * 100,
            "minmaxScore": res[2],
            "randomScore": res[3],
            "tours": res[4],
            "toursMinmax":res[5],
            "toursRandom":res[6]
        }
    }

    data.append(dico)

    with open(chemin_fichier, 'w') as fichier:
        json.dump(data, fichier, indent=4)
    

def partieMC(repetition: int) -> list[int]:
    """Simule une partie entre un joueur aléatoire et Monte Carlo
    
    :param repetition: Nombre de répétitions de Monte Carlo
    :type repetition: int
    :return: Liste de la forme `[gagnant (0 si Monte Carlo 1 sinon), score de Monte Carlo, score de Random, tours joués]`
    :rtype: list[int]
    """
    jeu = Awale()
    while not jeu.fin:
        if jeu.joueur == 0:
            coup = montecarlo.monteCarlo(jeu, repetition=repetition)
            jeu.joue(coup)
        else:
            jeu.joue(random.choice(jeu.coupsPossibles()))
        
        jeu.actualiseEtat(printIt=False)
    
    if jeu.score[0] > jeu.score[1]:
        return [0, jeu.score[0], jeu.score[1], jeu.tours]
    else:
        return [1, jeu.score[0], jeu.score[1], jeu.tours]

def simulationMC(k: int, repetition: int) -> list[int]:
    """Calcule les simulations de jeu
    
    :param k: Nombre de simulation à faire
    :type k: int
    :param repetition: Nombre de répétitions de Monte Carlo
    :type repetition: int
    :return: Liste des résultats des simulations
    :rtype: list[int]
    """
    debut = time.time()
    res = [0, 0, 0, 0, 0, 0, 0] # [victoire 1, victoire 2, score moyen 1, score moyen 2, tours moyen, tours moyen victoire, tours moyen defaites, temps d'exécution (append après)]

    for i in range(k):
        partie = partieMC(repetition)

        if partie is not None:
            res[partie[0]] += 1
            res[2] += partie[1]
            res[3] += partie[2]
            res[4] += partie[3]
            res[5 + partie[0]] += partie[3]

    for i in range(2, 5):
        res[i] = res[i] / k

    res[5] = res[5] / (res[0] if res[0] != 0 else 1)
    res[6] = res[6] / (res[1] if res[1] != 0 else 1)

    total = time.time() - debut
    res.append(total)

    return res

def extractMonteCarloRandom(nbr_sim: int, repetition: int) -> None:
    """Permet d'extraire des données

    Extrait les données au format JSON (`..data/resultat_montecarlo.json`), de simulation de parties entre un joueur aléatoire et l'IA Monte Carlo

    :param nbr_sim: Nombre de simulation effectué
    :type nbr_sim: int
    :param repetition: Nombre de répétitions de Monte Carlo
    :type repetition: int
    """
    res = simulationMC(nbr_sim, repetition)

    chemin_fichier = '../data/resultat_montecarlo.json'

    try:
        with open(chemin_fichier, 'r') as fichier:
            data = json.load(fichier)
    except FileNotFoundError:
        data = []

    dico = {
        "simID": len(data) + 1,
        "date": datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
        "ia": "Monte Carlo",
        "repetition": repetition,
        "nbrSimulation": nbr_sim,
        "temps_sec": res[7],
        "temps_format": str(datetime.timedelta(seconds=res[7])),
        "resultat": {
            "montecarloVictoire": res[0],
            "randomVictoire": res[1],
            "reussite": (res[0] / nbr_sim) * 100,
            "montecarloScore": res[2],
            "randomScore": res[3],
            "tours": res[4],
            "toursMonteCarlo": res[5],
            "toursRandom": res[6]
        }
    }

    data.append(dico)

    with open(chemin_fichier, 'w') as fichier:
        json.dump(data, fichier, indent=4)


for i in range(1,10):
    extractMonteCarloRandom(1000,i)
