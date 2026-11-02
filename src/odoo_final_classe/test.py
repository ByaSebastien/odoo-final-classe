from odoo_final_classe.characters import Hero

tidus = Hero("Tidus", strength=20, magic=12, defense=15, resistance=13)
jecht = Hero("Jecht", strength=16, magic=10, defense=25, resistance=12)
print(tidus.attack(jecht), jecht.hp)
print(jecht.attack(tidus), tidus.hp)