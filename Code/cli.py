from awale import Awale
from exception import CoupImpossible
import typer

cli = typer.Typer()

@cli.command("joue")
def joue():
    jeu = Awale()
    while not jeu.fin:
        jeu.affichePlateau()
        case = int(input("Entrez le trou choisie : "))
        try:
            jeu.joue(case-1)
        except CoupImpossible:
            print("Tu t'es trompé de trou chef ! Fais attention la prochaine fois")
        jeu.actualiseEtat()

joue()