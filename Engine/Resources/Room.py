# pylint: disable=[W,R,C,import-error]

try:
    from .FunctionalElement import FunctionalElement
    from .DynamicValue import DynamicValue
    from .Interactable import Interactable
except ImportError:
    from FunctionalElement import FunctionalElement
    from DynamicValue import DynamicValue
    from .Interactable import Interactable

class Room(FunctionalElement):
    def __init__(self, abstract, name:str, enter_message:DynamicValue, exit_message:DynamicValue, interactions:list[Interactable]):
        self.abstract = abstract
        self.name = name
        self.enter_message = enter_message
        self.exit_message = exit_message
        self.interactions = interactions

    def getLocalVariables(self) -> dict:
        return {
            ".name": self.name,
            ".interaction": self.interactions
        }
    
    def updateLocalVariables(self, locals: dict):
        ...
