# pylint: disable=[W,R,C,import-error]

try:
    from .FunctionalElement import FunctionalElement
    from .FunctionMemory import FunctionMemory
    from .Environment import Environment
    from .Identifier import Identifier
    from .DynamicValue import DynamicValue
    from .Room import Room
except ImportError:
    from FunctionalElement import FunctionalElement
    from FunctionMemory import FunctionMemory
    from Environment import Environment
    from Identifier import Identifier
    from DynamicValue import DynamicValue
    from Room import Room

import json

class Dungeon(FunctionalElement):

    def __init__(self, abstract, name:str, version:int|float|str, environment:Environment, entry_point:Identifier, enter_message:DynamicValue, exit_message:DynamicValue, data:dict|None, rooms:list[Room]):
        self.abstract = abstract
        self.name = name
        self.version = version
        self.environment = environment
        self.entry_point = entry_point
        self.enter_message = enter_message
        self.exit_message = exit_message
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
            ...
        return d
    
    def updateLocalVariables(self, locals: dict):
        ...

    def loadSaveData(self, function_memory:FunctionMemory):
        ...

    def _input_handler(self, player_id, text:str):
        ...


