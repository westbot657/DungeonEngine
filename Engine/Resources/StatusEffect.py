# pylint: disable=[W,R,C,import-error]

from .EngineDummy import Engine
from .StatusEffectCause import StatusEffectCause
from .FunctionalElement import FunctionalElement
from .FunctionMemory import FunctionMemory
from .Serializer import Serializer, Serializable


@Serializable("StatusEffect")
class StatusEffect(FunctionalElement):

    def __init__(self, abstract, name:str, level:int, duration:float|int, tick_interval:int, cause:StatusEffectCause, events:dict, getters:dict):
        self.abstract = abstract
        self.name = name
        self.level = level
        self.duration = duration
        self.tick_interval = tick_interval
        self.cause = cause
        self.events = events
        self.getters = getters

        self.effect_manager = None

    def serialize(self) -> dict:
        return Serializer.smartSerialize(
            self, 
            "abstract", "name", "level", "duration", "tick_interval", "cause", "events", "getters", "effect_manager"
        )
    
    @classmethod
    def deserialize(cls, instance, data: dict):
        return Serializer.smartDeserialize(instance, data)

    def getLocalVariables(self) -> dict:
        d = {
            ".name": self.name,
            ".level": self.level,
            ".duration": self.duration,
            ".cause": self.cause.getDisplay(),
            ".tick_interval": self.tick_interval
        }
        return d

    def bonuses(self, engine:Engine):
        if (get_bonuses := self.getters.get("bonuses", None)) is not None:
            return engine.evaluateFunction(get_bonuses, FunctionMemory(engine), None, self.getLocalVariables())

        return None

    def quickStats(self, function_memory:FunctionMemory):

        if (get_quick_stats := self.getters.get("quick_stats", None)) is not None:
            return function_memory.engine.evaluateFunction(get_quick_stats, FunctionMemory(function_memory.engine), None, self.getLocalVariables())

        return f"{self.name} {self.level}"

    def fullStats(self, function_memory:FunctionMemory):

        if (get_full_stats := self.getters.get("full_stats", None)) is not None:
            return function_memory.engine.evaluateFunction(get_full_stats, FunctionMemory(function_memory.engine), None, self.getLocalVariables())

        return f"{self.name} {self.level} {self.duration}s {self.cause.getDisplay()}"

    def onPlayerHit(self, function_memory:FunctionMemory):
        ...

    def _get_save(self, function_memory:FunctionMemory):
        d = {
            "type": "engine:status_effect",
            "effect": self.abstract.identifier.full(),
            "level": self.level,
            "cause": self.cause._get_cause()
        }



        return d
