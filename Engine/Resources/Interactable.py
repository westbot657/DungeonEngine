# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
    from .DynamicValue import DynamicValue
    from .FunctionalElement import FunctionalElement
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier
    from DynamicValue import DynamicValue
    from FunctionalElement import FunctionalElement

from typing import Any

class Interactable(FunctionalElement):
    
    def __init__(self, abstract, field_values:dict):
        self.abstract = abstract

        self.field_values = field_values


    def getLocalVariables(self):
        vals = {}
        for field_name, field_data in self.field_values.items():
            vals.update({f".{field_name}": field_data["value"]})
        return vals

    def updateLocalVariables(self, function_memory, locals:dict):
        for field_name, field_data in self.field_values.items():
            field_name: str
            field_data: dict
            field_value: Any = field_data["value"]
            field_type: str = field_data["type"]

            

            

