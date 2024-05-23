from awale import Awale
from typing import Optional
from exception import CoupImpossible
import sys
from minmax import minMax

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

@cli.command("shell_IA")
def joueShell() -> None:
    """Jouer dans le terminal.

    Permet de jouer à l'awale dans le terminal, avec une interface simple.

    :raises typer.Exit: Quitte l'application.
    """
    jeu = Awale()
    while not jeu.fin:
        if jeu.joueur == 0:
            jeu.affichePlateau()
            try:
                case = input("Entrez le trou choisi : ") #Mettre un string a la place d un int fait changer le tour 
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
            meilleur_coup, _ = minMax(jeu, profondeur=4, alpha=-sys.maxsize, beta=sys.maxsize, joueuramaximiser=True)
            jeu.joue(meilleur_coup)
            print(f"L'IA a joué dans le trou {meilleur_coup + 1}") 

        jeu.actualiseEtat()
@cli.command("shell_Humains")
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

if __name__ == "__main__":
    cli()