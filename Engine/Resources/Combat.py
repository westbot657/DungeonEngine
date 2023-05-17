# pylint: disable=[W,R,C,import-error]

try:
    from .AbstractEnemy import AbstractEnemy, Enemy
    from .FunctionMemory import FunctionMemory
    from .Player import Player
except ImportError:
    from AbstractEnemy import AbstractEnemy, Enemy
    from FunctionMemory import FunctionMemory
    from Player import Player



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
            def __init__(self):
                super().__init__("UniqueName")
        
        class NumberedName(_Operation):
            def __init__(self):
                super().__init__("NumberedName")

    class Task:
        def __init__(self, task, delay:int):
            self.task = task
            self.delay = delay

    def __init__(self, abstract, enemies:list[Enemy], sequence:dict, data:dict):
        self.abstract = abstract
        self.enemies = enemies
        self.sequence = sequence
        self.data = data
        self.players = []
        self.scheduled_tasks: list[Combat.Task] = []
        self.tick = None

    def addPlayer(self, player:Player):
        player._combat = self
        self.players.append(player)

    def removePlayer(self, player:Player):
        player._combat = None
        if player in self.players:
            self.players.remove(player)

    def onInput(self, player:Player, text:str):
        ...

    def start(self, function_memory:FunctionMemory):
        self.tick = self._mainloop(function_memory)
        self.tick.send(None)
        function_memory.engine.combats.append(self)

    def _mainloop(self, function_memory:FunctionMemory):
        result = yield None
        remove = []
        while True:
            if result == None:
                result = yield None
                continue

            remove.clear()
            for task in self.scheduled_tasks:
                task: Combat.Task
                task.delay -= 1

                if task.delay <= 0:
                    remove.append(task)
                    task.task(self, function_memory)



            for task in remove: self.scheduled_tasks.remove(task)

            result = yield None
    


