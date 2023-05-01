# pylint: disable=[W,R,C,import-error]

try:
    from .Inventory import Inventory
    from .Entity import Entity
    from .Location import Location
    from .StatusEffectManager import StatusEffectManager
    from .EngineDummy import Engine
    from .Logger import Log
    from .Position import Position
except ImportError:
    from Inventory import Inventory
    from Entity import Entity
    from Location import Location
    from StatusEffectManager import StatusEffectManager
    from EngineDummy import Engine
    from Logger import Log
    from Position import Position

import json

class Player(Entity):
    _loaded = {}

    def __init__(self, discord_id:int, name:str, max_health:int, health:int, inventory:Inventory, location:Location, position:Position, _text_pattern_categories:list[str]):
        self.discord_id = discord_id
        self.name = name
        self.max_health = max_health
        self.health = health
        self.inventory = inventory
        self.status_effects = StatusEffectManager()
        self._text_pattern_categories = _text_pattern_categories
        super().__init__(location, position)

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
        return "\n".join([
            f"{self.name} | {self.health}/{self.max_health} | {self.location}",
            self.inventory.fullStats(),
            self.status_effects.fullStats()
        ]).strip()

    @classmethod
    def loadData(cls, engine) -> list:

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

            _text_pattern_categories: list[str] = data.get("text_pattern_categories")

            Log["loadup"]["player"]("creating player instance...")
            location: Location = Location.fromString(location_str)
            position: Position = Position(*position_list)
            inventory: Inventory = Inventory.from_list(engine, inv_list)
            
            p = cls(Id, name, max_health, health, inventory, location, position, _text_pattern_categories)
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


