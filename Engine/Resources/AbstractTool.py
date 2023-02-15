# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
    from .Tool import Tool
    from .EngineErrors import InvalidObjectError
    from .EngineDummy import Engine
    from .AbstractGameObject import AbstractGameObject
except ImportError:
    from Identifier import Identifier
    from Tool import Tool
    from EngineErrors import InvalidObjectError
    from EngineDummy import Engine
    from AbstractGameObject import AbstractGameObject

import glob, json

class AbstractTool(AbstractGameObject):
    _loaded = {}
    _link_parents = []

    identity: Identifier = Identifier("engine", "abstract/", "tool")
    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data
        self.children: list[AbstractTool] = []
        self.parent: AbstractTool|None = None

        self.is_template: bool = data.get("template", False)

    def _set_parent(self, parent):
        self.parent = parent
        parent.children.append(self)
    
    def createInstance(self, **override_values) -> Tool:
        if self.is_template:
            ...
        else:
            return Tool(self
            )
    
    @classmethod
    def loadData(cls, engine:Engine) -> list:
        files: list[str] = glob.glob("**/weapons/*.json", recursive=True)
        #print(files)
        for file in files:
            file: str
            with open(file, "r+", encoding="utf-8") as f:
                data = json.load(f)

            Id = Identifier.fromFile(file)
            cls._loaded.update({Id.full(): cls(Id, data)})

        for w, p in cls._link_parents:
            w: AbstractTool
            p: str
            w._set_parent(cls._loaded.get(p))

        for l, o in cls._loaded.copy().items():
            l: str
            o: AbstractTool
            try:
                ...
            except InvalidObjectError as err:
                e: AbstractTool = cls._loaded.pop(l)
                print(f"Failed to load tool: {e.identifier}  {err}")
                continue
            

        return cls._loaded

if __name__ == "__main__":
    print(AbstractTool.loadData(None))

