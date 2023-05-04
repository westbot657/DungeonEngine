# pylint: disable=[W,R,C,import-error]

try:
    from .Room import Room
    from .Identifier import Identifier
    from .Logger import Log
    from .EngineErrors import InvalidObjectError
    from .EngineDummy import Engine
    from .AbstractInteractable import Interactable, AbstractInteractable
    from .FunctionMemory import FunctionMemory
    from .DynamicValue import DynamicValue
    from .Location import Location
    from .Environment import Environment
except ImportError:
    from Room import Room
    from Identifier import Identifier
    from Logger import Log
    from EngineErrors import InvalidObjectError
    from EngineDummy import Engine
    from AbstractInteractable import Interactable, AbstractInteractable
    from FunctionMemory import FunctionMemory
    from DynamicValue import DynamicValue
    from Location import Location
    from Environment import Environment

import glob, json, re

class AbstractRoom:
    _loaded = {}
    _link_parents = []

    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data
        self.parent: AbstractRoom|None = None
        self.children: list[AbstractRoom] = []
        
        if "parent" in data:
            AbstractRoom._link_parents.append((self, data["parent"]))

        self.name: str = data.get("name", None)
        self.events: dict|None = data.get("events", None)
        self.environment: dict = data.get("environment", {})
        self.interactions: list = data.get("interactions", [])

        self.is_template: bool = data.get("template", False)

    def _set_parent(self, parent):
        self.parent = parent
        parent.children.append(self)

    def is_parent_of(self, other):
        p = other
        while p is not None:
            if self == p:
                return True
            p = p.parent
        return False
    
    def inherets_from(self, other):
        p = self
        while p is not None:
            if p == other:
                return True
            p = p.parent
        return False

    def get_children(self, depth:int=-1): # recursive way to get a flat list of all sub children to some depth
        children = []
        for child in self.children:
            if not child.is_template:
                children.append(child)
            if depth != 0:
                children += child.get_children(depth-1)
        return children

    def get_parent_chain(self):
        if self.parent is None:
            return []
        else:
            return [self.parent] + self.parent.get_parent_chain()


    def getName(self):
        n = self.name or (self.parent.getName() if self.parent else None)
        if n is not None: return n
        raise InvalidObjectError(f"Tool has no name! ({self.identifier})")
    
    def getEvents(self):
        if self.events is None:
            e = self.parent.getEvents() if self.parent else None
        else:
            e = self.events
        return e or {}

    def getInteractions(self, function_memory:FunctionMemory) -> list[Interactable]:
        interactables = []
        for interaction in self.interactions:
            interactables.append(AbstractInteractable.createInteractable(function_memory, interaction))
        return interactables


    def createInstance(self, function_memory:FunctionMemory, **override_values):
        return Room(self,
            Location.fromString(self.identifier.full()),
            override_values.get("name", self.getName()),
            self.getEvents(),
            self.getInteractions(function_memory),
            Environment(self.environment)
        )

    @classmethod
    def getDungeonAbstractRooms(cls, function_memory:FunctionMemory, dungeon_name:str):
        rooms = {}
        for room in cls._loaded.values():
            room: AbstractRoom
            if room.identifier.namespace == dungeon_name:
                rooms.update({room.identifier.full(): room})
        return rooms

    @classmethod
    def getDungeonRooms(cls, function_memory:FunctionMemory, dungeon_name:str):
        rooms = {}
        for room in cls._loaded.values():
            room: AbstractRoom
            if room.identifier.namespace == dungeon_name.split(":")[1]:
                rooms.update({room.identifier.full(): room.createInstance(function_memory)})
        Log["debug"]["abstract"]["room"](f"getRooms: dungeon: {dungeon_name}, rooms:{rooms}")
        return rooms

    @classmethod
    def loadData(cls, engine:Engine):
        files: list[str] = glob.glob("**/rooms/**/*.json", recursive=True)
        Log["loadup"]["abstract"]["room"](f"found {len(files)} item files")

        for file in files:
            file: str
            Log["loadup"]["abstract"]["room"](f"loading AbstractRoom from '{file}'")
            with open(file, "r+", encoding="utf-8") as f:
                data = json.load(f)
            
            Id = Identifier.fromFile(file)
            cls._loaded.update({Id.full(): cls(Id, data)})
        
        Log["loadup"]["abstract"]["room"]("linking AbstractRoom parents...")
        for w, p in cls._link_parents:
            w: AbstractRoom
            p: str
            if parent := cls._loaded.get(p, None):
                if parent is w:
                    Log["ERROR"]["loadup"]["abstract"]["room"]("cannot set object as it's own parent")
                    #cls._loaded.pop(w.identifier.full())
                    continue
                elif w in parent.get_parent_chain():
                    Log["ERROR"]["loadup"]["abstract"]["room"]("circular parent loop found")
                    #cls._loaded.pop(w.identifier.full())
                    #cls._loaded.pop(parent.identifier.full())
                    continue
                w._set_parent(parent)
            else:
                Log["ERROR"]["loadup"]["abstract"]["room"](f"parent does not exist: '{p}'")

        Log["loadup"]["abstract"]["room"]("verifying AbstractRoom completion...")
        Log.track(len(cls._loaded), "loadup", "abstract", "room")
        for l, o in cls._loaded.copy().items():
            l: str
            o: AbstractRoom
            if o.is_template:
                Log.success()
                continue
            try:
                
                Log.success()
            except InvalidObjectError:
                e: AbstractRoom = cls._loaded.pop(l)
                Log.fail()
                Log.ERROR("loadup", "abstract", "room", f"failed to load room: {e.identifier}")

        Log.end_track()

        Log["loadup"]["abstract"]["room"]("AbstractRoom loading complete")
        return cls._loaded

    def _get_save(self, function_memory:FunctionMemory):
        s = {
            "name": self.name,
            "events": self.events,
            "environment": self.environment,
            "interactions": self.interactions
        }
        if self.is_template:
            s.update({"template": True})
        return s

if __name__ == "__main__":
    print(AbstractRoom.loadData(None))