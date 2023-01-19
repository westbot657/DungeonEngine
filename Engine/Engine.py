# pylint: disable=[W,R,C,import-error]
from Resources.AbstractAmmo         import AbstractAmmo, Ammo
from Resources.AbstractArmor        import AbstractArmor, Armor
from Resources.AbstractCombat       import AbstractCombat, Combat
from Resources.AbstractItem         import AbstractItem, Item
from Resources.AbstractLootTable    import AbstractLootTable, LootTable
from Resources.AbstractStatusEffect import AbstractStatusEffect, StatusEffect
from Resources.AbstractWeapon       import AbstractWeapon, Weapon
from Resources.Identifier           import Identifier


import glob, json, re

class Engine:
    _engine = None
    def __new__(cls):
        if not cls._engine:
            cls._engine = self = super().__new__(cls)
            self.init()
        return cls._engine

    def init(self):
        ...


    def loadGame(self):
        ...

    def saveGame(self):
        ...

