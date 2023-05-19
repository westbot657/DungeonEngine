# pylint: disable=[W,R,C,import-error]

try:
    from .AbstractEnemy import AbstractEnemy, Enemy
    from .FunctionMemory import FunctionMemory
    from .FunctionalElement import FunctionalElement
    from .Player import Player
    from .EngineErrors import CombatError
    from .EngineOperation import EngineOperation, _EngineOperation
    from .TextPattern import TextPattern
    from .Util import Util
except ImportError:
    from AbstractEnemy import AbstractEnemy, Enemy
    from FunctionMemory import FunctionMemory
    from FunctionalElement import FunctionalElement
    from Player import Player
    from EngineErrors import CombatError
    from EngineOperation import EngineOperation, _EngineOperation
    from TextPattern import TextPattern
    from Util import Util

from enum import Enum, auto

import random, re, json


class Combat(FunctionalElement):

    with open("../resources/combat.json", "r+", encoding="utf-8") as f:
        _combat_config = json.load(f)

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
            def __init__(self, enemies:list[str], priority):
                priority: Combat.JoinPriority
                super().__init__("Spawn")
                self.enemies = enemies
                self.priority = priority

        class Despawn(_Operation):
            def __init__(self, enemies:list[str]):
                super().__init__("Despawn")
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

        class DelayedAction(_Operation):
            def __init__(self, action):
                super().__init__("DelayedAction")
                self.action = action

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
            def __init__(self, player:Player, priority):
                priority: Combat.JoinPriority
                super().__init__("HandlePlayerJoin")
                self.player = player
                self.priority = priority
        
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
        self.input_requests = [] # may not need?
        self.function_memory = None
        self.combat_config = Util.deepCopy(self._combat_config)

    def getEnemy(self, enemy_id:str):
        for enemy in self.enemies:
            if enemy.uid == enemy_id:
                return enemy

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
        player.in_combat = True
        player._combat = self
        self.players.append(player)
        self.scheduled_tasks.insert(0, Combat.Task(Combat.Operation._HandlePlayerJoin(player, Combat.JoinPriority.NEXT), 0))

    def removePlayer(self, player:Player):
        self.scheduled_tasks.insert(0, Combat.Task(Combat.Operation._HandlePlayerLeave(player), 0))
        player._combat = None
        player.in_combat = False
        if player in self.players:
            self.players.remove(player)

    def onInput(self, player:Player, text:str):
        self.scheduled_tasks.insert(0, Combat.Task(Combat.Operation._HandleInput(player, text), 0))

    def start(self, function_memory:FunctionMemory):
        self.tick = self._mainloop(function_memory)
        self.tick.send(None)
        function_memory.engine.combats.append(self)

    # def responseHandler(self):
    #     while True:
    #         engine, player_id, text = yield EngineOperation.Continue()

    def evaluateResult(self, op:_EngineOperation, player_id:int, text:str=""):
        self.function_memory.engine.evaluateResult(self.function_memory.engine._default_input_handler, self.function_memory.engine.default_input_handler, op, player_id, text)

    def playerAttackEnemy(self, player:Player, enemy:Enemy):
        ev = player.attackEnemy(self.function_memory, enemy)
        v = None
        damage = 0
        try:
            v = ev.send(None)

        except StopIteration as e:
            v = e.value or v

    def enemyAttackPlayer(self, enemy:Enemy, player:Player):
        ev = enemy.attackPlayer(self.function_memory, player, self.last_trigger)
        v = None
        damage = 0
        try:
            v = ev.send(None)
            while isinstance(v, (_EngineOperation, Enemy.Operation._Operation)):
                if isinstance(v, Enemy.Operation._Operation):
                    # TODO: use this to store statistics?
                    v = None
                    v = ev.send(None)
                else:
                    res = yield v
                    v = None
                    v = ev.send(res)
        except StopIteration as e:
            if isinstance(e.value, _EngineOperation):
                yield e.value
            elif isinstance(e.value, Enemy.Operation._Operation):
                # TODO: statistics
                ...
            elif isinstance(e.value, int):
                damage = e.value
                # TODO: statistics

        ev = player.onAttacked(self.function_memory, enemy, damage)
        v = None
        try:
            v = ev.send(None)
            while isinstance(v, _EngineOperation):
                res = yield v
                v = None
                v = ev.send(res)
        except StopIteration as e:
            if isinstance(e.value, _EngineOperation):
                return e.value


    # im okay not implementing these 2 for a while
    def playerAttackPlayer(self, attacking_player:Player, target_player:Player):
        ...
    def enemyAttackEnemy(self, attacking_enemy:Enemy, target_enemy:Enemy):
        ...

    def handleOperation(self, function_memory:FunctionMemory, operation):
        match operation:
            case Combat.Operation._HandlePlayerJoin():
                
                if operation.priority == Combat.JoinPriority.NEXT:
                    self.turn_order.insert(self.current_turn+1, operation.player)
                elif operation.priority == Combat.JoinPriority.LAST:
                    self.turn_order.insert(self.current_turn, operation.player)
                    self.current_turn += 1
                elif operation.priority == Combat.JoinPriority.RANDOM:
                    r = random.randint(1, len(self.turn_order))
                    self.turn_order.insert(r, operation.player)
                    if r <= self.current_turn:
                        self.current_turn += 1

            case Combat.Operation._HandlePlayerLeave():
                i = self.turn_order.index(operation.player)
                self.turn_order.remove(operation.player)
                if i <= self.current_turn:
                    self.current_turn -= 1
                self.turn = self.turn_order[self.current_turn]

            case Combat.Operation._HandleInput():
                text = operation.text
                player = operation.player
                print(f"combat recieved input '{text}' from {player}")
                
                res = TextPattern.handleInput(function_memory, player, text, player._text_pattern_categories)
                #if isinstance(res, Generator):
                v = None
                try:
                    v = res.send(None)
                    if isinstance(v, _EngineOperation):
                        #ret = yield v
                        function_memory.engine.evaluateResult(function_memory.engine._default_input_handler, res, v, player.discord_id, text)
                        #v = res.send(ret)
                except StopIteration as e:
                    if isinstance(e.value, _EngineOperation):
                        self.evaluateResult(e.value, player.discord_id)
                        # function_memory.engine.evaluateResult(function_memory.engine._default_input_handler, function_memory.engine.default_input_handler, e.value, player.discord_id, text)

                if self.turn == player:
                    ...
                    # TODO: text matching for attacking or using an item

                    enemy_name_regexes = []
                    for entity in self.turn_order:
                        if isinstance(entity, Enemy):
                            enemy_name_regexes.append(
                                re.sub(r" +", " *", entity.name.lower())
                            )
                    enemy_names_regex = fr"(?P<enemy_name>{'|'.join(enemy_name_regexes)})"

                    self.prepFunctionMemory(function_memory)

                    function_memory.addContextData({
                        "#enemy_names_regex": enemy_names_regex,
                        "#player": player,
                        "#text": text
                    })

                    ev = function_memory.generatorEvaluateFunction(self.combat_config["on_player_turn_input"])
                    v = None
                    try:
                        v = ev.send(None)
                        while isinstance(v, _EngineOperation):
                            res = yield (player.discord_id, v)
                            v = None
                            v = ev.send(res)
                    except StopIteration as e:
                        if isinstance(e.value, _EngineOperation):
                            res = yield (player.discord_id, e.value)
                        else:
                            v = e.value or v
                            
                else:
                    ...
                    # TODO: text matching for when it's not a player's turn



            case Combat.Operation._EnemyAttack():
                ...
            case Combat.Operation.Trigger():
                self.last_trigger = operation.event_name
            case Combat.Operation.Spawn():
                if operation.priority == Combat.JoinPriority.NEXT:
                    i = 0
                    for enemy_id in operation.enemies:
                        enemy = self.getEnemy(enemy_id)
                        if enemy not in self.turn_order:
                            self.turn_order.insert(self.current_turn+1+i, enemy)
                            i += 1
                elif operation.priority == Combat.JoinPriority.LAST:
                    for enemy_id in operation.enemies:
                        enemy = self.getEnemy(enemy_id)
                        if enemy not in self.turn_order:
                            self.turn_order.insert(self.current_turn, enemy)
                            self.current_turn += 1
                elif operation.priority == Combat.JoinPriority.RANDOM:
                    for enemy_id in operation.enemies:
                        r = random.randint(1, len(self.turn_order))
                        enemy = self.getEnemy(enemy_id)
                        if enemy not in self.turn_order:
                            self.turn_order.insert(r, enemy)
                            if r <= self.current_turn:
                                self.current_turn += 1
            case Combat.Operation.Despawn():
                for enemy_id in operation.enemies:
                    enemy = self.getEnemy(enemy_id)
                    if enemy in self.turn_order:
                        i = self.turn_order.index(enemy)
                        self.turn_order.remove(enemy)
                        if i <= self.current_turn:
                            self.current_turn -= 1
                            self.turn = self.turn_order[self.current_turn]
            case Combat.Operation.Message():
                for player in self.players:
                    function_memory.engine.sendOutput(player, operation.message)
            case Combat.Operation._NextTurn():
                self.current_turn += 1
                if self.current_turn >= len(self.turn_order):
                    self.current_turn = 0
            case _:
                raise CombatError(f"Unrecognized combat operation: '{operation}'")
        yield (0, EngineOperation.Continue())


    def _mainloop(self, function_memory:FunctionMemory):
        self.function_memory = function_memory
        #result = yield {}
        result = None
        while True:
            # if result == None:
            #     result = yield {}
            #     continue

            for task in self.scheduled_tasks.copy():
                task: Combat.Task
                task.delay -= 1
                if task.delay <= 0:
                    self.scheduled_tasks.remove(task)
                    op = task.task
                    
                    try:
                        ev = self.handleOperation(function_memory, op)
                        v = None
                        player_id = 0
                        try:
                            player_id, v = ev.send(None)
                            if isinstance(v, _EngineOperation):
                                function_memory.engine.evaluateResult(function_memory.engine._default_input_handler, function_memory.engine.default_input_handler, v, player_id, "")
                        except StopIteration as e:
                            if isinstance(e.value, _EngineOperation):
                                function_memory.engine.evaluateResult(function_memory.engine._default_input_handler, function_memory.engine.default_input_handler, e.value, player_id, "")
                    except CombatError as e:
                        print(e)

            if self.last_trigger is None:
                self.last_trigger = "@start"
                if (start := self.sequence.get("@start", None)) is not None:
                    self.prepFunctionMemory(function_memory)

                    ev = function_memory.generatorEvaluateFunction(start)
                    v = None
                    try:
                        v = ev.send(None)
                        if isinstance(v, _EngineOperation):
                            self.evaluateResult(v, 0)
                    except StopIteration as e:
                        if isinstance(e.value, _EngineOperation):
                            self.evaluateResult(e.value, 0)
                    ...

            result = yield {}
    
    def quickStats(self, function_memory:FunctionMemory):
        ...
    
    def fullStats(self, function_memory:FunctionMemory):
        ...


