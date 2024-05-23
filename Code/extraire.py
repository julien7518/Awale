import subprocess
import json 
import re 

def lancer_simulation():
    """Lance une partie entre deux algorithmes 

    """
    retour = subprocess.run(['python','interface.py','shell_IAvsRandom'], capture_output = True, text = True)
    #subprocess permet d'exécuter la commande shell_IAvsIA dans le script python
    #capture_output = True on recupere le sortie standard
    #text retourne la sortie sous la forme de chaine de caracteres
    return retour.stdout

def matching_info(sortie : str):
    """Permet d'obtenir les informations de renvoi sur le gagnant, le score et le nombre de tours

    """
    trouver_gagnant = re.search(r'Gagnant: (.+) Score:',sortie)
    trouver_score = re.search(r'Score: (\d+ - \d+) Tours:',sortie)
    trouver_tours = re.search(r'Tours: (\d+)',sortie)
    # trouver_ permet d'obtenir soit la chaine de caracteres voulu soit None
    gagnant = trouver_gagnant.group(1) if trouver_gagnant else "Nul ou Erreur"
    score = trouver_score.group(1) if trouver_score else "0 - 0 ou Erreur"
    tours = trouver_tours.group(1) if trouver_tours else 0 

    # Renvoyer les informations en dictionnaire
    return {
        'gagnant':gagnant,
        'score':score,
        'tours':tours
    }

def simulation_jeu(nombre_de_partie : int) -> list:
    resultats = []
    for i in range(nombre_de_partie):
        sortie = lancer_simulation()
        resultat = matching_info(sortie)
        resultats.append(resultat)
    return resultats

def sauvegarder_resultats(resultats, nom_fichier):
    with open(nom_fichier,'w') as f:
        json.dump(resultats,f,indent=4)

if __name__ == "__main__":
    # Si le script python est executé 
    nombre_parties = 10
    resultats = simulation_jeu(nombre_parties)
    sauvegarder_resultats(resultats,'resultats_test.json')