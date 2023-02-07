# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
    from .StatusEffect import StatusEffect
    from .EngineDummy import Engine
except ImportError:
    from Identifier import Identifier
    from StatusEffect import StatusEffect
    from EngineDummy import Engine



class StatusEffectManager:
    
    def __init__(self):
        self.effects = []
        
    def addEffect(self, effect:StatusEffect):
        ...

    def fullStats(self):
        return ""

    def _get_save(self, engine:Engine):
        ...
    
    



