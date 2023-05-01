# pylint: disable=[W,R,C,import-error]

try:
    from .FunctionalElement import FunctionalElement
    from .FunctionMemory import FunctionMemory
    from .Environment import Environment
    from .Identifier import Identifier
    from .DynamicValue import DynamicValue
    from .Room import Room
    from .Player import Player
    from .EngineOperation import _EngineOperation
    from .ConsoleCommand import ConsoleCommand
    from .Logger import Log
    from .TextPattern import TextPattern
    from .EngineOperation import EngineOperation, _EngineOperation
    from .EngineErrors import EngineError, EngineBreak
    from .Location import Location
except ImportError:
    from FunctionalElement import FunctionalElement
    from FunctionMemory import FunctionMemory
    from Environment import Environment
    from Identifier import Identifier
    from DynamicValue import DynamicValue
    from Room import Room
    from Player import Player
    from EngineOperation import _EngineOperation
    from ConsoleCommand import ConsoleCommand
    from Logger import Log
    from TextPattern import TextPattern
    from EngineOperation import EngineOperation, _EngineOperation
    from EngineErrors import EngineError, EngineBreak
    from Location import Location

from typing import Generator

import json

class Dungeon(FunctionalElement):

    def __init__(self, abstract, name:str, version:int|float|str, environment:Environment, entry_point:Location, events:list, data:dict|None, rooms:list[Room]):
        self.abstract = abstract
        self.name = name
        self.version = version
        self.environment = environment
        self.entry_point = entry_point
        self.events = events
        self.data = data
        self.rooms = rooms

    def getLocalVariables(self) -> dict:
        d = {
            ".name": self.name,
            ".enviornment": self.environment,
            ".entry_point": self.entry_point,
        }
        for key, value in self.data:
            d.update({f".{key}": value})
        for room in self.rooms:
            d.update({f".{room.location.room}": room})
        return d
    
    def updateLocalVariables(self, locals: dict):
        ...

    def prepFunctionMemory(self, function_memory:FunctionMemory):
        function_memory.addContextData({
            "#dungeon": self
        })
        function_memory.update(self.getLocalVariables())

    def postEvaluate(self, function_memory:FunctionMemory):
        self.updateLocalVariables(function_memory.symbol_table)

    def loadSaveData(self, function_memory:FunctionMemory):
        ...

    def onEnter(self, function_memory:FunctionMemory, player:Player):
        player._text_pattern_categories = ["global", "common", "dungeon"]
        if (on_enter := self.events.get("on_enter", None)) is not None:
            self.prepFunctionMemory(function_memory)

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
        

    # def onInput(self, function_memory:FunctionMemory, player:Player, text:str):
    #     if (on_input := self.events.get("on_input", None)) is not None:
    #         self.prepFunctionMemory(function_memory)

    #         ev = function_memory.generatorEvaluateFunction(on_input)
    #         v = None
    #         try:
    #             v = ev.send(None)
    #             while isinstance(v, _EngineOperation):
    #                 res = yield v
    #                 v = ev.send(res)
    #         except StopIteration as e:
    #             v = e.value or (v if not isinstance(v, _EngineOperation) else None)
    #         res = v

    #         self.postEvaluate(function_memory)

    def onExit(self, function_memory:FunctionMemory, player:Player):
        player._text_pattern_categoris = ["global", "common", "world"]
        if (on_exit := self.events.get("on_exit", None)) is not None:
            self.prepFunctionMemory(function_memory)

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

    




