from odoo_final_classe.characters import Hero
from odoo_final_classe.game.display import console, banner, hero_sheet


def run():
    console.print(banner())
    cloud = Hero("Cloud", strength=20, magic=12, defense=15, resistance=13)
    cloud.take_damage(470)
    console.print(hero_sheet(cloud))