# pylint: disable=[W,R,C,import-error]

try:
    from .Inventory import Inventory
    from .Entity import Entity
    from .Location import Location
    from .StatusEffectManager import StatusEffectManager
    from .EngineDummy import Engine
    from .Logger import Log
    from .Position import Position
    from .EngineErrors import MemoryError, UnknownPlayerError
    from .FunctionalElement import FunctionalElement
    from .FunctionMemory import FunctionMemory
    from .Weapon import Weapon
    from .Tool import Tool
    from .Item import Item
    from .Ammo import Ammo
    from .Armor import Armor
    from .EngineOperation import _EngineOperation
except ImportError:
    from Inventory import Inventory
    from Entity import Entity
    from Location import Location
    from StatusEffectManager import StatusEffectManager
    from EngineDummy import Engine
    from Logger import Log
    from Position import Position
    from EngineErrors import MemoryError, UnknownPlayerError
    from FunctionalElement import FunctionalElement
    from FunctionMemory import FunctionMemory
    from Weapon import Weapon
    from Tool import Tool
    from Item import Item
    from Ammo import Ammo
    from Armor import Armor
    from EngineOperation import _EngineOperation

from typing import Any

import json

class Player(Entity):
    _loaded = {}

    def __init__(self, discord_id:int, name:str, max_health:int, health:int, inventory:Inventory, location:Location, position:Position, _text_pattern_categories:list[str], in_combat:bool):
        self.discord_id = discord_id
        self.name = name
        self.max_health = max_health
        self.health = health
        self.inventory = inventory
        self.inventory.setParent(self)
        self.status_effects = StatusEffectManager()
        self.in_combat = in_combat
        self._combat = None

        self.dungeon_data = {}
        self._text_pattern_categories = _text_pattern_categories
        super().__init__(location, position)

    def _getProperty(self, obj, propertyTree:list):
        while propertyTree:
            if isinstance(obj, FunctionalElement):
                obj_props = obj.getLocalVariables()
                curr = propertyTree.pop(0)
                if curr in obj_props:
                    obj = obj_props[curr]
                else:
                    raise MemoryError(f"Variable '{obj}' has no property '{curr}'")
            else:
                break
        return obj

    def ref(self, dungeon_name:str, value_name:str):
        if dungeon_dat := self.dungeon_data.get(dungeon_name, None):
            dungeon_dat: dict
            try:
                
                props = [f".{prop}" if prop else "." for prop in value_name.split(".")]
                prop = props.pop(0)[1:]
                if prop in dungeon_dat:
                    return self._getProperty(dungeon_dat[prop], props)

                raise MemoryError(f"Variable referenced before assignment: '{value_name}'")
            
            except KeyError:
                pass

        raise MemoryError(f"Variable referenced before assignment: '{value_name}'")

    def store(self, dungeon_name:str, value_name:str, value:Any):
        if dungeon_name not in self.dungeon_data:
            self.dungeon_data.update({dungeon_name: {}})
        
        self.dungeon_data[dungeon_name].update({value_name: value})

    def addHealth(self, health):
        self.health = min(self.max_health, self.health + health)

    def setHealth(self, health):
        self.health = min(max(0, health), self.max_health)

    def _get_save(self, function_memory):
        data = {
            "id": self.discord_id,
            "name": self.name,
            "max_health": self.max_health,
            "health": self.health,
            "location": self.location._get_save(function_memory),
            "position": self.position._get_save(function_memory),
            "inventory": self.inventory._get_save(function_memory),
            "status_effects": self.status_effects._get_save(function_memory)
        }
        return data

    def __repr__(self):
        return self.name

    def fullInventoryStats(self):
        text = "\n".join([
            f"{self.name} | {self.health}/{self.max_health} | {self.location}",
            self.inventory.fullStats(),
            self.status_effects.fullStats()
        ]).strip()


        return text


    def attackEnemy(self, function_memory:FunctionMemory, enemy):
        ...
    
    def onAttacked(self, function_memory:FunctionMemory, attacker, damage:int):
        ...

        # armor onPlayerHit method
        # status effect onPlayerHit methods
        # equipped tool onPlayerHit method
        # weapon onPlayerHit method

        equipped_weapon: Weapon = self.inventory.getEquipped(Weapon)
        equipped_tool: Tool = self.inventory.getEquipped(Tool)
        equipped_armor: Armor = self.inventory.getEquipped(Armor)

        function_memory.update({
            "damage": damage,
            "attacker": attacker
        })

        for gameObject in [equipped_armor, equipped_tool, equipped_weapon, self.status_effects]:
            gameObject: Armor|Tool|Weapon|StatusEffectManager
            ev = gameObject.onPlayerHit(function_memory, damage)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                v = e.value or (v if not isinstance(v, _EngineOperation) else None)
            
            if (dmg := function_memory.symbol_table.get("damage", None)) is not None:
                if isinstance(dmg, int):
                    function_memory.update({
                        "damage": max(0, dmg)
                    })
                    damage = max(0, dmg)
                else:
                    function_memory.update({
                        "damage": damage
                    })

        self.health -= damage

        if self.health <= 0:
            raise Exception(f"TODO: I have no idea how to do player death...")


    @classmethod
    def getPlayer(cls, player_id):
        if player_id in cls._loaded:
            return cls._loaded.get(player_id)
        raise UnknownPlayerError(player_id)

    @classmethod
    def loadData(cls, engine) -> dict:

        Inventory._default_equips = {
            "engine:weapon": engine.loader.abstract_weapons["engine:weapons/unnarmed_strike"],
            "engine:armor": engine.loader.abstract_armor["engine:armor/common_clothes"]
        }

        Log["loadup"]["player"]("Loading Player Data...")
        with open("Engine/save_data/players.json", "r+", encoding="utf-8") as f:
            data_list: list[dict] = json.load(f)
        
        for data in data_list:
            Id: int = data.get("id")
            name: str = data.get("name")
            max_health: int = data.get("max_health")
            health: int = data.get("health")
            location_str: str = data.get("location")
            position_list: list = data.get("position")
            inv_list: list = data.get("inventory")
            in_combat: bool = data.get("in_combat", False)

            _text_pattern_categories: list[str] = data.get("text_pattern_categories")

            Log["loadup"]["player"]("creating player instance...")
            location: Location = Location.fromString(location_str)
            position: Position = Position(*position_list)
            inventory: Inventory = Inventory.from_list(engine, inv_list)
            
            p = cls(Id, name, max_health, health, inventory, location, position, _text_pattern_categories, in_combat)
            cls._loaded.update({Id: p})
            Log["loadup"]["player"]("player instance created")
        Log["loadup"]["player"](f"Loaded players: {cls._loaded}")
        return cls._loaded

    @classmethod
    def saveData(cls, engine):
        # TODO: implement this
        pass


if __name__ == "__main__":
    pass


