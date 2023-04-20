# pylint: disable=[W,R,C,import-error]

try:
    from .EngineDummy import Engine
except ImportError:
    from EngineDummy import Engine



class StatusEffect:

    def __init__(self, abstract, name:str, level:int, duration:float|int, cause, events:dict):
        self.abstract = abstract
        self.name = name
        self.level = level
        self.duration = duration
        self.cause = cause
        self.events = events

    def _get_save(self, function_memory):
        ...
