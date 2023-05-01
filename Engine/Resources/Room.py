# pylint: disable=[W,R,C,import-error]

try:
    from .FunctionalElement import FunctionalElement
    from .DynamicValue import DynamicValue
    from .Interactable import Interactable
    from .FunctionMemory import FunctionMemory
    from .Player import Player
    from .EngineOperation import _EngineOperation
    from .Location import Location
except ImportError:
    from FunctionalElement import FunctionalElement
    from DynamicValue import DynamicValue
    from Interactable import Interactable
    from FunctionMemory import FunctionMemory
    from Player import Player
    from EngineOperation import _EngineOperation
    from Location import Location

class Room(FunctionalElement):
    def __init__(self, abstract, location:Location, name:str, events:dict, interactions:list[Interactable]):
        self.abstract = abstract
        self.location = location
        self.name = name
        self.events = events
        self.interactions = interactions

    def getLocalVariables(self) -> dict:
        l = {
            ".name": self.name
        }
        for interaction in self.interactions:
            l.update({
                f".{interaction.}"
            })
    
    def updateLocalVariables(self, locals: dict):
        ...


    def prepFunctionMemory(self, function_memory:FunctionMemory):
        function_memory.addContextData({
            "#room": self
        })
        function_memory.update(self.getLocalVariables())
    
    def postEvaluate(self, function_memory:FunctionMemory):
        self.updateLocalVariables(function_memory.symbol_table)

    def onEnter(self, function_memory:FunctionMemory, player:Player):
        if (on_enter := self.events.get("on_enter", None)) is not None:
            self.prepFunctionMemory(function_memory)
            function_memory.addContextData({
                "#player": player
            })

            ev = function_memory.generatorEvaluateFunction(on_enter)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                v = e.value or (v if not isinstance(v, _EngineOperation) else None)
            res = v

            self.postEvaluate(function_memory)

    def onExit(self, function_memory:FunctionMemory, player:Player):
        if (on_exit := self.events.get("on_exit", None)) is not None:
            self.prepFunctionMemory(function_memory)
            function_memory.addContextData({
                "#player": player
            })

            ev = function_memory.generatorEvaluateFunction(on_exit)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                v = e.value or (v if not isinstance(v, _EngineOperation) else None)
            res = v

            self.postEvaluate(function_memory)

    def onInput(self, function_memory:FunctionMemory, player:Player, text:str):
        if (on_input := self.events.get("on_input", None)) is not None:
            self.prepFunctionMemory(function_memory)
            function_memory.addContextData({
                "#player": player,
                "#text": text
            })

            ev = function_memory.generatorEvaluateFunction(on_input)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                v = e.value or (v if not isinstance(v, _EngineOperation) else None)
            res = v

            self.postEvaluate(function_memory)
