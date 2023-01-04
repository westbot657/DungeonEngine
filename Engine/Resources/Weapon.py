# pylint: disable=[W,R,C,import-error]

class Weapon:
    def __init__(self, name:str, damage:int, range:int, durability:int):
        self.name = name
        self.damage = damage
        self.range = range
        self.durability = durability

    def __repr__(self):
        return f"Weapon {self.name}: damage:{self.damage} range:{self.range}  durability:{self.durability}"
