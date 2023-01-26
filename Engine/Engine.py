# pylint: disable=[W,R,C,import-error]
from Resources.AbstractAmmo         import AbstractAmmo, Ammo
from Resources.AbstractArmor        import AbstractArmor, Armor
from Resources.AbstractCombat       import AbstractCombat, Combat
from Resources.AbstractItem         import AbstractItem, Item
from Resources.LootTable            import LootTable, LootPool, LootEntry
from Resources.AbstractStatusEffect import AbstractStatusEffect, StatusEffect
from Resources.AbstractWeapon       import AbstractWeapon, Weapon
from Resources.Identifier           import Identifier
from Resources.DungeonLoader        import DungeonLoader
from Resources.FunctionMemory       import FunctionMemory


import glob, json, re

class Engine:
    _engine = None
    def __new__(cls):
        if not cls._engine:
            cls._engine = self = super().__new__(cls)
            self.init()
        return cls._engine

    def init(self):
        self.loader: DungeonLoader = DungeonLoader()
        self.function_memory: FunctionMemory = FunctionMemory()

    def evaluateFunction(self, data:dict):
        return self.loader.evaluateFunction(self, data)

    def loadGame(self):
        self.loader.loadGame(self)

    def saveGame(self):
        ...

    def run(self):
        ...


if __name__ == "__main__":
    ...
