# pylint: disable=[W,R,C,import-error]

try:
    from .AbstractEnemy import AbstractEnemy, Enemy
    from .FunctionMemory import FunctionMemory
except ImportError:
    from AbstractEnemy import AbstractEnemy, Enemy
    from FunctionMemory import FunctionMemory



from enum import Enum, auto


class Combat:

    class Operation:
        class _Operation:
            def __init__(self, name:str, ):
                self.name = name
        
        class Message(_Operation):
            def __init__(self, message:str):
                super().__init__("Message")
                self.message = message

        class Spawn(_Operation):
            def __init__(self, enemies:list[Enemy]):
                super().__init__("Spawn")
                self.enemies = enemies

        class Trigger(_Operation):
            def __init__(self, event_name:str):
                super().__init__("Trigger")
                self.event_name = event_name

        class UniqueName(_Operation):
            def __init__(self, enemy:Enemy):
                super().__init__("UniqueName")
                self.enemy = enemy
        
        class NumberedName(_Operation):
            def __init__(self, enemy:Enemy):
                super().__init__("NumberedName")
                self.enemy = enemy


    class Style(Enum):
        SEQUENCED = auto()
        BASIC = auto()

    def __init__(self, abstract, enemies:list[Enemy], sequence:dict, data:dict):
        self.abstract = abstract
        self.enemies = enemies
        self.sequence = sequence
        self.data = data

        self.players = []

    
    


