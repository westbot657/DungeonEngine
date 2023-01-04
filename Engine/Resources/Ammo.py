# pylint: disable=[W,R,C,import-error]

class Ammo:
    def __init__(self, name:str, bonus_damage:int, max_count:int, count:int=None):
        self.name = name
        self.bonus_damage = bonus_damage
        self.max_count = max_count
        self.count = count or max_count

    def __repr__(self):
        return f"Ammo {self.name}: bonus-damage:{self.bonus_damage} max-count:{self.max_count}"

