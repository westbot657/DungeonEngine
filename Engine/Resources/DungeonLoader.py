# pylint: disable=[W,R,C,import-error]

try:
    from .AbstractAmmo import AbstractAmmo
    from .AbstractArmor import AbstractArmor
    from .AbstractCombat import AbstractCombat
    from .AbstractDungeon import AbstractDungeon
    from .AbstractItem import AbstractItem
    from .AbstractLootTable import AbstractLootTable
    from .AbstractRoom import AbstractRoom
    from .AbstractStatusEffect import AbstractStatusEffect
    from .AbstractTool import AbstractTool
    from .AbstractWeapon import AbstractWeapon
except ImportError:
    from AbstractAmmo import AbstractAmmo
    from AbstractArmor import AbstractArmor
    from AbstractCombat import AbstractCombat
    from AbstractDungeon import AbstractDungeon
    from AbstractItem import AbstractItem
    from AbstractLootTable import AbstractLootTable
    from AbstractRoom import AbstractRoom
    from AbstractStatusEffect import AbstractStatusEffect
    from AbstractTool import AbstractTool
    from AbstractWeapon import AbstractWeapon


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
        self.abstract_loot_tables: dict[str, AbstractLootTable] = {}
        self.abstract_rooms: dict[str, AbstractRoom] = {}
        self.abstract_status_effects: dict[str, AbstractStatusEffect] = {}
        self.abstract_tools: dict[str, AbstractTool] = {}
        self.abstract_weapons: dict[str, AbstractWeapon] = {}

    def evaluateFunction(self, data:dict, symbol_table:dict=None):
        if not symbol_table: symbol_table = {}
        
        if (funcs := data.get("functions", None)) is not None:
            for func in funcs:
                result = None
                res = self.evaluateFunction(func, symbol_table)
                if res: result = res
            return result
        
        elif (func := data.get("function", None)) is not None:
            ...
        
        else:
            ... # ?


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


    def loadGame(self):
        self.abstract_ammo = AbstractAmmo.loadData()
        self.abstract_armor = AbstractArmor.loadData()
        self.abstract_combats = AbstractCombat.loadData()

        self.abstract_items = AbstractItem.loadData()
        self.abstract_loot_tables = AbstractLootTable.loadData()
        
        # self.abstract_rooms = AbstractRoom.loadData()
        self.abstract_status_effects = AbstractStatusEffect.loadData()
        self.abstract_tools = AbstractTool.loadData()
        self.abstract_weapons = AbstractWeapon.loadData()

        self.abstract_dungeons = AbstractDungeon.loadData()

