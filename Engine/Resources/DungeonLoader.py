# pylint: disable=[W,R,C,import-error]

try:
    from .AbstractAmmo import AbstractAmmo, Ammo
    from .AbstractArmor import AbstractArmor, Armor
    from .AbstractCombat import AbstractCombat, Combat
    from .AbstractDungeon import AbstractDungeon, Dungeon
    from .AbstractItem import AbstractItem, Item
    from .AbstractRoom import AbstractRoom, Room
    from .AbstractStatusEffect import AbstractStatusEffect, StatusEffect
    from .AbstractTool import AbstractTool, Tool
    from .AbstractWeapon import AbstractWeapon, Weapon
    from .Functions import LoaderFunction
    from .Identifier import Identifier
    from .EngineDummy import Engine
    from .EngineErrors import InvalidObjectError, FunctionLoadError
    from .LootTable import LootTable
    from .AbstractGameObject import AbstractGameObject, GameObject
except ImportError:
    from AbstractAmmo import AbstractAmmo, Ammo
    from AbstractArmor import AbstractArmor, Armor
    from AbstractCombat import AbstractCombat, Combat
    from AbstractDungeon import AbstractDungeon, Dungeon
    from AbstractItem import AbstractItem, Item
    from AbstractRoom import AbstractRoom, Room
    from AbstractStatusEffect import AbstractStatusEffect, StatusEffect
    from AbstractTool import AbstractTool, Tool
    from AbstractWeapon import AbstractWeapon, Weapon
    from Functions import LoaderFunction
    from Identifier import Identifier
    from EngineDummy import Engine
    from EngineErrors import InvalidObjectError, FunctionLoadError
    from LootTable import LootTable
    from AbstractGameObject import AbstractGameObject, GameObject

import re

class DungeonLoader:
    _loader = None
    def __new__(cls):
        if not cls._loader:
            cls._loader = self = super().__new__(cls)
            self.init()
        return cls._loader

    def init(self):
        self.abstract_ammo: dict[str, AbstractAmmo] = {}
        self.abstract_armor: dict[str, AbstractArmor] = {}
        self.abstract_combats: dict[str, AbstractCombat] = {}
        self.abstract_dungeons: dict[str, AbstractDungeon] = {}
        self.abstract_items: dict[str, AbstractItem] = {}
        #self.abstract_loot_tables: dict[str, AbstractLootTable] = {}
        self.abstract_rooms: dict[str, AbstractRoom] = {}
        self.abstract_status_effects: dict[str, AbstractStatusEffect] = {}
        self.abstract_tools: dict[str, AbstractTool] = {}
        self.abstract_weapons: dict[str, AbstractWeapon] = {}


    def evaluateFunction(self, engine:Engine, data:dict, expected_key:str|None=None):
        
        if (funcs := data.get("functions", None)) is not None:
            for func in funcs:
                result = None
                res = self.evaluateFunction(engine, func, expected_key)
                if res: result = res
            return result
        
        elif (func := data.get("function", None)) is not None:
            if f := LoaderFunction.getFunction(func):
                f: LoaderFunction

                if (predicate := data.get("predicate", None)) is not None:
                    if not engine.function_memory.checkPredicate(engine, predicate): return None

                args = {}
                for key, item in data.items():
                    if key in ["function", "#store"]: continue
                    if isinstance(item, dict):
                        args.update({key: self.evaluateFunction(engine, item, expected_key)})
                    else:
                        args.update({key: item})
                r = f._call(engine, args)
                if var := data.get("#store", None):
                    engine.function_memory.store(var, r)
                return r

        elif (var := data.get("#ref", None)) is not None:
            return engine.function_memory.ref(var)

        elif isinstance(data, dict):
            dat = {}
            for key, item in data.items():
                dat.update({key, self.evaluateFunction(engine, item, expected_key)})
            return dat

        else:
            return data


    def constructAmmo(self, data:dict) -> Ammo:
        ...
    def constructArmor(self, data:dict) -> Armor:
        ...
    def constructCombat(self, data:dict) -> Combat:
        ...
    # def constructDungeon(self, data:dict) -> Dungeon: # This shouldn't be needed, there should be no in-line dungeons inside a dungeon
    #     ...
    def constructItem(self, data:dict) -> Item:
        ...
    def constructLootTable(self, data:dict) -> LootTable:
        ...
    # def constructRoom(self, data:dict) -> Room: # also shouldn't be any in-line rooms
    #     ...
    def constructStatusEffect(self, data:dict) -> StatusEffect:
        ...
    def constructTool(self, data:dict) -> Tool:
        ...
    def constructWeapon(self, data:dict) -> Weapon:
        ...
    
    def constructGameObject(self, data:dict) -> GameObject:
        if obj_type := data.get("type", None):
            identifier = Identifier.fromString(obj_type)
            identifier.path = "object/"
            match identifier.full():
                case "engine:object/ammo":
                    return self.constructAmmo(data)
                case "engine:object/armor":
                    return self.constructArmor(data)
                case "engine:object/item":
                    return self.constructItem(data)
                case "engine:object/tool":
                    return self.constructTool(data)
                case "engine:object/weapon":
                    return self.constructWeapon(data)
                case _:
                    raise InvalidObjectError(f"Unrecognized GameObject type: '{identifier.full()}'")
        elif "parent" in data:
            ...
            # determine parent type
        else:
            raise InvalidObjectError("No type or parent given for GameObject")
            

    def getAmmo(self, identifier:Identifier|str) -> AbstractAmmo:
        identifier: Identifier = Identifier.fromString(identifier)
        
    def getArmor(self, identifier:Identifier|str) -> AbstractArmor:
        identifier: Identifier = Identifier.fromString(identifier)
    
    def getItem(self, identifier:Identifier|str) -> AbstractItem:
        identifier: Identifier = Identifier.fromString(identifier)
    
    def getStatusEffect(self, identifier:Identifier|str) -> AbstractStatusEffect:
        identifier: Identifier = Identifier.fromString(identifier)

    def getTool(self, identifier:Identifier|str) -> AbstractTool:
        identifier: Identifier = Identifier.fromString(identifier)
    
    def getWeapon(self, identifier:Identifier|str) -> AbstractWeapon:
        identifier: Identifier = Identifier.fromString(identifier)

    def getGameObject(self, identifier:Identifier|str) -> AbstractGameObject:
        identifier: Identifier = Identifier.fromString(identifier)

        # TODO: actually search for object (however that needs to be done)

    def loadGame(self, engine:Engine):
        self.abstract_ammo = AbstractAmmo.loadData(self)
        self.abstract_armor = AbstractArmor.loadData(self)
        self.abstract_combats = AbstractCombat.loadData(self)

        self.abstract_items = AbstractItem.loadData(self)
        #self.abstract_loot_tables = AbstractLootTable.loadData(self)
        
        # self.abstract_rooms = AbstractRoom.loadData(self)
        self.abstract_status_effects = AbstractStatusEffect.loadData(self)
        self.abstract_tools = AbstractTool.loadData(self)
        self.abstract_weapons = AbstractWeapon.loadData(self)

        self.abstract_dungeons = AbstractDungeon.loadData(self)

    def saveGame(self, engine:Engine):
        # TODO: implement saving
        pass
