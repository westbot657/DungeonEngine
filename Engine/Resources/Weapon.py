# pylint: disable=[W,R,C,import-error]

class Weapon:
    def __init__(self, abstract, name:str, damage:int, range:int, max_durability:int, durability:int, ammo_type):
        self.abstract = abstract
        self.name = name
        self.damage = damage
        self.range = range
        self.durability = durability
        self.max_durability = max_durability
        self.ammo_type = ammo_type

    def __repr__(self):
        return f"Weapon {self.name}: damage:{self.damage} range:{self.range}  durability:{self.durability}"


