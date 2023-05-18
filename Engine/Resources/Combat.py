# pylint: disable=[W,R,C,import-error]

try:
    from .AbstractEnemy import AbstractEnemy, Enemy
    from .FunctionMemory import FunctionMemory
    from .FunctionalElement import FunctionalElement
    from .Player import Player
    from .EngineErrors import CombatError
except ImportError:
    from AbstractEnemy import AbstractEnemy, Enemy
    from FunctionMemory import FunctionMemory
    from FunctionalElement import FunctionalElement
    from Player import Player
    from EngineErrors import CombatError

from enum import Enum, auto

import random


class Combat(FunctionalElement):

    class JoinPriority(Enum):
        NEXT = auto()
        LAST = auto()
        RANDOM = auto()

    class Operation:
        class _Operation:
            def __init__(self, name:str, ):
                self.name = name
        
        class Message(_Operation):
            def __init__(self, message:str):
                super().__init__("Message")
                self.message = message

        class Spawn(_Operation):
            def __init__(self, enemies:list[Enemy], ):
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



        class _EnemyAttack(_Operation):
            def __init__(self, enemy:Enemy, target:Player):
                super().__init__("EnemyAttack")
                self.enemy = enemy
                self.target = target

        class _HandleInput(_Operation):
            def __init__(self, player:Player, text:str):
                super().__init__("HandleInput")
                self.player = player
                self.text = text

        class _HandlePlayerJoin(_Operation):
            def __init__(self, player:Player, ):
                super().__init__("HandlePlayerJoin")
                self.player = player
        
        class _HandlePlayerLeave(_Operation):
            def __init__(self, player:Player):
                super().__init__("HandlePlayerLeave")
                self.player = player

        class _NextTurn(_Operation):
            def __init__(self):
                super().__init__("NextTurn")

    class Task:
        def __init__(self, task, delay:int):
            self.task = task
            self.delay = delay

    def __init__(self, abstract, enemies:list[Enemy], sequence:dict, data:dict):
        self.abstract = abstract
        self.enemies: list[Enemy] = enemies
        self.sequence: dict = sequence
        self.data: dict = data
        self.players: list[Player] = []
        self.turn_order: list[Player|Enemy] = []
        self.current_turn: int = 0
        self.scheduled_tasks: list[Combat.Task] = []
        self.tick = None
        self.turn = None
        self.last_trigger = None

    def getLocalVariables(self) -> dict:
        d = {}
        return d

    def updateLocalVariables(self, locals: dict):
        ...
    
    def prepFunctionMemory(self, function_memory:FunctionMemory):
        function_memory.addContextData({
            "#combat": self
        })
        function_memory.update(self.getLocalVariables())
    
    def postEvaluate(self, function_memory:FunctionMemory):
        self.updateLocalVariables(function_memory.symbol_table)

    def addPlayer(self, player:Player):
        player._combat = self
        self.players.append(player)
        self.scheduled_tasks.insert(0, Combat.Task(Combat.Operation._HandlePlayerJoin(player), 0))

    def removePlayer(self, player:Player):
        self.scheduled_tasks.insert(0, Combat.Task(Combat.Operation._HandlePlayerLeave(player), 0))
        player._combat = None
        if player in self.players:
            self.players.remove(player)

    def onInput(self, player:Player, text:str):
        self.scheduled_tasks.insert(0, Combat.Task(Combat.Operation._HandleInput(player, text), 0))

    def start(self, function_memory:FunctionMemory):
        self.tick = self._mainloop(function_memory)
        self.tick.send(None)
        function_memory.engine.combats.append(self)

    def handleOperation(self, function_memory:FunctionMemory, operation):
        match operation:
            case Combat.Operation._HandlePlayerJoin():
                self.turn_order.insert(self.current_turn+1, operation.player)
            case Combat.Operation._HandlePlayerLeave():
                self.turn_order.remove(operation.player)
            case Combat.Operation._HandleInput():
                ...
            case Combat.Operation._EnemyAttack():
                ...
            case Combat.Operation.Trigger():
                ...
            case Combat.Operation.Spawn():
                for enemy in operation.enemies:
                    ...
            case Combat.Operation.Message():
                ...
            case Combat.Operation._NextTurn():
                self.current_turn += 1
                if self.current_turn >= len(self.turn_order):
                    self.current_turn = 0
            case _:
                raise CombatError(f"Unrecognized combat operation: '{operation}'")

    def _mainloop(self, function_memory:FunctionMemory):
        result = yield None

        while True:
            if result == None:
                result = yield None
                continue

            for task in self.scheduled_tasks.copy():
                task: Combat.Task
                task.delay -= 1
                if task.delay <= 0:
                    self.scheduled_tasks.remove(task)
                    op = task.task

                    try:
                        self.handleOperation(function_memory, op)
                    except CombatError as e:
                        print(e)

            if self.last_trigger is None:
                if (start := self.sequence.get("@start", None)) is not None:
                    self.prepFunctionMemory(function_memory)

                    ...

            result = yield None
    


