# pylint: disable=[W,R,C,import-error]

try:
    from .EngineDummy import Engine
except ImportError:
    from EngineDummy import Engine



class StatusEffect:

    def __init__(self, abstract):
        self.abstract = abstract
        ...

    def _get_save(self, engine:Engine):
        ...
