# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
    from .Item import Item
    from .EngineErrors import InvalidObjectError
except ImportError:
    from Identifier import Identifier
    from Item import Item
    from EngineErrors import InvalidObjectError

import glob, json, re

class AbstractItem:
    _loaded: dict = {}
    _link_parents: list = []

    def __init__(self, identifier:Identifier, data:dict):
        
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
            c = self.parent.getMaxCount() if self.parent else None
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

    def createItem(self, **override_values) -> Item:
        return Item(
            override_values.get("name", self.getName()),
            override_values.get("max_count", self.getMaxCount()),
            override_values.get("count", self.getCount()),
            override_values.get("data", self.getData())
        )


    @classmethod
    def loadData(cls) -> list:
        files: list[str] = glob.glob("**/items/*.json", recursive=True)
        for file in files:
            file: str
            with open(file, "r+", encoding="utf-8") as f:
                data = json.load(f)

            if m := re.match(r"Dungeons/(?P<namespace>[^/]+)/resources/(?P<path>(?:[^/]+/)+)(?P<name>[a-z0-9_]+)\.json", file):
                d: dict = m.groupdict()
                namespace:str = d["namespace"]
                path: str = d["path"]
                name: str = d["name"]
                cls._loaded.update({f"{namespace}:items/{name}": cls(Identifier(namespace, path, name), data)})

            elif m := re.match(r"resources/items/(?P<name>[a-z0-9_]+)\.json", file):
                d: dict = m.groupdict()
                name: str = d["name"]
                cls._loaded.update({f"engine:items/{name}": cls(Identifier("engine", "resources/items/", name), data)})

        for w, p in cls._link_parents:
            w: AbstractItem
            p: str
            w._set_parent(cls._loaded.get(p))

        for l, o in cls._loaded.copy().items():
            l: str
            o: AbstractItem
            try:
                o.getName()
                o.getMaxCount()
                o.getCount()
                o.getData()
            except InvalidObjectError:
                e: AbstractItem = cls._loaded.pop(l)
                print(f"Failed to load item: {e.identifier}")

        return cls._loaded


if __name__ == "__main__":
    print(AbstractItem.loadData())

