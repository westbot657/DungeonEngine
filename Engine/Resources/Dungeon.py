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

import json, os

class Dungeon(FunctionalElement):

    def __init__(self, abstract, name:str, version:int|float|str, environment:Environment, entry_point:Location, events:list, data:dict|None, rooms:dict[str, Room]):
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
        for room in self.rooms.values():
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

    def loadData(self, function_memory:FunctionMemory):
        filename = f"./Engine/save_data/{self.abstract.identifier.name}.json"

        if os.path.exists(filename):
            with open(filename, "r+", encoding="utf-8") as f:
                data = json.load(f)
            
            if (dungeon := data.get("dungeon", None)) is not None:
                if (name := dungeon.get("name", None)) is not None:
                    self.name = name
                if (version := dungeon.get("verison", None)) is not None:
                    self.version = version
                if (environemt := dungeon.get("environment", None)) is not None:
                    self.environment = Environment(environemt)
                if (entry_point := dungeon.get("entry_point", None)) is not None:
                    self.entry_point = Location.fromString(entry_point)
                if (data := dungeon.get("data", None)) is not None:
                    _data = {}
                    for key, value in data:
                        _data.update({key: function_memory.rebuildData(value)})
                    self.data = _data


    def saveData(self, function_memory:FunctionMemory):
        filename = f"./Engine/save_data/{self.abstract.identifier.name}.json"
        data = {}
        _dat = self.abstract._get_save(function_memory)
        dat = {}
        # for val_name, abstract_val in _dat.items():
        #     current_val = getattr(self, val_name)
        #     if current_val != abstract_val:
        #         dat.update({val_name: current_val})
        
        if (name := _dat.get("name", None)) is not None:
            if name != self.name:
                dat.update({"name": self.name})

        if (version := _dat.get("version", None)) is not None:
            if version != self.version:
                dat.update({"version": self.version})

        if (environment := _dat.get("environment", None)) is not None:
            if self.environment != environment:
                dat.update({"environment": self.environment._get_save(function_memory)})
            
        if (entry_point := _dat.get("entry_point", None)) is not None:
            if self.entry_point.full() != entry_point:
                dat.update({"entry_point": self.entry_point})
        
        if (_data := _dat.get("data", None)) is not None:
            _data_save = {}
            for data_name, current_val in self.data.items():
                if (abstract_val := _data.get(data_name, None)) is not None:
                    if abstract_val != current_val:
                        _data_save.update({data_name: function_memory.getSaveData(current_val)})
                else:
                    _data_save.update({data_name: function_memory.getSaveData(current_val)})
            if _data_save:
                dat.update({"data": _data_save})

        if dat:
            data.update({"dungeon": dat})

        rooms = {}

        for room in self.rooms:
            room: Room
            room._save_to(function_memory, rooms)

        if rooms:
            data.update({"rooms": rooms})

        if data:
            with open(filename, "w+", encoding="utf-8") as f:
                json.dump(data, f)
        

    def onEnter(self, function_memory:FunctionMemory, player:Player):
        player._text_pattern_categories = ["global", "common", "dungeon"]
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

        entrance: Room = self.rooms.get(self.entry_point.full())

        ev = entrance.onEnter(function_memory, player)
        v = None
        try:
            v = ev.send(None)
            while isinstance(v, (_EngineOperation, Generator)):
                res = yield v
                v = ev.send(res)
        except StopIteration as e:
            pass#v = e.value or v
        


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

    




