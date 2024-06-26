# pylint: disable=[W,R,C,import-error]

from .AbstractEnemy import AbstractEnemy, Enemy
from .FunctionMemory import FunctionMemory
from .FunctionalElement import FunctionalElement
from .Player import Player
from .EngineErrors import CombatError
from .EngineOperation import EngineOperation, _EngineOperation
from .TextPattern import TextPattern
from .Util import Util
from .Logger import Log
from .Location import Location
from .Position import Position
from .Map import Map
from .Serializer import Serializer, Serializable

from enum import Enum, auto

import random, re, json, time

@Serializable("Combat")
class Combat(FunctionalElement):
    _combats = {}

    with open("./resources/combat.json", "r+", encoding="utf-8") as f:
        _combat_config = json.load(f)

    class JoinPriority(Enum):
        NEXT = auto()
        LAST = auto()
        RANDOM = auto()

    class Operation:
        class _Operation:#(_EngineOperation):
            def __init__(self, name:str, ):
                self.name = name
        
        class Message(_Operation):
            def __init__(self, message:str, *players, global_message=False):
                super().__init__("Message")
                self.message = message
                self.players = players
                self.global_message = global_message

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
            def __repr__(self):
                return f"Combat.Task:EnemyAttack  enemy:{self.enemy} attacking target:{self.target}"

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

        class _HandlePlayerDeath(_Operation):
            def __init__(self, player:Player):
                super().__init__("HandlePlayerDeath")
                self.player = player

        class _NextTurn(_Operation):
            def __init__(self):
                super().__init__("NextTurn")
            def __repr__(self):
                return "Combat.Task:NextTurn"

    class Task:
        def __init__(self, task, delay:int):
            self.task = task
            self.delay = delay
        
        def __repr__(self):
            return f"Combat.Task:[{self.task}]"

    def __new__(cls, abstract, enemies, sequence, data, respawn_point):
        print(cls._combats, abstract)
        if abstract.identifier.full() in cls._combats:
            # print("returning old combat!")
            return cls._combats[abstract.identifier.full()]
        else:
            # print("creating new combat!")
            self = super().__new__(cls) # pylint: disable=no-value-for-parameter
            self._init_(abstract, enemies, sequence, data, respawn_point)
            cls._combats.update({abstract.identifier.full(): self})
            return self

    def _init_(self, abstract, enemies:list[Enemy], sequence:dict, data:dict, respawn_point:Location):
        self.abstract = abstract
        self.location: Location = None
        self.abstract_enemies: list[AbstractEnemy] = enemies
        self.complete = False
        self.enemies = []
        self.sequence: dict = sequence
        self.data: dict = data
        self.respawn_point = respawn_point
        self.players: list[Player] = []
        self.old_players: list[Player] = []
        self.turn_order: list[Player|Enemy] = []
        self.current_turn: int = 0
        self.scheduled_tasks: list[Combat.Task] = []
        self.tick = None
        self.turn = None
        self.last_trigger = None
        self.input_requests = [] # may not need?
        self.function_memory = None
        self.combat_config = Util.deepCopy(self._combat_config)
        self.active = True
        self.turn_summary = {
            "damage_dealt": 0,
            "damage_blocked": 0,
            "attacking_enemy": None,
            "attacked_player": None,
            "attack": None,
            "blocking_armor": None,
            "attack_hit": None,
            "outputs": []
        }
        self.summarize_output = True
        self._enemies = {}

    def serialize(self):
        return {
            "abstract": Serializer.serialize(self.abstract),
            "location": Serializer.serialize(self.location),
            "abstract_enemies": Serializer.serialize(self.abstract_enemies),
            "complete": Serializer.serialize(self.complete),
            "enemies": Serializer.serialize(self.enemies),
            "sequence": Serializer.serialize(self.sequence),
            "data": Serializer.serialize(self.data),
            "respawn_point": Serializer.serialize(self.respawn_point),
            "players": Serializer.serialize(self.players),
            "old_players": Serializer.serialize(self.old_players),
            "turn_order": Serializer.serialize(self.turn_order),
            "current_turn": Serializer.serialize(self.current_turn),
            "scheduled_tasks": Serializer.serialize(self.scheduled_tasks),
            "tick": Serializer.serialize(self.tick),
            "turn": Serializer.serialize(self.turn),
            "last_trigger": Serializer.serialize(self.last_trigger),
            "input_requests": Serializer.serialize(self.input_requests),
            "function_memory": Serializer.serialize(self.function_memory),
            "combat_config": Serializer.serialize(self.combat_config),
            "active": Serializer.serialize(self.active),
            "turn_summary": Serializer.serialize(self.turn_summary),
            "summarize_output": Serializer.serialize(self.summarize_output),
            "_enemies": Serializer.serialize(self._enemies)
        }
    
    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)

    def resetCombat(self):
        try:
            Combat._combats.pop(self.abstract.identifier.full())
        except:
            pass

    def getEnemy(self, function_memory:FunctionMemory, enemy_id:str):
        if enemy := self._enemies.get(enemy_id, None):
            return enemy
        
        for abstract_enemy in self.abstract_enemies:
            if abstract_enemy._id == enemy_id:
                enemy = abstract_enemy.createInstance(function_memory, self.location.copy(), Map.getRandomEnemySpawnPosition(function_memory.engine.loader.getLocation(function_memory, self.location).map), uid=enemy_id)
                self._enemies.update({enemy_id: enemy})
                self.enemies.append(enemy)
                enemy.combat = self
                return enemy

    def getLocalVariables(self) -> dict:
        d = {
            ".enemies": self.enemies,
            ".players": self.players,
            ".current_turn": self.current_turn,
            ".turn": self.turn,
            ".last_trigger": self.last_trigger,
            ".old_trigger": self.old_trigger,
            ".turn_order": self.turn_order,
            ".complete": self.complete,
            ".respawn_point": self.respawn_point,
            ".location": self.location
        }
        return d

    def __dict__(self):
        return {
            "%ENGINE:DATA-TYPE": "Combat",
            "enemies": self.enemies,
            "players": self.players,
            "current_turn": self.current_turn,
            "turn": self.turn,
            "last_trigger": self.last_trigger,
            "old_trigger": self.old_trigger,
            "turn_order": self.turn_order,
            "complete": self.complete,
            "respawn_point": self.respawn_point
        }

    def updateLocalVariables(self, locals: dict):
        ...

    def prepFunctionMemory(self, function_memory:FunctionMemory):
        function_memory.addContextData({
            "#combat": self
        })
        function_memory.update(self.getLocalVariables())
    
    def postEvaluate(self, function_memory:FunctionMemory):
        self.updateLocalVariables(function_memory.symbol_table)

    def addTask(self, task:Operation._Operation, position:int=-1, delay:int=0):
        if self.complete: return

        if isinstance(task, Combat.Operation.Message) and (not task.global_message) and self.summarize_output:
            self.turn_summary["outputs"].append(task.message)
        else:
            self.scheduled_tasks.insert(position, Combat.Task(task, delay))

    def addPlayer(self, player:Player):
        if self.complete: return
        player.in_combat = True
        player._combat = self
        self.players.append(player)
        if player not in self.old_players:
            self.old_players.append(player)
        self.scheduled_tasks.insert(0, Combat.Task(Combat.Operation._HandlePlayerJoin(player, Combat.JoinPriority.NEXT), 0))

    def removePlayer(self, player:Player):
        
        self.scheduled_tasks.insert(0, Combat.Task(Combat.Operation._HandlePlayerLeave(player), 0))
        player._combat = None
        player.in_combat = False
        if player in self.players:
            self.players.remove(player)

    def onInput(self, player:Player, text:str):
        if self.complete: return
        self.scheduled_tasks.insert(0, Combat.Task(Combat.Operation._HandleInput(player, text), 0))

    def start(self, function_memory:FunctionMemory):
        
        # print("start called")
        
        if self.complete: return
        
        # print("combat.complete is False")
        
        self.tick = self._mainloop(function_memory)
        self.tick.send(None)
        function_memory.engine.combats.append(self)
        
        function_memory.engine.sendOutput(3, self)

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
        Log["debug"]["enemy"]("ENEMY ATTACK PLAYER!!")
        
        if enemy.health <= 0 and enemy.max_health > 0:
            # self.addTask(Combat.Operation._NextTurn())
            return
        
        self.function_memory.update({
            "damage": 0
        })
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

        damage = self.function_memory.ref("damage")

        # print(f"Combat: damage: {damage}")

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
            elif isinstance(e.value, Combat.Operation._HandlePlayerDeath):
                self.scheduled_tasks.insert(0, Combat.Task(e.value, 0))


    # im okay not implementing these 2 for a while
    def playerAttackPlayer(self, attacking_player:Player, target_player:Player):
        ...
    def enemyAttackEnemy(self, attacking_enemy:Enemy, target_enemy:Enemy):
        ...

    def handleOperation(self, function_memory:FunctionMemory, operation):
        # if self.complete: return
        match operation:
            case Combat.Operation._HandlePlayerJoin():
                
                if operation.priority == Combat.JoinPriority.NEXT:
                    self.turn_order.insert(self.current_turn+1, operation.player)
                    i = self.current_turn+1
                elif operation.priority == Combat.JoinPriority.LAST:
                    self.turn_order.insert(self.current_turn, operation.player)
                    i = self.current_turn
                    self.current_turn += 1
                elif operation.priority == Combat.JoinPriority.RANDOM:
                    r = random.randint(1, len(self.turn_order))
                    self.turn_order.insert(r, operation.player)
                    i = r
                    if r <= self.current_turn:
                        self.current_turn += 1
                else: i = 0 # this branch is unreachable
                
                # reset turn to player if player is first to join/is re-joining combat
                if len([a for a in self.turn_order if isinstance(a, Player)]) == 1:
                    self.current_turn = i + 1
                    # self.turn = operation.player
                
                    # self.current_turn += 1
                    if self.current_turn >= len(self.turn_order):
                        self.current_turn = 0
                    self.turn = self.turn_order[self.current_turn]
                    

            case Combat.Operation._HandlePlayerLeave():
                i = self.turn_order.index(operation.player)
                self.turn_order.remove(operation.player)
                if i <= self.current_turn:
                    self.current_turn -= 1
                self.turn = self.turn_order[self.current_turn]

            case Combat.Operation._HandlePlayerDeath():
                player = operation.player
                i = self.turn_order.index(player)
                self.turn_order.remove(player)

                if player in self.players:
                    self.players.remove(player)

                player._combat = None
                player.in_combat = False

                if i <= self.current_turn:
                    self.current_turn -= 1
                self.turn = self.turn_order[self.current_turn]

                player.health = 3 # TODO: set player recovery health

                Log["debug"]["combat"](f"Player `{player}` died. respawned at `{self.respawn_point}`")
                self.scheduled_tasks.append(
                    Combat.Task(Combat.Operation.Message(self.data.get("player_death_message", "`{player}` died.").format(player=player)), 0)
                )

                if len(self.players) == 0:
                    self.turn = None
                    self.turn_order.clear()
                    self.active = False
                    Log["debug"]["combat"]("Combat ended. Players lost")
                    self.scheduled_tasks.append(
                        Combat.Task(Combat.Operation.Message(self.data.get("player_lose_message", "Combat Ended. Players lost"), *self.old_players), 0)
                    )
                    # self.complete = True
                    self.resetCombat()
                    function_memory.engine.sendOutput(3, None)

                yield (player.uuid, EngineOperation.KillPlayer(player, self.respawn_point))

            case Combat.Operation._HandleInput():
                text = operation.text
                player = operation.player
                Log["debug"]["combat"]["handle operation"](f"combat recieved input '{text}' from {player}")

                Log["debug"]["INFO"](f"Combat data:  turn={self.turn}")
                
                res = TextPattern.handleInput(function_memory, player, text, player._text_pattern_categories)
                #if isinstance(res, Generator):
                v = None
                try:
                    v = res.send(None)
                    if isinstance(v, _EngineOperation):
                        #ret = yield v
                        function_memory.engine.evaluateResult(function_memory.engine._default_input_handler, res, v, player.uuid, text)
                        #v = res.send(ret)
                except StopIteration as e:
                    if isinstance(e.value, _EngineOperation):
                        self.evaluateResult(e.value, player.uuid)
                        # function_memory.engine.evaluateResult(function_memory.engine._default_input_handler, function_memory.engine.default_input_handler, e.value, player.uuid, text)

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
                            res = yield (player.uuid, v)
                            v = None
                            v = ev.send(res)
                    except StopIteration as e:
                        if isinstance(e.value, _EngineOperation):
                            res = yield (player.uuid, e.value)
                        else:
                            v = e.value or v
                            
                else:
                    ...
                    # TODO: text matching for when it's not a player's turn

            case Combat.Operation._EnemyAttack():
                if self.turn_order:
                    enemy = operation.enemy
                    player = operation.target

                    if (not player) or (player not in self.players):
                        return

                    ev = self.enemyAttackPlayer(enemy, player)
                    v = None
                    try:
                        v = ev.send(None)
                        while isinstance(v, _EngineOperation):
                            res = yield (player.uuid, v)
                            v = None
                            v = ev.send(res)
                    except StopIteration as e:
                        if isinstance(e.value, _EngineOperation):
                            res = yield (player.uuid, e.value)
                        else:
                            v = e.value or v # idk why i'm doing this

                    self.send_turn_summary(function_memory)
                    
                    self.current_turn += 1
                    if self.current_turn >= len(self.turn_order):
                        self.current_turn = 0
                    self.turn = self.turn_order[self.current_turn]


                    if isinstance(self.turn, Enemy):
                        self.scheduled_tasks.append(
                            Combat.Task(Combat.Operation._EnemyAttack(self.turn, random.choice(self.players or [None])), f"{time.time()+5}")
                        )

            case Combat.Operation.Trigger():
                self.old_trigger = self.last_trigger
                self.last_trigger = operation.event_name

            case Combat.Operation.Spawn():
                Log["debug"]["combat"]["handle operation"]("dungeon spawn enemies?")
                if operation.priority == Combat.JoinPriority.NEXT:
                    i = 0
                    for enemy_id in operation.enemies:
                        enemy = self.getEnemy(function_memory, enemy_id)
                        if enemy not in self.turn_order:
                            self.turn_order.insert(self.current_turn+1+i, enemy)
                            enemy.combat = self
                            i += 1
                elif operation.priority == Combat.JoinPriority.LAST:
                    for enemy_id in operation.enemies:
                        enemy = self.getEnemy(function_memory, enemy_id)
                        if enemy not in self.turn_order:
                            self.turn_order.insert(self.current_turn, enemy)
                            enemy.combat = self
                            self.current_turn += 1
                elif operation.priority == Combat.JoinPriority.RANDOM:
                    for enemy_id in operation.enemies:
                        r = random.randint(1, len(self.turn_order))
                        enemy = self.getEnemy(function_memory, enemy_id)
                        if enemy not in self.turn_order:
                            self.turn_order.insert(r, enemy)
                            enemy.combat = self
                            if r <= self.current_turn:
                                self.current_turn += 1
                # self.turn = self.turn_order[self.current_turn]
                function_memory.engine.sendOutput(9, "update-combat-ui")

            case Combat.Operation.Despawn():
                for enemy_id in operation.enemies:
                    enemy = self.getEnemy(function_memory, enemy_id)
                    if enemy in self.turn_order:
                        i = self.turn_order.index(enemy)
                        self.turn_order.remove(enemy)
                        if i <= self.current_turn:
                            self.current_turn -= 1
                
                if all((isinstance(a, Player) or ((isinstance(a, Enemy) and a.health <= 0))) for a in self.turn_order):
                    Log["debug"]["combat"]("Combat ended. Players win!")
                    self.scheduled_tasks.append(
                        Combat.Task(Combat.Operation.Message(self.data.get("player_win_message", "Combat Ended. Players win!"), *self.players), 0)
                    )
                    self.complete = True
                    function_memory.engine.sendOutput(3, None)
                    
                    for player in self.players:
                        player.in_combat = False
                        player._combat = None
                    
                    self.players.clear()
                    self.turn_order.clear()
                    self.turn = 0
                else:
                    self.turn = self.turn_order[self.current_turn]
                function_memory.engine.sendOutput(9, "update-combat-ui")

            case Combat.Operation.Message():
                Log["debug"]["combat"]["message"](operation.message)
                if operation.players:
                    if self.summarize_output:
                        self.turn_summary["outputs"].append(operation.message)
                    else:
                        for player in operation.players:
                            function_memory.engine.sendOutput(player, operation.message)
                else:
                    if self.summarize_output:
                        self.turn_summary["outputs"].append(operation.message)
                    else:
                        for player in self.players:
                            function_memory.engine.sendOutput(player, operation.message)

            case Combat.Operation._NextTurn():

                if len(self.turn_order) == 0 or len([a for a in self.players if isinstance(a, Player)]) == 0:
                    return

                self.current_turn += 1
                if self.current_turn >= len(self.turn_order):
                    self.current_turn = 0
                self.turn = self.turn_order[self.current_turn]
                
                self.send_turn_summary(function_memory)

                if isinstance(self.turn, Enemy):
                    self.turn_summary = {
                        "damage_dealt": 0,
                        "damage_blocked": 0,
                        "attacking_enemy": None,
                        "attacked_player": None,
                        "attack": None,
                        "blocking_armor": None,
                        "attack_hit": None,
                        "outputs": []
                    }
                    self.summarize_output = True
                    self.scheduled_tasks.append(
                        Combat.Task(Combat.Operation._EnemyAttack(self.turn, random.choice(self.players)), f"{time.time()+5}")
                    )
                else:
                    # self.summarize_output = False
                    function_memory.engine.sendOutput(9, "update-combat-ui")

            case _:
                raise CombatError(f"Unrecognized combat operation: '{operation}'")
        yield (0, EngineOperation.Continue())


    def send_turn_summary(self, function_memory:FunctionMemory):
        targets = " / ".join(p.name for p in self.players)

        damage: int = self.turn_summary["damage_dealt"]
        blocked: int = self.turn_summary["damage_blocked"]
        enemy: Enemy = self.turn_summary["attacking_enemy"]
        target: Player = self.turn_summary["attacked_player"]
        attack = self.turn_summary["attack"]
        hit: bool = self.turn_summary["attack_hit"],
        armor = self.turn_summary["blocking_armor"]
        outs = "\n".join(self.turn_summary["outputs"])

        if target is None: return


        self.turn_summary = {
            "damage_dealt": 0,
            "damage_blocked": 0,
            "attacking_enemy": None,
            "attacked_player": None,
            "attack": None,
            "blocking_armor": None,
            "attack_hit": None,
            "outputs": []
        }

        if hit and damage:
            summary = "\n".join([
                "```less",
                targets,
                outs,
                f"\n─ {enemy.name} {Util.getDurabilityBar(enemy.health, enemy.max_health)} ─ {attack.name} ─ HIT ─ {damage} damage",
                f"Damage: {damage}" + (f" (-{blocked} {armor.name}) = {max(0, damage-blocked)}" if armor.name != "Common Clothes" else ""),
                f"│ {target.name} {Util.getDurabilityBar(target.health, target.max_health)}"
            ])

            if armor.name != "Common Clothes":
                summary += f"\n│ {armor.name} {armor.durability}/{armor.max_durability}"

            summary += "\n```"

        else:
            summary = "\n".join([
                "```less",
                targets,
                outs,
                f"\n─ {enemy.name} {Util.getDurabilityBar(enemy.health, enemy.max_health)} ─ {attack.name} ─ MISS",
                f"│ {target.name} {Util.getDurabilityBar(target.health, target.max_health)}",
                "```"
            ])
        
        function_memory.engine.sendOutput("Combat", summary)

    def _mainloop(self, function_memory:FunctionMemory):
        self.function_memory = function_memory
        #result = yield {}
        result = None
        
        if self.complete: return
        
        while self.active:
            # if result == None:
            #     result = yield {}
            #     continue
            
            for task in self.scheduled_tasks.copy():
                task: Combat.Task
                if isinstance(task.delay, int):
                    task.delay -= 1
                elif isinstance(task.delay, str):
                    if time.time() >= float(task.delay):
                        task.delay = 0
                    
                if isinstance(task.delay, (int, float)) and task.delay <= 0:
                    Log["debug"]["combat"](f"running combat-task: {task}")
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
                        Log["ERROR"]["combat"](e)

            if self.complete:
                if self.scheduled_tasks:
                    continue
                else:
                    self.active = False
                    return

            if len(self.turn_order) == 0:
                if self.scheduled_tasks:
                    continue
                self.active = False

            if self.last_trigger is None:
                self.last_trigger = self.old_trigger = "@start"
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

            if self.old_trigger != self.last_trigger:
                self.old_trigger = self.last_trigger
                if (seq := self.sequence.get(self.last_trigger, None)) is not None:
                    self.prepFunctionMemory(function_memory)

                    ev = function_memory.generatorEvaluateFunction(seq)
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
        WIDTH = 50-19
        # │┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌▓▒░
        
        
        #      ┌─────────────╓╥╥╥╥╥╥╥╥╥╥╥╥──────┐
        #      │ Zombie 1    ╙╨╨╨╨╨╨╨╨╨╨╨╨──────┤
        #      └────────────────────────────────┘
        
        lines = [
            "```",
            f"┌{'─'*WIDTH}┐",
            f"│ {'Combat Stats': <{WIDTH-2}} │",
            f"├{'─'*WIDTH}┤",
        ]
        
        for t in self.turn_order:
            t: Enemy|Player
            
            if self.turn is t:
                per = int(t.health/t.max_health*15)
                
                if per == 0:
                    b1 = f"╔{'═'*15}╗"
                    b2 = f"╙{'─'*15}╢"
                else:
                    b1 = f"╔{'╦'*per}{'═'*(15-per)}╗"
                    b2 = f"╙{'╨'*per}{'─'*(15-per)}╢"

                sub = [
                    f"│ ╔{'═'*(WIDTH-(20))}{b1} │",
                    f"│ ║ {t.name: <{WIDTH-22}} {b2} │",
                    f"│ ╚{'═'*(WIDTH-4)}╝ │"
                ]
            
            else:
                per = int(t.health/t.max_health*15)
                
                if per == 0:
                    b1 = f"┌{'─'*15}┐"
                    b2 = f"└{'─'*15}┤"
                else:
                    b1 = f"╓{'╥'*per}{'─'*(15-per)}┐"
                    b2 = f"╙{'╨'*per}{'─'*(15-per)}┤"

                sub = [
                    f"│ ┌{'─'*(WIDTH-20)}{b1} │",
                    f"│ │ {t.name: <{WIDTH-22}} {b2} │",
                    f"│ └{'─'*(WIDTH-4)}┘ │"
                ]
            lines += sub
        
        lines += [
            f"└{'─'*WIDTH}┘",
            "```"
        ]
        
        return "\n".join(lines)


