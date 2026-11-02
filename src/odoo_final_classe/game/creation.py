"""La création du héros : son nom, et la répartition de ses points."""

from odoo_final_classe.characters import Hero
from odoo_final_classe.game.display import console

POINTS = 20  # les points à répartir
BASE_STAT = 10  # la valeur de départ de chaque statistique


def ask_int(prompt: str, low: int, high: int) -> int:
    """Demande un nombre entre low et high, jusqu'à obtenir une réponse valide."""
    while True:
        answer = input(prompt).strip()
        if answer.isdigit() and low <= int(answer) <= high:
            return int(answer)
        console.print(f"[red]Un nombre entre {low} et {high}, s'il vous plaît.[/]")


def ask_name() -> str:
    """Demande le nom du héros, jusqu'à obtenir un nom non vide."""
    while True:
        name = input("Nom de votre héros : ").strip()
        if name:
            return name.title()
        console.print("[red]Un héros a besoin d'un nom.[/]")


def create_hero(name: str) -> Hero:
    """Répartit les points entre FOR, MAG et DÉF ; la RÉS reçoit le reste."""
    console.print(f"Chaque statistique vaut {BASE_STAT}. Répartissez {POINTS} points.")
    remaining = POINTS
    bonus: dict[str, int] = {}
    for stat in ("FOR", "MAG", "DÉF"):
        points = ask_int(f"{stat} (+0 à +{remaining}) : ", 0, remaining)
        bonus[stat] = points
        remaining -= points
    bonus["RÉS"] = remaining
    console.print(f"RÉS reçoit les {remaining} points restants.")
    return Hero(
        name,
        strength=BASE_STAT + bonus["FOR"],
        magic=BASE_STAT + bonus["MAG"],
        defense=BASE_STAT + bonus["DÉF"],
        resistance=BASE_STAT + bonus["RÉS"],
    )
