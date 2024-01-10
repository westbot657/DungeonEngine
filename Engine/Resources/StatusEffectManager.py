# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
    from .StatusEffect import StatusEffect
    from .EngineDummy import Engine
    from .FunctionMemory import FunctionMemory
    from .Serializer import Serializer, Serializable
except ImportError:
    from Identifier import Identifier
    from StatusEffect import StatusEffect
    from EngineDummy import Engine
    from FunctionMemory import FunctionMemory
    from Serializer import Serializer, Serializable

@Serializable("StatusEffectManager")
class StatusEffectManager:
    
    def __init__(self):
        self.effects: list[StatusEffect] = []
    
    def serialize(self):
        return Serializer.smartSerialize(self, "effects")
    
    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)
    
    def addEffect(self, effect:StatusEffect):
        effect.effect_manager = self
        self.effects.append(effect)

    def fullStats(self, function_memory:FunctionMemory):
        return "\n".join([effect.fullStats() for effect in self.effects]).strip()

    def quickStats(self, function_memory:FunctionMemory):
        return "\n".join([effect.quickStats() for effect in self.effects]).strip()

    def onPlayerHit(self, function_memory:FunctionMemory, damage:int):
        yield


    def _get_save(self, function_memory:FunctionMemory):
        data = []

        for effect in self.effects:
            data.append(effect._get_save(function_memory))
        
        return data
    
    



