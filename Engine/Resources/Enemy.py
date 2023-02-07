
try:
    from .Entity import Entity
    from .Identifier import Identifier
    from .Location import Location
    from .EngineDummy import Engine
except:
    from Entity import Entity
    from Identifier import Identifier
    from Location import Location
    from EngineDummy import Engine

class Enemy(Entity):
    ...
    
    def __init__(self, abstract, name:str, max_health:int, health:int, attacks:list):
        self.abstract = abstract
        self.name = name
        self.max_health = max_health
        self.health = health
        self.attacks = attacks



