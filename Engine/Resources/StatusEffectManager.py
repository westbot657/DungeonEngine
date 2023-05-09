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
        self.effects: list[StatusEffect] = []
        
    def addEffect(self, effect:StatusEffect):
        effect.effect_manager = self
        self.effects.append(effect)

    def fullStats(self):
        return "\n".join([effect.fullStats() for effect in self.effects]).strip()

    def _get_save(self, function_memory):
        ...
    
    



