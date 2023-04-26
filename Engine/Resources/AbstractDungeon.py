# pylint: disable=[W,R,C,import-error]

try:
    from .Dungeon import Dungeon
    from .Identifier import Identifier
    from .EngineErrors import InvalidObjectError
    from .Logger import Log
    from .AbstractRoom import AbstractRoom
except ImportError:
    from Dungeon import Dungeon
    from Identifier import Identifier
    from EngineErrors import InvalidObjectError
    from Logger import Log
    from AbstractRoom import AbstractRoom


import glob, json, re

####XXX######################XXX####
### XXX Path/File Structures XXX ###
####XXX######################XXX####

# │┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌


class AbstractDungeon:
    _loaded = {}

    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data

        self.name: str = data.get("name", None)
        self.version: float|str|int = data.get("version", None)
        self.entry_point: str = data.get("entry_point", None)
        self.enter_message: str|dict = data.get("enter_message")
        self.exit_message: str|dict = data.get("exit_message")
        self.data: dict = data.get("data", {})


        #room_files: list[str] = glob.glob(f"Dungeons/{self.identifier.name}/rooms/*.json")

        self.abstract_rooms: list[AbstractRoom]


    @classmethod
    def loadData(cls, engine) -> list:
        files: list[str] = glob.glob("Dungeons/**/*.json")#, recursive=True)

        Log["loadup"]["dungeon"](f"Loading {len(files)} dungeons...")

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

        return cls._loaded

if __name__ == "__main__":
    pass #print(AbstractDungeon.loadData())

