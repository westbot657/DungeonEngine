# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
    from .DynamicValue import DynamicValue
    from .FunctionalElement import FunctionalElement
    from .FunctionMemory import FunctionMemory
    from .Player import Player
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier
    from DynamicValue import DynamicValue
    from FunctionalElement import FunctionalElement
    from FunctionMemory import FunctionMemory
    from Player import Player

from typing import Any

class Interactable(FunctionalElement):
    
    def __init__(self, abstract, field_values:dict):
        self.abstract = abstract
        self.field_values = field_values
        self.name = self.field_values.pop("id")

    def getLocalVariables(self):
        vals = {}
        for field_name, field_data in self.field_values.items():
            vals.update({f".{field_name}": field_data["value"]})
        return vals

    def updateLocalVariables(self, locals:dict):
        for field_name, field_data in self.field_values.items():
            field_name: str
            field_data: dict
            field_value: Any = field_data["value"]
            field_type: str = field_data["type"]

    def prepFunctionMemory(self, function_memory:FunctionMemory):
        function_memory.update(self.getLocalVariables())
    
    def postEvaluate(self, function_memory:FunctionMemory):
        self.updateLocalVariables(function_memory.symbol_table)
    

    def onInteract(self, function_memory:FunctionMemory, player:Player):
        ...

            

