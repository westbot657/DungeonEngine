# pylint: disable=[W,R,C,import-error]


try:
    from .Location import Location
    from .Position import Position
    from .FunctionalElement import FunctionalElement
except ImportError:
    from Location import Location
    from Position import Position
    from FunctionalElement import FunctionalElement


class Entity(FunctionalElement):
    
    def __init__(self, location:Location, position:Position):
        self.location = location
        self.position = position
    
    



