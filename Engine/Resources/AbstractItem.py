# pylint: disable=[W,R,C,import-error]

from Identifier import Identifier
from Item import Item
from EngineErrors import InvalidObjectError
from DynamicValue import DynamicValue
from EngineDummy import Engine
from AbstractGameObject import AbstractGameObject
from Logger import Log
from Loader import Loader
from Serializer import Serializer, Serializable

import glob, json, re, random
from mergedeep import merge

@Serializable("AbstractItem")
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
        self.description: str|None = data.get("description", None)
        self.max_count: int = data.get("max_count", None)
        self.count: int = data.get("count", self.max_count)
        self.data: dict = data.get("data", {})
        self.events: dict = data.get("events", {})
        self.keywords: list = data.get("keywords", None)

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

    def getDescription(self) -> str:
        if self.description is None:
            n = self.parent.getDescription() if self.parent else None
        else:
            n = self.description
        if n is not None:
            return n
        return ""
        # raise InvalidObjectError(f"Item has no name! ({self.identifier})")

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

    def getEvents(self) -> dict:
        return merge({}, self.parent.getEvents() if self.parent else {}, self.events)

    def createInstance(self, function_memory, **override_values) -> Item:
        if self.is_template:
            return random.choice(self.get_children()).createInstance(function_memory, **override_values)
        else:
            return Item(self,
                DynamicValue(override_values.get("name", self.getName())).getNew(function_memory),
                DynamicValue(override_values.get("description", self.getDescription())).getNew(function_memory),
                int(override_values.get("max_count", self.getMaxCount())),
                int(DynamicValue(override_values.get("count", self.getCount())).getCachedOrNew(function_memory)),
                override_values.get("data", self.getData()),
                self.getEvents()
            )

    @classmethod
    def loadData(cls, engine) -> list:
        files: list[str] = glob.glob("**/items/*.json", recursive=True)
        Log["loadup"]["abstract"]["item"](f"found {len(files)} item files")
        for file in files:
            file: str
            Log["loadup"]["abstract"]["item"](f"loading AbstractItem from '{file}'")
            data = Loader.load(file)
            
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
                o.getKeywords()
                Log.success()
            except InvalidObjectError:
                e: AbstractItem = cls._loaded.pop(l)
                Log.fail()
                Log.ERROR("loadup", "abstract", "item", f"failed to load item: {e.identifier}")

        Log.end_track()

        cls._link_parents.clear()

        Log["loadup"]["abstract"]["item"]("AbstractItem loading complete")
        return cls._loaded

    def serialize(self):
        return {
            "identifier": Serializer.serialize(self.identifier),
            "_raw_data": Serializer.serialize(self._raw_data),
            "parent": Serializer.serialize(self.parent),
            "children": Serializer.serialize(self.children),
            "name": Serializer.serialize(self.name),
            "description": Serializer.serialize(self.description),
            "max_count": Serializer.serialize(self.max_count),
            "count": Serializer.serialize(self.count),
            "data": Serializer.serialize(self.data),
            "events": Serializer.serialize(self.events),
            "keywords": Serializer.serialize(self.keywords),
            "is_template": Serializer.serialize(self.is_template)
        }

    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)

if __name__ == "__main__":
    pass #print(AbstractItem.loadData())

