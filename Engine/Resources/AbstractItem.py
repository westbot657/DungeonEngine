# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
    from .Item import Item
    from .EngineErrors import InvalidObjectError
    from .DynamicValue import DynamicValue
    from .EngineDummy import Engine
    from .AbstractGameObject import AbstractGameObject
    from .Logger import Log
except ImportError:
    from Identifier import Identifier
    from Item import Item
    from EngineErrors import InvalidObjectError
    from DynamicValue import DynamicValue
    from EngineDummy import Engine
    from AbstractGameObject import AbstractGameObject
    from Logger import Log

import glob, json, re

class AbstractItem(AbstractGameObject):
    _loaded: dict = {}
    _link_parents: list = []
    identity: Identifier = Identifier("engine", "abstract/", "item")
    def __init__(self, identifier:Identifier, data:dict):
        Log["loadup"]["abstract"]["item"]("creating new AbstractItem")
        self.identifier = identifier
        self._raw_data = data

        self.parent: AbstractItem|None = None
        self.children: list[AbstractItem] = []

        if "parent" in data:
            AbstractItem._link_parents.append((self, data["parent"]))

        self.name: str = data.get("name", None)
        self.max_count: int = data.get("max_count", None)
        self.count: int = data.get("count", self.max_count)
        self.data: dict = data.get("data", None)

        self.is_template: bool = data.get("template", False)

    def _set_parent(self, parent):
        self.parent = parent
        parent.children.append(self)

    def getName(self) -> str:
        if self.name is None:
            n = self.parent.getName() if self.parent else None
        else:
            n = self.name
        if n is not None:
            return n
        raise InvalidObjectError(f"Item has no name! ({self.identifier})")

    def getMaxCount(self) -> int:
        if self.max_count is None:
            c = self.parent.getMaxCount() if self.parent is not None else None
        else:
            c = self.max_count
        if c is not None: return c
        raise InvalidObjectError(f"Item has no max_count! ({self.identifier})")

    def getCount(self) -> int:
        if self.count is None:
            c = self.parent.getCount() if self.parent else None
        else:
            c = self.count
        if c is not None: return c
        raise InvalidObjectError(f"Item has no count! ({self.identifier})")
    
    def getData(self) -> dict:
        if self.data is None:
            return self.parent.getData() or {} if self.parent else {}
        return self.data

    def createInstance(self, engine:Engine, **override_values) -> Item:
        if self.is_template:
            ...
        else:
            return Item(self,
                override_values.get("name", self.getName()),
                override_values.get("max_count", self.getMaxCount()),
                DynamicValue(override_values.get("count", self.getCount())).getCachedOrNew(engine),
                DynamicValue(override_values.get("data", self.getData()))
            )

    @classmethod
    def loadData(cls, inline_handler) -> list:
        files: list[str] = glob.glob("**/items/*.json", recursive=True)
        Log["loadup"]["abstract"]["item"](f"found {len(files)} item files")
        for file in files:
            file: str
            Log["loadup"]["abstract"]["item"](f"loading AbstractItem from '{file}'")
            with open(file, "r+", encoding="utf-8") as f:
                data = json.load(f)
            
            Id = Identifier.fromFile(file)
            cls._loaded.update({Id.full(): cls(Id, data)})

            # if m := re.match(r"Dungeons/(?P<namespace>[^/]+)/resources/(?P<path>(?:[^/]+/)+)(?P<name>[a-z0-9_]+)\.json", file):
            #     d: dict = m.groupdict()
            #     namespace:str = d["namespace"]
            #     path: str = d["path"]
            #     name: str = d["name"]
            #     cls._loaded.update({f"{namespace}:items/{name}": cls(Identifier(namespace, path, name), data)})

            # elif m := re.match(r"resources/items/(?P<name>[a-z0-9_]+)\.json", file):
            #     d: dict = m.groupdict()
            #     name: str = d["name"]
            #     cls._loaded.update({f"engine:items/{name}": cls(Identifier("engine", "resources/items/", name), data)})
        Log["loadup"]["abstract"]["item"]("linking AbstractItem parents...")
        for w, p in cls._link_parents:
            w: AbstractItem
            p: str
            if parent := cls._loaded.get(p, None):
                if parent is w:
                    Log["ERROR"]["loadup"]["abstract"]["item"]("cannot set object as it's own parent")
                    #cls._loaded.pop(w.identifier.full())
                    continue
                elif w in parent.get_parent_chain():
                    Log["ERROR"]["loadup"]["abstract"]["item"]("circular parent loop found")
                    #cls._loaded.pop(w.identifier.full())
                    #cls._loaded.pop(parent.identifier.full())
                    continue
                w._set_parent(parent)
            else:
                Log["ERROR"]["loadup"]["abstract"]["item"](f"parent does not exist: '{p}'")

        Log["loadup"]["abstract"]["item"]("verifying AbstractItem completion...")
        Log.track(len(cls._loaded), "loadup", "abstract", "item")
        for l, o in cls._loaded.copy().items():
            l: str
            o: AbstractItem
            if o.is_template:
                Log.success()
                continue
            try:
                o.getName()
                o.getMaxCount()
                o.getCount()
                o.getData()
                Log.success()
            except InvalidObjectError:
                e: AbstractItem = cls._loaded.pop(l)
                Log.fail()
                Log.ERROR("loadup", "abstract", "item", f"failed to load item: {e.identifier}")

        Log.end_track()

        Log["loadup"]["abstract"]["item"]("AbstractItem loading complete")
        return cls._loaded


if __name__ == "__main__":
    pass #print(AbstractItem.loadData())

