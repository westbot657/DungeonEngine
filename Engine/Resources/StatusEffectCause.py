# pylint: disable=[W,R,C,import-error]

try:
    from .FunctionalElement import FunctionalElement
except ImportError:
    from FunctionalElement import FunctionalElement


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

    def getDisplay(self):
        return f"[{self.name}]"

    def __repr__(self):
        extra = self.getDisplay()
        if extra:
            return f"{self.name} {extra}"
        return self.name

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

class EnemyInflictedStatusEffectCause(StatusEffectCause):
    def __init__(self, enemy):
        super().__init__("Enemy Inflicted")
        self.enemy = enemy
    
    def getDisplay(self):
        return f"({self.enemy})"



