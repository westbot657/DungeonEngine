# pylint: disable=[W,R,C,import-error]

try:
    from .Serializer import Serializer, Serializable
except ImportError:
    from Serializer import Serializer, Serializable


@Serializable("Region")
class Region:
    
    def __init__(self, x:int, y:int, width:int, height:int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def serialize(self):
        return {
            "x": Serializer.serialize(self.x),
            "y": Serializer.serialize(self.y),
            "width": Serializer.serialize(self.width),
            "height": Serializer.serialize(self.height)
        }        
        
    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)
