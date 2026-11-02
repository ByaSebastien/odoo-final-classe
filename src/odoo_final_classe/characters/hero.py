"""Le héros : ses statistiques, ses PV et ses PM."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pour l'éditeur seulement : monster.py importe déjà hero.py
    from odoo_final_classe.characters.monster import Monster


class Hero:
    """Un héros de Final Classe."""

    BASE_HP = 600
    BASE_MP = 60
    DAMAGE_CAP = 9999
    FIRE_COST = 8
    POTION_HEAL = 200  # bonus ★ 1

    def __init__(self, name: str, strength: int, magic: int, defense: int, resistance: int) -> None:
        if min(strength, magic, defense, resistance) < 1:
            raise ValueError("Chaque statistique vaut au moins 1")
        self.name = name  # passe par le setter
        self.strength = strength
        self.magic = magic
        self.defense = defense
        self.resistance = resistance
        self.max_hp = Hero.BASE_HP
        self.max_mp = Hero.BASE_MP
        self._hp = self.max_hp
        self._mp = self.max_mp
        self.potions = 3  # bonus ★ 1
        self.level = 1  # bonus ★★ 3
        self.xp = 0  # bonus ★★ 3
        self.gil = 0  # bonus ★★ 3

    @property
    def name(self) -> str:
        """Le nom du héros."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        value = value.strip()
        if not value:
            raise ValueError("Un héros a besoin d'un nom")
        self._name = value

    @property
    def hp(self) -> int:
        """Les PV actuels : en lecture seule."""
        return self._hp

    @property
    def mp(self) -> int:
        """Les PM actuels : en lecture seule."""
        return self._mp

    @property
    def is_alive(self) -> bool:
        """Vrai tant qu'il reste des PV."""
        return self._hp > 0

    @property
    def hp_ratio(self) -> float:
        """La part de PV restante, entre 0 et 1."""
        return self._hp / self.max_hp

    @property
    def can_cast_fire(self) -> bool:
        """Vrai s'il reste assez de PM pour lancer Feu."""
        return self._mp >= Hero.FIRE_COST

    @property
    def xp_to_next(self) -> int:
        """Bonus ★★ 3 : l'XP qu'il faut pour passer au niveau suivant."""
        return self.level * 100

    def attack(self, target: Hero | Monster) -> int:
        """Frappe la cible ; renvoie les PV qu'elle a perdus."""
        damage = self.strength * 10 - target.defense * 5
        damage = max(1, min(Hero.DAMAGE_CAP, damage))
        return target.take_damage(damage)

    def cast_fire(self, target: Hero | Monster) -> int:
        """Lance Feu sur la cible ; renvoie les PV perdus, ou 0 si les PM manquent."""
        if not self.can_cast_fire:
            return 0
        self._mp -= Hero.FIRE_COST
        damage = self.magic * 12 - target.resistance * 5
        damage = max(1, min(Hero.DAMAGE_CAP, damage))
        return target.take_damage(damage)

    def take_damage(self, amount: int) -> int:
        """Retire des PV, sans descendre sous 0 ; renvoie les PV réellement perdus."""
        lost = min(amount, self._hp)
        self._hp -= lost
        return lost

    def heal(self, amount: int) -> int:
        """Rend des PV à un héros debout, sans dépasser le maximum ; renvoie les PV rendus."""
        if not self.is_alive:
            return 0
        gained = min(amount, self.max_hp - self._hp)
        self._hp += gained
        return gained

    def rest(self) -> None:
        """Bonus ★★ 4 : entre deux combats, le héros récupère tous ses PV et ses PM."""
        self._hp = self.max_hp
        self._mp = self.max_mp

    def drink_potion(self) -> int:
        """Bonus ★ 1 : boit une potion ; renvoie les PV rendus, ou 0 s'il n'en reste plus."""
        if self.potions == 0:
            return 0
        self.potions -= 1
        return self.heal(Hero.POTION_HEAL)

    def gain_xp(self, amount: int) -> int:
        """Bonus ★★ 3 : ajoute de l'XP ; renvoie le nombre de niveaux gagnés."""
        self.xp += amount
        levels = 0
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.max_hp += 60
            self.strength += 2
            self.magic += 2
            self.defense += 2
            self.resistance += 2
            levels += 1
        return levels
