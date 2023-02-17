# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
    from .EngineDummy import Engine
    from .Util import Util
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier
    from EngineDummy import Engine
    from Util import Util

class Tool(GameObject):
    identifier = Identifier("engine", "object/", "tool")
    def __init__(self, abstract, name:str, durability:int, max_durability:int, events:dict):
        self.abstract = abstract
        self.name = name
        self.durability = durability
        self.max_durability = max_durability
        self.events = events

    def on_use(self, engine:Engine):
        if func := self.events.get("on_use", None):
            engine.evaluateFunction(func)



    def __repr__(self):
        return f"Tool: {self.name} {self.durability}/{self.max_durability}"

    def fullStats(self, is_equipped=False):
        return f"{self.name} {Util.getDurabilityBar(self.durability, self.max_durability)}" + (" EQUIPPED" if is_equipped else "")

    def quickStats(self):
        return f"{self.name} {Util.getDurabilityBar(self.durability, self.max_durability)}"



