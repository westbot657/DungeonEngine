# pylint: disable=[W,R,C,import-error,assignment-from-none]

try:
    from .FunctionalElement import FunctionalElement
    from .Serializer import Serializer, Serializable
except ImportError:
    from FunctionalElement import FunctionalElement
    from Serializer import Serializer, Serializable

@Serializable("StatusEffectCause")
class StatusEffectCause(FunctionalElement):
    _cause_types = {}

    def __init_subclass__(cls):
        StatusEffectCause._cause_types.update({cls.__name__: cls})

    @classmethod
    def getCauseType(cls, cause_type:str|None=None):
        if cause_type is not None and cause_type in cls._cause_types:
            return cls._cause_types[cause_type]
        else:
            return cls._cause_types["UnknownStatusEffectCause"]

    def __init__(self, name:str):
        self.name = name

    def serialize(self):
        return Serializer.smartSerialize(self, "name")
    
    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)

    def getDisplay(self):
        return None #f"[{self.name}]"

    @classmethod
    def load(cls, data:dict):
        if data.get("type", None) == "status_effect_cause":
            c = cls._cause_types[data.get("cause_type", "UnknownStatusEffectCause")](**data.get("data", {}))
        return cls._cause_types["UnknownStatusEffectCause"]()

    def __repr__(self):
        extra = self.getDisplay()
        if extra:
            return f"{self.name} {extra}"
        return self.name

    def _get_save(self, function_memory):
        return {
            "type": "engine:status_effect_cause",
            "cause_type": self.__class__.__name__,
            "data": {}
        }

class UnknownStatusEffectCause(StatusEffectCause):
    def __init__(self):
        super().__init__("Unknown Effect Cause")


class PassiveStatusEffectCause(StatusEffectCause):
    def __init__(self):
        super().__init__("Passive Effect")


class SelfInflictedStatusEffectCause(StatusEffectCause):
    def __init__(self, player):
        super().__init__("Self Inflicted")
        self.player = player
    
    def getDisplay(self):
        return f"({self.player})"

    def _get_save(self, function_memory):
        return {
            "type": "engine:status_effect_cause",
            "cause_type": self.__class__.__name__,
            "cause": f"{self}",
            "data": {
                "player": f"{self.player}"
            }
        }

class EnemyInflictedStatusEffectCause(StatusEffectCause):
    def __init__(self, enemy):
        super().__init__("Enemy Inflicted")
        self.enemy = enemy

    def getDisplay(self):
        return f"({self.enemy})"

    def _get_save(self, function_memory):
        return {
            "type": "engine:status_effect_cause",
            "cause_type": self.__class__.__name__,
            "cause": f"{self}",
            "data": {
                "enemy": f"{self.enemy}"
            }
        }

