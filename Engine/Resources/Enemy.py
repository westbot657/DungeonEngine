# pylint: disable=[W,R,C,import-error]

try:
    from .Entity import Entity
    from .Identifier import Identifier
    from .Location import Location
    from .EngineDummy import Engine
    from .Position import Position
    from .FunctionMemory import FunctionMemory
    from .Util import Util
    from .AbstractAttack import AbstractAttack, Attack
    from .EngineOperation import _EngineOperation
except:
    from Entity import Entity
    from Identifier import Identifier
    from Location import Location
    from EngineDummy import Engine
    from Position import Position
    from FunctionMemory import FunctionMemory
    from Util import Util
    from AbstractAttack import AbstractAttack, Attack
    from EngineOperation import _EngineOperation

class Enemy(Entity):
    
    def __init__(self, abstract, name:str, max_health:int, health:int, attacks:list, location:Location, position:Position):
        self.abstract = abstract
        self.name = name
        self.max_health = max_health
        self.health = health
        self.attacks = attacks
        self.uid = None
        super().__init__(location, position)
        self.events = {}

    def getLocalVariables(self) -> dict:
        d = {}

        return d

    def updateLocalVariables(self, locals: dict):
        ...
    
    def prepFunctionMemory(self, function_memory:FunctionMemory):
        function_memory.addContextData({
            "#enemy": self
        })
        function_memory.update(self.getLocalVariables())
    
    def postEvaluate(self, function_memory:FunctionMemory):
        self.updateLocalVariables(function_memory.symbol_table)

    def quickStats(self, function_memory:FunctionMemory):
        return f"{self.name}  {Util.getDurabilityBar(self.health, self.max_health)}"

    def fullStats(self, function_memory:FunctionMemory):
        s = [f"{self.name}  {Util.getDurabilityBar(self.health, self.max_health)}"]

        for attack in self.attacks:
            attack: Attack
            s.append(f"  {attack.quickStats(function_memory)}")

        return "\n".join(s)

    def onEvent(self, function_memory:FunctionMemory, current_trigger:str, event_name:str):
        if current_trigger in self.events:
            if (event := self.events[current_trigger].get(event_name, None)):
                self.prepFunctionMemory(function_memory)

                ev = function_memory.generatorEvaluateFunction(event)
                v = None
                try:
                    v = ev.send(None)
                    while isinstance(v, _EngineOperation):
                        res = yield v
                        v = ev.send(res)
                except StopIteration as e:
                    v = e.value or (v if not isinstance(v, _EngineOperation) else None)
                return v

    def _get_save(self, function_memory:FunctionMemory) -> dict:
        return {}



