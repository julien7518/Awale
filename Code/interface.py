from awale import Awale
from typing import Optional
from exception import CoupImpossible
import sys
import minmax
import fct_evalution
import random 
import typer

cli = typer.Typer(no_args_is_help=True, add_completion=False, context_settings={"help_option_names": ["--help", "-h"]})

def _version_callback(value: bool) -> None:
    """Renvoie la version du projet.

    :raises typer.Exit: Quitte l'application.
    """
    if value:
        typer.echo("1.0.0")
        raise typer.Exit()


def _credits_callback(value: bool) -> None:
    """Affiche les crédits du projet.

    :raises typer.Exit: Quitte l'application.
    """
    if value:
        typer.echo("Sarusan Nithiyarajan - Julien Fernandes\nAwale 2024-2025 ©️")
        raise typer.Exit()


@cli.callback()
def main(version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Voir la version et quitter.",
        callback=_version_callback,
        is_eager=True),
        credits: Optional[bool] = typer.Option(
        None,
        "--credits",
        "-c",
        help="Voir les crédits et quitter.",
        callback=_credits_callback,
        is_eager=True)
    ) -> None:
    pass


@cli.command("GUI")
def joueGui() -> None:
    """Jouer avec une interface.

    Permet de jouer à l'awale dans une fenêtre externe avec interface graphique.
    """
    print("In progress...")


@cli.command("shell")
def joueShell(type: str) -> None:
    """Jouer dans le terminal.

    Permet de jouer à l'awale dans le terminal, avec une interface simple.

    :raises typer.Exit: Quitte l'application.
    """
    jeu = Awale()
    while not jeu.fin:
        if jeu.joueur == 0 or type is None:
            jeu.affichePlateau()
            try:
                case = input("Entrez le trou choisi : ") 
                if case == ".quit":
                    raise typer.Exit()
                else:
                    case = int(case)
                try:
                    jeu.joue(case-1)
                except CoupImpossible:
                    print("Tu t'es trompé de trou chef ! Fais attention la prochaine fois")
            except ValueError:
                print("Veuillez saisir un nombre entre 1 et 12")
        else:
            print("Tour de l'IA...")
            if type == "minmax":
                meilleur_coup, _ = minmax.minMax(jeu, profondeur=4, alpha=-sys.maxsize, beta=sys.maxsize, joueuramaximiser=True, eval=fct_evaluation.evaluation)
            elif type == "mcts":
                meilleur_coup = random.choice(jeu.coupsPossibles())
            elif type == "random":
                meilleur_coup = random.choice(jeu.coupsPossibles())

            jeu.joue(meilleur_coup)
            print(f"L'IA a joué dans le trou {meilleur_coup + 1}") 

        jeu.actualiseEtat()


@cli.command("shell_Humain")
def joueShell_h() -> None:
    """Jouer dans le terminal.

    Permet de jouer à l'awale dans le terminal, avec une interface simple.

    :raises typer.Exit: Quitte l'application.
    """
    jeu = Awale()
    while not jeu.fin:
        jeu.affichePlateau()
        try:
            case = input("Entrez le trou choisi : ") 
            if case == ".quit":
                raise typer.Exit()
            else:
                case = int(case)
            try:
                jeu.joue(case-1)
            except CoupImpossible:
                print("Tu t'es trompé de trou chef ! Fais attention la prochaine fois")
        except ValueError:
            print("Veuillez saisir un nombre entre 1 et 12")

    jeu.actualiseEtat()

@cli.command("shell_IAvsIA") #Pas d'interet de se faire battre 2 min_max avec profondeur diff car c'est tjrs exactement le meme match mais utile pour voir quelle est la meilleure fonction d evaluation
def joueShell_i() -> None:
    """Jouer dans le terminal.

    Permet de jouer à l'awale dans le terminal, avec une interface simple.

    :raises typer.Exit: Quitte l'application.
    """
    jeu = Awale()
    while not jeu.fin:
        if jeu.joueur == 0:
            print("Tour de l'IA 1...")
            meilleur_coup, _ = minmax.minMax(jeu, profondeur=4, alpha=-sys.maxsize, beta=sys.maxsize, joueuramaximiser=True, eval=fct_evaluation.evaluation)
            jeu.joue(meilleur_coup)
            print(f"L'IA a joué dans le trou {meilleur_coup + 1}") 
        else: 
            print("Tour de l'IA 2...")
            meilleur_coup, _ = minmax.minMax(jeu, profondeur=3, alpha=-sys.maxsize, beta=sys.maxsize, joueuramaximiser=True, eval=fct_evaluation.evaluation)
            jeu.joue(meilleur_coup)
            print(f"L'IA a joué dans le trou {meilleur_coup + 1}") 


        jeu.actualiseEtat()
        jeu.affichePlateau()

@cli.command("shell_IAvsRandom")
def joueShell_r() -> None:
    """Jouer dans le terminal.

    Permet de jouer à l'awale dans le terminal, avec une interface simple.

    :raises typer.Exit: Quitte l'application.
    """
    jeu = Awale()
    while not jeu.fin:
        if jeu.joueur == 0:
            meilleur_coup, _ = minmax.minMax(jeu, profondeur=4, alpha=-sys.maxsize, beta=sys.maxsize, joueuramaximiser=True, eval=fct_evaluation.evaluation)
            jeu.joue(meilleur_coup)
        else:
            jeu.joue(random.choice(jeu.coupsPossibles()))
        
        jeu.actualiseEtat()



if __name__ == "__main__":
    cli()
