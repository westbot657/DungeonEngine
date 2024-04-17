# pylint: disable=[W,R,C,import-error]

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
from .Map import Map
from .Loader import Loader
from .Serializer import Serializer, Serializable

import glob, json, re

####XXX######################XXX####
### XXX Path/File Structures XXX ###
####XXX######################XXX####

# │┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌


@Serializable("AbstractCombat")
class AbstractDungeon:
    _loaded = {}
    _dungeon_instances = []

    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data

        self.name: str = data.get("name", None)
        self.version: float|str|int = data.get("version", None)
        self.environment: dict = data.get("environment", {})
        self.entry_point: Location = Location.fromString(data.get("entry_point", None))
        self.events: dict|None = data.get("events", {})
        self.data: dict = data.get("data", {})
        self.recovery_location: Location = Location.fromString(l) if (l := data.get("recovery_location", None)) is not None else Location.fromString("world:rooms/start")

        if map := data.get("map", None): self.map = Map(map)
        else: self.map = None

    def createRooms(self, function_memory:FunctionMemory):
        return AbstractRoom.getDungeonRooms(function_memory, self.identifier.full())

    def createInstance(self, function_memory, **override_values):
        dungeon = Dungeon(self,
            override_values.get("name", self.name),
            self.version,
            Environment(self.environment),
            self.entry_point,
            self.events,
            Util.deepCopy(self.data),
            self.createRooms(function_memory),
            self.recovery_location
        )
        dungeon.map = self.map
        AbstractDungeon._dungeon_instances.append(dungeon)
        return dungeon

    @classmethod
    def loadData(cls, engine) -> list:
        files: list[str] = glob.glob("./Dungeons/**/*.json")#, recursive=True)

        for file in files.copy():
            if file.endswith(("ec_functions.json", "editor_data.json")):
                files.remove(file)

        Log["loadup"]["dungeon"](f"Loading {len(files)} dungeons...")
        Log["debug"]["dungeon"](f"dungeons: {", ".join(files)}")

        for file in files:
            data = Loader.load(file)

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
            "recovery_location": self.recovery_location._get_save(function_memory),
            "data": self.data
        }

    @classmethod
    def saveData(cls, function_memory:FunctionMemory):
        for dungeon in cls._dungeon_instances:
            dungeon: Dungeon
            dungeon.saveData(function_memory)

    def serialize(self):
        return {
            "identifier": Serializer.serialize(self.identifier),
            "_raw_data": Serializer.serialize(self._raw_data),
            "name": Serializer.serialize(self.name),
            "version": Serializer.serialize(self.version),
            "environment": Serializer.serialize(self.environment),
            "entry_point": Serializer.serialize(self.entry_point),
            "events": Serializer.serialize(self.events),
            "data": Serializer.serialize(self.data),
            "recovery_location": Serializer.serialize(self.recovery_location),
            "map": Serializer.serialize(self.map)
        }
    
    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)


if __name__ == "__main__":
    pass #print(AbstractDungeon.loadData())

