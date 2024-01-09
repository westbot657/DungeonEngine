# pylint: disable=[W,R,C,import-error]

try:
    from .StatusEffect import StatusEffect
    from .EngineErrors import InvalidObjectError
    from .Identifier import Identifier
    from .DynamicValue import DynamicValue
    from .StatusEffectCause import StatusEffectCause
    from .FunctionMemory import FunctionMemory
    from .Logger import Log
    from .Loader import Loader
    from .Serializer import Serializer, Serializable
except ImportError:
    from StatusEffect import StatusEffect
    from EngineErrors import InvalidObjectError
    from Identifier import Identifier
    from DynamicValue import DynamicValue
    from StatusEffectCause import StatusEffectCause
    from FunctionMemory import FunctionMemory
    from Logger import Log
    from Loader import Loader
    from Serializer import Serializer, Serializable


import glob, json, re

@Serializable("AbstractStatusEffect")
class AbstractStatusEffect:
    _loaded = {}
    _link_parents = []

    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data
        self.parent: AbstractStatusEffect|None = None
        self.children: list[AbstractStatusEffect] = []

        if "parent" in data:
            AbstractStatusEffect._link_parents.append((self, data["parent"]))

        self.name: str|None = data.get("name", None)
        self.level: int|None = data.get("level", None)
        self.duration: int|None = data.get("duration", None)
        self.tick_interval: int|dict|None = data.get("tick_interval", None)
        self.cause: int|None = data.get("cause", None)
        self.events: dict = data.get("events", {})
        self.getters: dict = data.get("display", {})

        self.is_template: bool = data.get("template", False)

    def getName(self):
        n = self.name or (self.parent.getName() if self.parent else None)
        if n is not None: return n
        raise InvalidObjectError(f"StatusEffect has no name! ({self.identifier})")

    def getLevel(self):
        if self.level is None:
            l = self.parent.getLevel() if self.parent else None
        else:
            l = self.level
        if l is not None:
            return l
        raise InvalidObjectError(f"StatusEffect has no level! ({self.identifier})")
    
    def getDuration(self):
        if self.duration is None:
            d = self.parent.getDuration() if self.parent else None
        else:
            d = self.duration
        if d is not None:
            return d
        return 1
        # raise InvalidObjectError(f"StatusEffect has no duration! ({self.identifier})")

    def getTickInterval(self):
        if self.tick_interval is None:
            if self.events.get("on_tick", None) is not None:
                return 1
            return -1
        return self.tick_interval

    def getCause(self):
        if self.cause is None: # *existential crisis*
            c = self.parent.getCause() if self.parent else None
        else:
            c = self.cause
        if c is not None:
            return c
        return StatusEffectCause.getCauseType(c)
        
    def _assertCause(self, cause):
        if isinstance(cause, StatusEffectCause):
            return cause()
        elif isinstance(cause, dict):
            return StatusEffectCause.load(cause)
        raise InvalidObjectError(f"StatusEffect has invalid cause: '{cause}'") # *existential crisis part 2*
    
    def createInstance(self, function_memory:FunctionMemory, **override_values):
        if self.is_template:
            pass
            # I sure hope no one makes any status effect templates and tries to apply them as an effect...
        else:
            return StatusEffect(self,
                override_values.get("name", self.getName()),
                override_values.get("level", self.getLevel()),
                override_values.get("duration", self.getDuration()),
                DynamicValue(override_values.get("tick_interval", self.getTickInterval())).getCachedOrNew(function_memory),
                self._assertCause((override_values.get("cause", self.getCause()))),
                self.events,
                self.getters
            )

    @classmethod
    def loadData(cls, engine) -> list:
        files: list[str] = glob.glob("**/status_effects/*.json", recursive=True)

        Log["loadup"]["abstract"]["status effect"](f"found {len(files)} status effect files")
        for file in files:
            file: str
            Log["loadup"]["abstract"]["status effect"](f"loading AbstractStatusEffect from '{file}'")
            data = Loader.load(file)
            
            Id = Identifier.fromFile(file)
            cls._loaded.update({Id.full(): cls(Id, data)})

        Log["loadup"]["abstract"]["status effect"]("linking AbstractStatusEffect parents...")
        for a, p in cls._link_parents:
            a: AbstractStatusEffect
            p: str
            if parent := cls._loaded.get(p, None):
                if parent is a:
                    Log["ERROR"]["loadup"]["abstract"]["status effect"]("cannot set object as it's own parent")
                    continue
                elif parent in a.get_parent_chain():
                    Log["ERROR"]["loadup"]["abstract"]["status effect"]("circular parent loop found")
                    continue
                a._set_parent(parent)
            else:
                Log["ERROR"]["loadup"]["abstract"]["status effect"](f"parent does not exist: '{p}'")
        
        Log["loadup"]["abstract"]["status effect"]("verifying AbstractStatusEffect completion...")
        Log.track(len(cls._loaded), "loadup", "abstract", "status effect")
        for l, o in cls._loaded.copy().items():
            l: str
            o: AbstractStatusEffect
            if o.is_template:
                Log.success()
                continue
            try:
                o.getName()
                o.getLevel()
                o.getDuration()
                o.getCause()
                Log.success()
            except InvalidObjectError:
                e: AbstractStatusEffect = cls._loaded.pop(l)
                Log.ERROR("loadup", "abstract", "status effect", f"failed to load status effect: {e.identifier}")

        Log.end_track()

        cls._link_parents.clear()

        Log["loadup"]["abstract"]["status effect"]("AbstractStatusEffect loading complete")
        return cls._loaded

    def serialize(self):
        return {
            "identifier": Serializer.serialize(self.identifier),
            "_raw_data": Serializer.serialize(self._raw_data),
            "parent": Serializer.serialize(self.parent),
            "children": Serializer.serialize(self.children),
            "name": Serializer.serialize(self.name),
            "level": Serializer.serialize(self.level),
            "duration": Serializer.serialize(self.duration),
            "tick_interval": Serializer.serialize(self.tick_interval),
            "cause": Serializer.serialize(self.cause),
            "events": Serializer.serialize(self.events),
            "getters": Serializer.serialize(self.getters),
            "is_template": Serializer.serialize(self.is_template)
        }
    
    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)

if __name__ == "__main__":
    print(AbstractStatusEffect.loadData(None))


