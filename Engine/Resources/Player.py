# pylint: disable=[W,R,C,import-error]

try:
    from .Inventory import Inventory
    from .Location import Location
except ImportError:
    from Inventory import Inventory
    from Location import Location

import json

class Player:
    _loaded = {}

    def __init__(self, discord_id:int, name:str, max_health:int, health:int, inventory:Inventory, location:Location):
        self.discord_id = discord_id
        self.name = name
        self.max_health = max_health
        self.health = health
        self.inventory = inventory
        self.location = location

    @classmethod
    def loadData(cls) -> list:

        with open("Engine/save_data/players.json", "r+", encoding="utf-8") as f:
            data_list: list[dict] = json.load(f)
        
        for data in data_list:
            Id: int = data.get("id")
            name: str = data.get("name")
            max_health: int = data.get("max_health")
            health: int = data.get("health")
            location_dict: dict = data.get("location")
            inv_list: list = data.get("inventory")

            location: Location = Location.from_dict(location_dict)
            inventory: Inventory = Inventory.from_list(inv_list)



