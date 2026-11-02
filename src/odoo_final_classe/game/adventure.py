"""Le déroulement de la partie."""

from odoo_final_classe.characters import Hero, Monster
from odoo_final_classe.game.battle import fight
from odoo_final_classe.game.creation import ask_name, create_hero
from odoo_final_classe.game.display import banner, console, hero_sheet


def prologue() -> None:
    """Nibelheim, il y a cinq ans : un duel perdu d'avance."""
    console.print("[italic]Nibelheim, il y a cinq ans…[/]\n")
    cloud = Hero("Cloud", strength=20, magic=12, defense=15, resistance=13)
    sephiroth = Hero("Sephiroth", strength=50, magic=60, defense=99, resistance=99)
    while cloud.is_alive and sephiroth.is_alive:
        console.print(hero_sheet(cloud))
        console.print(hero_sheet(sephiroth))
        damage = cloud.attack(sephiroth)
        console.print(f"Cloud frappe Sephiroth : [bold]{damage}[/] dégât(s).")
        damage = sephiroth.attack(cloud)
        console.print(f"Sephiroth frappe Cloud : [bold red]{damage}[/] dégâts.\n")
    console.print(hero_sheet(cloud))
    console.print("\nSephiroth : « Tu n'es qu'une marionnette. »")
    console.print("[italic]Un jour, tu reviendras. Et cette fois, tu seras prêt.[/]")


def flan(name: str = "Flan") -> Monster:
    """Un Flan : sa gélatine encaisse les coups, mais craint la magie."""
    return Monster(
        name, hp=450, mp=0, strength=14, magic=1, defense=18, resistance=4, xp=30, gil=50
    )


def wolf(name: str = "Loup") -> Monster:
    """Bonus ★★ 4 : un Loup, qui mord fort mais se protège mal."""
    return Monster(name, hp=380, mp=0, strength=16, magic=1, defense=6, resistance=8, xp=40, gil=60)


def reward(hero: Hero, monsters: list[Monster]) -> None:
    """Bonus ★★ 3 : l'XP et les gils des monstres vaincus."""
    xp = sum(monster.xp for monster in monsters)
    gil = sum(monster.gil for monster in monsters)
    hero.gil += gil
    console.print(f"Butin : [yellow]+{xp} XP[/], [yellow]+{gil} gils[/]")
    if hero.gain_xp(xp) > 0:
        console.print(f"[bold yellow]{hero.name} passe au niveau {hero.level} ![/]")


def run() -> None:
    """Lance la partie : le prologue, la création du héros, puis les Plaines de Dalmasca."""
    console.print(banner())
    prologue()
    console.print("\n[bold]Cinq ans plus tard…[/]")
    hero = create_hero(ask_name())
    console.print(hero_sheet(hero))
    console.print("\n[bold cyan]=== Les Plaines de Dalmasca ===[/]")
    waves = [
        [flan()],
        [wolf("Loup A"), wolf("Loup B")],
        [flan(), wolf()]
    ]  # bonus ★★ 4 et ★★★ 5
    for monsters in waves:
        if not fight(hero, monsters):
            console.print("[bold red]=== Game over ===[/]")
            return
        reward(hero, monsters)
        hero.rest()
        console.print(f"{hero.name} se repose : PV et PM au maximum.")
    console.print(hero_sheet(hero))
    console.print("\n[bold green]Les Plaines de Dalmasca sont traversées ![/]")
