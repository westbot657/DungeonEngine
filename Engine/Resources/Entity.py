# pylint: disable=[W,R,C,import-error]


try:
    from .Location import Location
    from .Position import Position
except ImportError:
    from Location import Location
    from Position import Position


class Entity:
    
    def __init__(self, location:Location, position:Position):
        self.location = location
        self.position = position
    
    



