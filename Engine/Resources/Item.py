# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier

class Item(GameObject):
    identifier = Identifier("engine", "object/", "item")
    def __init__(self, abstract, name:str, max_count:int, count:int, data:dict|None=None):
        self.abstract = abstract
        self.name = name
        self.max_count = max_count
        self.count = count
        self.data = data or {}

    def __repr__(self):
        return f"Item {self.name}: max_count:{self.max_count} count:{self.count} data:{self.data}"

