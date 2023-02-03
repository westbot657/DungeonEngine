

try:
    from .Location import Location
except ImportError:
    from Location import Location


class Entity:
    
    def __init__(self, location:Location):
        self.location = location
    
    



