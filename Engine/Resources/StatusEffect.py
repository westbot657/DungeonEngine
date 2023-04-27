# pylint: disable=[W,R,C,import-error]

try:
    from .EngineDummy import Engine
    from .StatusEffectCause import StatusEffectCause
    from .FunctionalElement import FunctionalElement
except ImportError:
    from EngineDummy import Engine
    from StatusEffectCause import StatusEffectCause
    from FunctionalElement import FunctionalElement



class StatusEffect(FunctionalElement):

    def __init__(self, abstract, name:str, level:int, duration:float|int, tick_interval, cause:StatusEffectCause, events:dict):
        self.abstract = abstract
        self.name = name
        self.level = level
        self.duration = duration
        self.tick_interval = tick_interval
        self.cause = cause
        self.events = events

    def _get_save(self, function_memory):
        ...
