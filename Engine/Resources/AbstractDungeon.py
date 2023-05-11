# pylint: disable=[W,R,C,import-error]

try:
    from .Dungeon import Dungeon
    from .Identifier import Identifier
    from .EngineErrors import InvalidObjectError
    from .Logger import Log
    from .AbstractRoom import AbstractRoom
    from .Environment import Environment
    from .FunctionMemory import FunctionMemory
    from .DynamicValue import DynamicValue
    from .Util import Util
    from .Location import Location
except ImportError:
    from Dungeon import Dungeon
    from Identifier import Identifier
    from EngineErrors import InvalidObjectError
    from Logger import Log
    from AbstractRoom import AbstractRoom
    from Environment import Environment
    from FunctionMemory import FunctionMemory
    from DynamicValue import DynamicValue
    from Util import Util
    from Location import Location


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
        self.environment: dict = data.get("environment", {})
        self.entry_point: Location = Location.fromString(data.get("entry_point", None))
        self.events: dict|None = data.get("events", {})
        self.data: dict = data.get("data", {})


        #room_files: list[str] = glob.glob(f"Dungeons/{self.identifier.name}/rooms/*.json")

    def createRooms(self, function_memory:FunctionMemory):
        return AbstractRoom.getDungeonRooms(function_memory, self.identifier.full())


    def createInstance(self, function_memory, **override_values):
        return Dungeon(self,
            override_values.get("name", self.name),
            self.version,
            Environment(self.environment),
            self.entry_point,
            self.events,
            Util.deepCopy(self.data),
            self.createRooms(function_memory)
        )

    @classmethod
    def loadData(cls, engine) -> list:
        files: list[str] = glob.glob("Dungeons/**/*.json")#, recursive=True)

        Log["loadup"]["dungeon"](f"Loading {len(files)} dungeons...")

        for file in files:
            with open(file, "r+", encoding="utf-8") as f:
                data = json.load(f)

            Id = Identifier("dungeon", "", file.replace("\\", "/").rsplit("/", 1)[1].rsplit(".", 1)[0])
            Log["debug"]["abstract"]["dungeon"](f"dungeon id: {Id.full()}")
            cls._loaded.update({Id.full(): cls(Id, data)})

        for l in cls._loaded.copy():
            try:
                pass # run getters
            except InvalidObjectError:
                e = cls._loaded.pop(l)

        return cls._loaded

    def _get_save(self, function_memory:FunctionMemory):
        return {
            "name": self.name,
            "version": self.version,
            "environment": self.environment,
            "entry_point": self.entry_point._get_save(function_memory),
            #"events": self.events,
            "data": self.data
        }

    @classmethod
    def saveData(cls, function_memory:FunctionMemory):
        ...


if __name__ == "__main__":
    pass #print(AbstractDungeon.loadData())

