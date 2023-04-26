# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
    from .DynamicValue import DynamicValue
    from .Util import Util
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier
    from DynamicValue import DynamicValue
    from Util import Util

class Weapon(GameObject):
    identifier = Identifier("engine", "object/", "weapon")
    def __init__(self, abstract, name:str, damage:DynamicValue, range:DynamicValue, max_durability:int, durability:int, ammo_type, events:dict):
        self.abstract = abstract
        self.name = name
        self.damage = damage
        self.range = range
        self.durability = durability
        self.max_durability = max_durability
        self.ammo_type = ammo_type
        self.events = events

    def __repr__(self):
        return f"Weapon {self.name}: damage:{self.damage} range:{self.range}  durability:{self.durability}"

    def bonuses(self, engine):
        return f"+{self.damage.quickDisplay(engine)}dmg {self.range.quickDisplay(engine)}ft"

    def fullStats(self, engine, is_equipped=False):
        return f"{self.name} +{self.damage.fullDisplay(engine)}dmg {self.range.fullDisplay(engine)}ft {Util.getDurabilityBar(self.durability, self.max_durability)}" + (" [EQUIPPED]" if is_equipped else "")

    def quickStats(self, engine):
        return f"{self.name} {Util.getDurabilityBar(self.durability, self.max_durability)}"

    # onUse
    # onDamage
    # onBreak
    # onAttack
    # onEquip
    # onUnequip
    # onRepair



