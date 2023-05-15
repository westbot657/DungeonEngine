# pylint: disable=[W,R,C,import-error]

try:
    from .Entity import Entity
    from .Identifier import Identifier
    from .Location import Location
    from .EngineDummy import Engine
    from .Position import Position
    from .FunctionMemory import FunctionMemory
    from .Util import Util
    from .AbstractAttack import AbstractAttack, Attack
except:
    from Entity import Entity
    from Identifier import Identifier
    from Location import Location
    from EngineDummy import Engine
    from Position import Position
    from FunctionMemory import FunctionMemory
    from Util import Util
    from AbstractAttack import AbstractAttack, Attack

class Enemy(Entity):
    
    def __init__(self, abstract, name:str, max_health:int, health:int, attacks:list, location:Location, position:Position):
        self.abstract = abstract
        self.name = name
        self.max_health = max_health
        self.health = health
        self.attacks = attacks
        super().__init__(location, position)


    def quickStats(self, function_memory:FunctionMemory):
        return f"{self.name}  {Util.getDurabilityBar(self.health, self.max_health)}"

    def fullStats(self, function_memory:FunctionMemory):
        s = [f"{self.name}  {Util.getDurabilityBar(self.health, self.max_health)}"]

        for attack in self.attacks:
            attack: Attack
            s.append(f"  {attack.quickStats(function_memory)}")

    def _get_save(self, function_memory:FunctionMemory) -> dict:
        return {}



