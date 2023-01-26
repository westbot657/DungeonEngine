# pylint: disable=[W,R,C,import-error]

try:
    from .AbstractAmmo import AbstractAmmo
    from .AbstractArmor import AbstractArmor
    from .AbstractCombat import AbstractCombat
    from .AbstractDungeon import AbstractDungeon
    from .AbstractItem import AbstractItem
    from .AbstractRoom import AbstractRoom
    from .AbstractStatusEffect import AbstractStatusEffect
    from .AbstractTool import AbstractTool
    from .AbstractWeapon import AbstractWeapon
    from .Functions import LoaderFunction
    from .Identifier import Identifier
    from .EngineDummy import Engine
    from .EngineErrors import InvalidObjectError, FunctionLoadError
except ImportError:
    from AbstractAmmo import AbstractAmmo
    from AbstractArmor import AbstractArmor
    from AbstractCombat import AbstractCombat
    from AbstractDungeon import AbstractDungeon
    from AbstractItem import AbstractItem
    from AbstractRoom import AbstractRoom
    from AbstractStatusEffect import AbstractStatusEffect
    from AbstractTool import AbstractTool
    from AbstractWeapon import AbstractWeapon
    from Functions import LoaderFunction
    from Identifier import Identifier
    from EngineDummy import Engine
    from EngineErrors import InvalidObjectError, FunctionLoadError

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

    def checkPredicate(self, engine:Engine, predicate:dict) -> bool:
        ...

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
                    if not self.checkPredicate(engine, predicate): return None

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


    def constructAmmo(self, data:dict):
        ...
    def constructArmor(self, data:dict):
        ...
    def constructCombat(self, data:dict):
        ...
    # def constructDungeon(self, data:dict): # This shouldn't be needed, there should be no in-line dungeons inside a dungeon
    #     ...
    def constructItem(self, data:dict):
        ...
    def constructLootTable(self, data:dict):
        ...
    # def constructRoom(self, data:dict): # also shouldn't be any in-line rooms
    #     ...
    def constructStatusEffect(self, data:dict):
        ...
    def constructTool(self, data:dict):
        ...
    def constructWeapon(self, data:dict):
        ...


    def getObject(self, identifier:Identifier|str):
        if isinstance(identifier, str):
            if m := re.match(r"(?P<namespace>[a-zA-Z0-9_]+):(?P<path>(?:[a-zA-Z0-9_]+/)*)(?P<name>[a-zA-Z0-9_])", identifier):
                d = m.groupdict()
                identifier = Identifier(d["namespace"], d["path"], d["name"])
            else:
                raise InvalidObjectError(f"Unrecognized identifier: '{identifier}'")

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

