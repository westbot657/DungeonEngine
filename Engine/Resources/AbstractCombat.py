# pylint: disable=[W,R,C,import-error]

try:
    from .Combat import Combat
    from .Identifier import Identifier
except ImportError:
    from Combat import Combat
    from Identifier import Identifier

import glob, json, re


class AbstractCombat:
    _loaded: dict = {}

    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data
        
    @classmethod
    def loadData(cls) -> list:
        files: list[str] = glob.glob("**/combats/*.json", recursive=True)

        for file in files:
            file: str
            with open(file, "r+", encoding="utf-8") as f:
                data = json.load(f)
            
            if m := re.match(r"Dungeons/(?P<namespace>[^/]+)/resources/(?P<path>(?:[^/]+/)+)(?P<name>[a-z0-9_]+)\.json", file):
                d: dict = m.groupdict()
                namespace:str = d["namespace"]
                path: str = f"Dungeons/{namespace}/resources/{d['path']}"
                name: str = d["name"]
                cls._loaded.update({f"{namespace}:combats/{name}": cls(Identifier(namespace, path, name), data)})

            elif m := re.match(r"resources/combats/(?P<name>[a-z0-9_]+)\.json", file):
                d: dict = m.groupdict()
                name: str = d["name"]
                cls._loaded.update({f"engine:combats/{name}": cls(Identifier("engine", "resources/combats/", name), data)})


        return cls._loaded


