# pylint: disable=[W,R,C,import-error]

try:
    from .Dungeon import Dungeon
    from .Identifier import Identifier
    from .EngineErrors import InvalidObjectError
except ImportError:
    from Dungeon import Dungeon
    from Identifier import Identifier
    from EngineErrors import InvalidObjectError


import glob, json, re

####XXX######################XXX####
### XXX Path/File Structures XXX ###
####XXX######################XXX####

# │┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌
""" files
my_dungeon
├ resources
│ ├ armor
│ ├ attacks
│ ├ enemies
│ │ └ some_enemy.json
│ └ weapons
│   └ some_weapon.json
├ rooms
│ ├ room1.json
│ └ room2.json
├ my_dungeon.json
└ my_dungeon.py
"""


""" 
> meh_dungeon.json
{
    "name": "Meh Dungeon",
    "version": 0.1,
    "entry_point": "meh_dungeon.rooms.entrance",
    "rooms": {
        "entrance": {
            "name": "Entrance",
            "environment_data": [
                "fish-habitable"
            ],
            "interactions": [
                { # targeted with: (room assumption) meh_dungeon:#door_entrance_left
                    "type": "door",
                    "id": "door_entrance_left",
                    "target": "meh_dungeon"
                },
                {
                    "type": "loot-item",
                    "id": "entrance_loot",
                    "item": "meh_dungeon:weapons/some_weapon"
                }
            ]
        }
    }
}



"""


class AbstractDungeon:
    _loaded = {}

    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data

    @classmethod
    def loadData(cls, inline_handler) -> list:
        files: list[str] = glob.glob("Dungeons/**/*.json")#, recursive=True)

        print(files)

        for file in files:
            with open(file, "r+", encoding="utf-8") as f:
                data = json.load(f)
            
            if m := re.match(r"Dungeons/(?P<dungeon_id>[^/]+)/\1.json", file):
                d: dict = m.groupdict()
                dungeon_id = d.get("dungeon_id")
                cls._loaded.update({dungeon_id: cls(Identifier(dungeon_id, f"Dungeons/{dungeon_id}/"), data)})

        for l in cls._loaded.copy():
            try:
                pass # run getters
            except InvalidObjectError:
                e = cls._loaded.pop(l)
                print(f"Failed to load dungeon: {e}")

        return cls._loaded

if __name__ == "__main__":
    pass #print(AbstractDungeon.loadData())

