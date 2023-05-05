# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
    from .Util import Util
    from .EngineDummy import Engine
    from .EngineOperation import EngineOperation, _EngineOperation
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier
    from Util import Util
    from EngineDummy import Engine
    from EngineOperation import EngineOperation, _EngineOperation

class Item(GameObject):
    identifier = Identifier("engine", "object/", "item")
    def __init__(self, abstract, name:str, max_count:int, count:int, data:dict|None=None):
        self.abstract = abstract
        self.name = name
        self.max_count = max_count
        self.count = count
        self.data = data or {}

        self.owner = None

    def checkKeyword(self, keyword):
        return keyword in self.abstract.getKeywords()

    def onUse(self, function_memory, amount_used:int):
        if on_use := self.events.get("on_use", None):
            function_memory.addContextData({
                "#tool": self
            })
            ev = function_memory.generatorEvaluateFunction(on_use)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                v = e.value or (v if not isinstance(v, _EngineOperation) else None)
            res = v

    def __repr__(self):
        return f"Item {self.name}: max_count:{self.max_count} count:{self.count} data:{self.data}"

    def fullStats(self, engine, _):
        return f"{self.name}  {self.count}/{self.max_count}"

    def quickStats(self, engine):
        return f"{self.name}  {self.count}/{self.max_count}"
    