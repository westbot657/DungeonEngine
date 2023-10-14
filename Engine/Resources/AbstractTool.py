# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
    from .Tool import Tool
    from .EngineErrors import InvalidObjectError
    from .EngineDummy import Engine
    from .AbstractGameObject import AbstractGameObject
    from .DynamicValue import DynamicValue
    from .Logger import Log
except ImportError:
    from Identifier import Identifier
    from Tool import Tool
    from EngineErrors import InvalidObjectError
    from EngineDummy import Engine
    from AbstractGameObject import AbstractGameObject
    from DynamicValue import DynamicValue
    from Logger import Log

import glob, json, random

class AbstractTool(AbstractGameObject):
    _loaded = {}
    _link_parents = []

    identity: Identifier = Identifier("engine", "abstract/", "tool")
    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data
        self.children: list[AbstractTool] = []
        self.parent: AbstractTool|None = None

        self.name: str|None = data.get("name", None)
        self.description: str|None = data.get("description", None)
        self.max_durability: int|None = data.get("max_durability", None)
        self.durability: int|None = data.get("durability", self.max_durability)
        self.events: dict|None = data.get("events", None)
        self.data: dict = data.get("data", {})

        self.keywords: list = data.get("keywords", None)

        self.is_template: bool = data.get("template", False)

    def _set_parent(self, parent):
        self.parent = parent
        parent.children.append(self)
    
    def getName(self):
        n = self.name or (self.parent.getName() if self.parent else None)
        if n is not None: return n
        raise InvalidObjectError(f"Tool has no name! ({self.identifier})")

    def getDescription(self):
        n = self.description or (self.parent.getDescription() if self.parent else None)
        if n is not None: return n
        return ""
        # raise InvalidObjectError(f"Tool has no name! ({self.identifier})")

    def getMaxDurability(self):
        if self.max_durability is None:
            d = self.parent.getMaxDurability() if self.parent else None
        else:
            d = self.max_durability
        if d is not None:
            return d
        raise InvalidObjectError(f"Tool has no max-durability! ({self.identifier})")

    def getDurability(self):
        if self.durability is None:
            d = self.parent.getDurability() if self.parent else None
        else:
            d = self.durability
        if d is not None:
            return d
        raise InvalidObjectError(f"Tool has no durability! ({self.identifier})")

    def getEvents(self) -> dict:
        if self.events:
            return self.events
        elif self.parent:
            return self.parent.getEvents()
        return {}

    def getData(self) -> dict:
        _data = {}
        if self.parent:
            _data.update(self.parent.getData())
        _data.update(self.data.copy())
        return _data

    def getKeywords(self) -> list:
        if self.keywords is None:
            if self.parent:
                words = self.parent.getKeywords()
                if "use" not in words: words.append("use")
                return words
            return ["use"]
        words = self.keywords.copy()
        if self.parent:
            words += [word for word in self.parent.getKeywords() if word not in words]
        return words

    def createInstance(self, function_memory, **override_values) -> Tool:
        if self.is_template:
            return random.choice(self.get_children()).createInstance(function_memory, **override_values)
            
        else:
            return Tool(self,
                DynamicValue(override_values.get("name", self.getName())).getNew(function_memory),
                DynamicValue(override_values.get("description", self.getDescription())).getNew(function_memory),
                DynamicValue(override_values.get("durability", self.getDurability())).getCachedOrNew(function_memory),
                override_values.get("max_durability", self.getMaxDurability()),
                self.getEvents(),
                self.getData()
            )
    
    @classmethod
    def loadData(cls, engine:Engine) -> list:
        files: list[str] = glob.glob("**/tools/*.json", recursive=True)
        #print(files)
        Log["loadup"]["abstract"]["tool"](f"found {len(files)} tool file{'s' if len(files) != 1 else ''}")
        for file in files:
            file: str
            Log["loadup"]["abstract"]["tool"](f"loading AbstractTool from '{file}'")
            with open(file, "r+", encoding="utf-8") as f:
                data = json.load(f)

            Id = Identifier.fromFile(file)
            cls._loaded.update({Id.full(): cls(Id, data)})

        Log["loadup"]["abstract"]["tool"]("linking AbstractTool parents...")
        for a, p in cls._link_parents:
            a: AbstractTool
            p: str
            if parent := cls._loaded.get(p, None):
                if parent is a:
                    Log["ERROR"]["loadup"]["abstract"]["tool"]("cannot set object as it's own parent")
                    continue
                elif parent in a.get_parent_chain():
                    Log["ERROR"]["loadup"]["abstract"]["tool"]("circular parent loop found")
                    continue
                a._set_parent(parent)
            else:
                Log["ERROR"]["loadup"]["abstract"]["tool"](f"parent does not exist: '{p}'")

        Log["loadup"]["abstract"]["tool"]("verifying AbstractTool completion...")
        Log.track(len(cls._loaded), "loadup", "abstract", "tool")
        for l, o in cls._loaded.copy().items():
            l: str
            o: AbstractTool

            if o.is_template:
                Log.success()
                continue
            try:
                o.getName()
                o.getMaxDurability()
                o.getDurability()
                Log.success()
            except InvalidObjectError as err:
                e: AbstractTool = cls._loaded.pop(l)
                Log.ERROR("loadup", "abstract", "tool", f"failed to load tool: {e.identifier}")

        Log.end_track()

        cls._link_parents.clear()

        Log["loadup"]["abstract"]["tool"]("AbstractTool loading complete")
        return cls._loaded

if __name__ == "__main__":
    print(AbstractTool.loadData(None))

