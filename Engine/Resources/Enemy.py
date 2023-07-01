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
    from .EngineOperation import _EngineOperation
except:
    from Entity import Entity
    from Identifier import Identifier
    from Location import Location
    from EngineDummy import Engine
    from Position import Position
    from FunctionMemory import FunctionMemory
    from Util import Util
    from AbstractAttack import AbstractAttack, Attack
    from EngineOperation import _EngineOperation

import json, random

class Enemy(Entity):
    
    class Operation:
        class _Operation:
            def __init__(self, name:str):
                self._name = name
        
        class ChooseAttack(_Operation):
            def __init__(self, attack:Attack):
                super().__init__("Choose Attack")
                self.attack = attack
        
        class ForceMiss(_Operation):
            def __init__(self):
                super().__init__("Force Miss")

        class ForceHit(_Operation):
            def __init__(self):
                super().__init__("Force Hit")

        class CancelAttack(_Operation):
            def __init__(self):
                super().__init__("Cancel Attack")

    def __init__(self, abstract, name:str, max_health:int, health:int, attacks:list, location:Location, position:Position):
        self.abstract = abstract
        self.name = name
        self.max_health = max_health
        self.health = health
        self.attacks = attacks
        self.uid = None
        super().__init__(location, position)
        self.events: dict[str, dict] = {}

        self.combat = None

    def getLocalVariables(self) -> dict:
        d = {
            ".name": self.name,
            ".max_health": self.max_health,
            ".health": self.health,
            ".attacks": self.attacks,
            ".uid": self.uid
        }

        return d

    def updateLocalVariables(self, locals: dict):
        ...
    
    def prepFunctionMemory(self, function_memory:FunctionMemory):
        function_memory.addContextData({
            "#enemy": self
        })
        function_memory.update(self.getLocalVariables())
    
    def postEvaluate(self, function_memory:FunctionMemory):
        self.updateLocalVariables(function_memory.symbol_table)

    def quickStats(self, function_memory:FunctionMemory):
        return f"{self.name}  {Util.getDurabilityBar(self.health, self.max_health)}"

    def fullStats(self, function_memory:FunctionMemory):
        s = [f"{self.name}  {Util.getDurabilityBar(self.health, self.max_health)}"]

        for attack in self.attacks:
            attack: Attack
            s.append(f"  {attack.quickStats(function_memory)}")

        return "\n".join(s)

    def setEvents(self, events):
        self.events = Util.deepCopy(events)
        with open("../resources/enemy_required_events.json", "r+", encoding="utf-8") as f:
            self.events.update(json.load(f))

    def attackPlayer(self, function_memory:FunctionMemory, player, current_trigger:str):

        attack = random.choice(self.attacks)

        self.prepFunctionMemory(function_memory)
        function_memory.addContextData({
            "#player": player
        })
        function_memory.update({
            "attack": attack
        })

        ev = self.onEvent(function_memory, current_trigger, "on_attack")
        v = None
        hit = None
        try:
            v = ev.send(None)
            while isinstance(v, _EngineOperation, Enemy.Operation._Operation):
                if isinstance(v, Enemy.Operation._Operation):
                    match v:
                        case Enemy.Operation.CancelAttack():
                            ev.close()
                            return v
                        case Enemy.Operation.ChooseAttack():
                            if isinstance(v.attack, str):
                                for atk in self.attacks:
                                    if atk.abstract.identifier.full() == v.attack:
                                        attack = atk
                                        break
                            elif v.attack in self.attacks:
                                attack = v.attack
                        case Enemy.Operation.ForceHit():
                            hit = True
                        case Enemy.Operation.ForceMiss():
                            hit = False
                    yield v
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
                match e.value:
                    case Enemy.Operation.CancelAttack():
                        ev.close()
                        return e.value
                    case Enemy.Operation.ChooseAttack():
                        if isinstance(e.value.attack, str):
                            for atk in self.attacks:
                                if atk.abstract.identifier.full() == e.value.attack:
                                    attack = atk
                                    break
                        elif e.value.attack in self.attacks:
                            attack = e.value.attack
                    case Enemy.Operation.ForceHit():
                        hit = True
                    case Enemy.Operation.ForceMiss():
                        hit = False
                yield e.value
        
        if hit is False:
            acc = 0
        elif hit is True:
            acc = 100
        else:
            acc = None
        
        ev = attack.onAttack(function_memory, player, acc)
        v = None
        try:
            v = ev.send(None)
            while isinstance(v, (_EngineOperation, Enemy.Operation._Operation)):
                if isinstance(v, Enemy.Operation.CancelAttack):
                    ev.close()
                    return v
                if isinstance(v, _EngineOperation):
                    res = yield v
                    v = None
                    v = ev.send(None)
        except StopIteration as e:
            if isinstance(e.value, (_EngineOperation, Enemy.Operation._Operation)):
                if isinstance(e.value, Enemy.Operation.CancelAttack):
                    ev.close()
                    return e.value
                if isinstance(v, _EngineOperation):
                    return v
            return e.value or v
    
    def damage(self, function_memory:FunctionMemory, amount:int):
        ...
    
    def heal(self, function_memory:FunctionMemory, amount:int):
        ...
    
    def kill(self, function_memory:FunctionMemory):
        ...

    def onEvent(self, function_memory:FunctionMemory, current_trigger:str, event_name:str):
        if current_trigger is None and self.combat is not None:
            current_trigger = self.combat.last_trigger
        for trigger in [current_trigger, "@global", "@required"]:
            if trigger in self.events:
                if (event := self.events[trigger].get(event_name, None)):
                    self.prepFunctionMemory(function_memory)

                    ev = function_memory.generatorEvaluateFunction(event)
                    v = None
                    try:
                        v = ev.send(None)
                        while isinstance(v, _EngineOperation):
                            res = yield v
                            v = ev.send(res)
                    except StopIteration as e:
                        v = e.value or (v if not isinstance(v, _EngineOperation) else None)

                    self.postEvaluate(function_memory)
                    return v

    def _get_save(self, function_memory:FunctionMemory) -> dict:
        return {}



