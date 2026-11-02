"""Le monstre : les mêmes statistiques que le héros."""

from odoo_final_classe.characters.hero import Hero


class Monster:
    """Un monstre de Final Classe."""

    DAMAGE_CAP = 9999

    def __init__(
        self,
        name: str,
        hp: int,
        mp: int,
        strength: int,
        magic: int,
        defense: int,
        resistance: int,
        xp: int = 0,
        gil: int = 0,
    ) -> None:
        if min(hp, strength, magic, defense, resistance) < 1:
            raise ValueError("Chaque statistique vaut au moins 1")
        self.name = name
        self.strength = strength
        self.magic = magic
        self.defense = defense
        self.resistance = resistance
        self.max_hp = hp
        self.max_mp = mp
        self._hp = hp
        self._mp = mp
        self.xp = xp  # bonus ★★ 3 : l'XP gagnée en le battant
        self.gil = gil  # bonus ★★ 3 : les gils gagnés en le battant

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

    def attack(self, target: Hero) -> int:
        """Frappe le héros ; renvoie les PV qu'il a perdus."""
        damage = self.strength * 10 - target.defense * 5
        damage = max(1, min(Monster.DAMAGE_CAP, damage))
        return target.take_damage(damage)

    def take_damage(self, amount: int) -> int:
        """Retire des PV, sans descendre sous 0 ; renvoie les PV réellement perdus."""
        lost = min(amount, self._hp)
        self._hp -= lost
        return lost
