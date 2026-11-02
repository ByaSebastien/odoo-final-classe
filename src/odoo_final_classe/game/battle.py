"""Le combat : le héros contre un groupe de monstres."""

from odoo_final_classe.characters import Hero, Monster
from odoo_final_classe.game.creation import ask_int
from odoo_final_classe.game.display import console, hero_sheet, monster_line


def choose_target(monsters: list[Monster]) -> Monster:
    """Bonus ★★★ 5 : le joueur choisit sa cible parmi les monstres debout."""
    standing = [monster for monster in monsters if monster.is_alive]
    if len(standing) == 1:
        return standing[0]
    for number, monster in enumerate(standing, start=1):
        console.print(f"  {number}. {monster_line(monster)}")
    return standing[ask_int("Cible : ", 1, len(standing)) - 1]


def fight(hero: Hero, monsters: list[Monster]) -> bool:
    """Le combat, tour par tour ; renvoie True si le héros gagne."""
    names = ", ".join(monster.name for monster in monsters)
    console.print(f"\n[bold red]Combat : {hero.name} contre {names}[/]")
    turns = dealt = taken = 0  # bonus ★ 2 : le bilan
    while hero.is_alive and any(monster.is_alive for monster in monsters):
        turns += 1
        console.print(f"\n[bold]--- Tour {turns} ---[/]")
        console.print(hero_sheet(hero))
        for monster in monsters:
            if monster.is_alive:
                console.print(monster_line(monster))
        menu = f"1. Attaquer  2. Feu ({Hero.FIRE_COST} PM)  3. Potion (x{hero.potions})\n> "
        choice = ask_int(menu, 1, 3)
        if choice == 2 and not hero.can_cast_fire:
            console.print("[red]Pas assez de PM ![/]")
            continue
        if choice == 3:
            if hero.potions == 0:
                console.print("[red]Plus de potion ![/]")
                continue
            console.print(f"{hero.name} boit une potion : [green]+{hero.drink_potion()} PV[/]")
        else:
            target = choose_target(monsters)
            if choice == 1:
                damage = hero.attack(target)
                console.print(f"{hero.name} attaque {target.name} : [bold]{damage}[/] dégâts.")
            else:
                damage = hero.cast_fire(target)
                console.print(
                    f"{hero.name} lance Feu sur {target.name} : [bold]{damage}[/] dégâts."
                )
            dealt += damage
            if not target.is_alive:
                console.print(f"[green]{target.name} est vaincu ![/]")
        for monster in monsters:
            if monster.is_alive and hero.is_alive:
                damage = monster.attack(hero)
                taken += damage
                console.print(f"{monster.name} attaque {hero.name} : [bold red]{damage}[/] dégâts.")
    won = hero.is_alive
    console.print("\n[bold green]Victoire ![/]" if won else f"\n[bold red]{hero.name} est K.O…[/]")
    console.print(f"[dim]Bilan : {turns} tours, {dealt} dégâts infligés, {taken} dégâts reçus.[/]")
    return won
