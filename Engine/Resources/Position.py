# pylint: disable=[W,R,C,import-error]

from .FunctionalElement import FunctionalElement
from .Serializer import Serializer, Serializable


@Serializable("Position")
class Position(FunctionalElement):

    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
    
    def serialize(self):
        return {
            "x": Serializer.serialize(self.x),
            "y": Serializer.serialize(self.y),
        }
    
    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)
    
    def copy(self):
        return Position(self.x, self.y)

    def __dict__(self):
        return {
            "%ENGINE:DATA-TYPE%": "Position",
            "x": self.x,
            "y": self.y
        }

    def _get_save(self, function_memory):
        return [self.x, self.y]
