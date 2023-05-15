# pylint: disable=[W,R,C,import-error]

try:
    from .Entity import Entity
    from .Identifier import Identifier
    from .Location import Location
    from .EngineDummy import Engine
    from .Position import Position
    from .FunctionMemory import FunctionMemory
except:
    from Entity import Entity
    from Identifier import Identifier
    from Location import Location
    from EngineDummy import Engine
    from Position import Position
    from FunctionMemory import FunctionMemory

class Enemy(Entity):
    
    def __init__(self, abstract, name:str, max_health:int, health:int, attacks:list, location:Location, position:Position):
        self.abstract = abstract
        self.name = name
        self.max_health = max_health
        self.health = health
        self.attacks = attacks
        super().__init__(location, position)



    def fullStats(self, function_memory:FunctionMemory):
        ...

    def _get_save(self, function_memory:FunctionMemory) -> dict:
        return {}



