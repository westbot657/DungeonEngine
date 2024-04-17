# pylint: disable=[W,R,C,import-error]


# This is used to store info on a location like:
# humidity
# temperature
# what can live where
# other descriptors, made as needed

from Util import Util
from Serializer import Serializer, Serializable
    

@Serializable("Environment")
class Environment:

    def __init__(self, stats:dict):
        self.stats = stats
        self.parent: Environment|None = None

    def serialize(self):
        return {
            "stats": Serializer.serialize(self.stats),
            "parent": Serializer.serialize(self.parent)
        }
    
    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)

    def setParent(self, environment):
        self.parent = environment

    def check(self, other_environment:dict):
        """
        This checks that this Environment contains every stat specified by `other_environment`.
        If `other_environment` contains a stat that this environment does not, the check will fail.
        this environment may have more stats than `other_environment` without affecting the check.
        """
        #print(f"environment check:\nself: {self.stats}\nother: {other_environment}")
        for key, value in other_environment.items():
            if key in self.stats:
                if value != self.stats[key]:
                    return False
            elif self.parent and (key in self.parent.stats):
                if not self.parent._comp(key, value):
                    return False
            elif value is True:
                return False
        return True

    def _comp(self, key, value):
        if key in self.stats:
            return self.stats[key] == value
        elif self.parent:
            return self.parent._comp(key, value)
        return False

    def __add__(self, other):
        d = Util.deepCopy(self.stats)
        d.update(Util.deepCopy(other.stats))
        return Environment(d)

    def __eq__(self, other):
        if isinstance(other, Environment):
            return self.stats == other.stats
        elif isinstance(other, dict):
            return self.stats == other

    def _load_from(self, function_memory, stats):
        self.stats = stats

    def _get_save(self, function_memory):
        return self.stats

