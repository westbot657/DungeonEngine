# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
    from .DynamicValue import DynamicValue
    from .FunctionMemory import FunctionMemory
    from .Serializer import Serializer, Serializable
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier
    from DynamicValue import DynamicValue
    from FunctionMemory import FunctionMemory
    from Serializer import Serializer, Serializable


@Serializable("Ammo")
class Ammo(GameObject):
    identifier = Identifier("engine", "object/", "ammo")
    def __init__(self, abstract, name:str, description:str, bonus_damage:DynamicValue, max_count:int, count:int=None):
        self.abstract = abstract
        self.name = name
        self.description = description
        self.bonus_damage = bonus_damage
        self.max_count = max_count
        self.count = count or max_count # this will make None and 0 set the amount to max (0 is included so that you can't have a stack of no ammo)

        self.owner = None

    def __repr__(self):
        return f"Ammo {self.name}: bonus-damage:{self.bonus_damage} max-count:{self.max_count}"

    def can_stack(self, other):
        other: Ammo
        return self.abstract is other.abstract and self.name == other.name and self.description == other.description and self.max_count == other.max_count and self.bonus_damage == other.bonus_damage

    def stack(self, other) -> bool:
        other: Ammo
        """returns whether `other` should be deleted after trying to stack"""
        if self.can_stack(other):
            if self.max_count <= 0:
                self.count += other.count
                return True
            
            diff = self.max_count - self.count
            
            c = other.count
            other.count = max(0, other.count - diff)
            d = c - other.count
            
            self.count += d
            
            return other.count <= 0

    def fullStats(self, function_memory:FunctionMemory, is_equipped=False):
        return f"{self.name} +{self.bonus_damage.fullDisplay(function_memory)}dmg {self.count}/{self.max_count}" + (f" \"{self.description}\"" if self.description else "") + (" [EQUIPPED]" if is_equipped else "")

    def quickStats(self, function_memory:FunctionMemory):
        return f"{self.name} {self.count}/{self.max_count}"

    def getLocalVariables(self) -> dict:
        return {
            ".name": self.name,
            ".description": self.description,
            ".bonus_damage": self.bonus_damage,
            ".max_count": self.max_count,
            ".count": self.count
        }

    def updateLocalVariables(self, locals: dict):
        ...
        if n := locals.get(".name", None):
            if isinstance(n, str) and n.strip() != self.name:
                self.name = n.strip()
        
        if n := locals.get(".description", None):
            if isinstance(n, str) and n.strip() != self.description:
                self.description = n.strip()
        
        if n := locals.get(".count", None):
            if isinstance(n, int) and n != self.count:
                self.count = n

    def prepFunctionMemory(self, function_memory:FunctionMemory):
        function_memory.addContextData({
            "#ammo": self
        })
        function_memory.update(self.getLocalVariables())

    def postEvaluate(self, function_memory:FunctionMemory):
        ... # self.updateLocalVariables(function_memory.symbol_table)

    def onHit(self, function_memory:FunctionMemory):
        ...
    
    def onMiss(self, function_memory:FunctionMemory):
        ...

    def _get_save(self, function_memory:FunctionMemory):
        d = {
            "type": "engine:ammo",
            "parent": self.abstract.identifier.full()
        }

        if self.name != self.abstract.getName():
            d.update({"name": self.name})
        if self.description != self.abstract.getDescription():
            d.update({"description": self.description})
        if self.bonus_damage != self.abstract.getBonusDamage():
            d.update({"bonus_damage": self.bonus_damage})
        if self.max_count != self.abstract.getMaxCount():
            d.update({"max_count": self.max_count})
        if self.count != self.abstract.getCount():
            d.update({"count": self.count})
        return d

    def serialize(self):
        return {
            "abstract": Serializer.serialize(self.abstract),
            "name": Serializer.serialize(self.name),
            "description": Serializer.serialize(self.description),
            "bonus_damage": Serializer.serialize(self.bonus_damage),
            "max_count": Serializer.serialize(self.max_count),
            "count": Serializer.serialize(self.count),
            "owner": Serializer.serialize(self.owner)
        }
    
    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)
