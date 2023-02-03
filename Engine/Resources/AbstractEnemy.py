# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
    from .EngineErrors import InvalidObjectError
    from .EngineDummy import Engine
    from .Enemy import Enemy
except ImportError:
    from Identifier import Identifier
    from EngineErrors import InvalidObjectError
    from EngineDummy import Engine
    from Enemy import Enemy

import glob, json

class AbstractEnemy:
    _loaded: dict = {}
    _link_parents: list = []
    
    def __init__(self, identifier:Identifier, data:dict):
        ...
    
    @classmethod
    def loadData(cls, engine:Engine) -> list:
        files: list[str] = glob.glob("**/enemies/*.json", recursive=True)
        #print(files)
        for file in files:
            file: str
            with open(file, "r+", encoding="utf-8") as f:
                data = json.load(f)

            Id = Identifier.fromFile(file)
            cls._loaded.update({Id.full(): cls(Id, data)})

        for w, p in cls._link_parents:
            w: AbstractEnemy
            p: str
            w._set_parent(cls._loaded.get(p))

        for l, o in cls._loaded.copy().items():
            l: str
            o: AbstractEnemy
            try:
                ...
            except InvalidObjectError as err:
                e: AbstractEnemy = cls._loaded.pop(l)
                print(f"Failed to load enemy: {e.identifier}  {err}")

        return cls._loaded






