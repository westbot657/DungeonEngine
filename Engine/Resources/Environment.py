# pylint: disable=[W,R,C,import-error]


# This is used to store info on a location like:
# humidity
# temperature
# what can live where
# other descriptors, made as needed

class Environment:

    def __init__(self, stats:dict):
        self.stats = stats
        self.parent: Environment|None = None

    def check(self, other_environment:dict):
        for key, value in other_environment.items():
            if key in self.stats:
                if value != self.stats[key]:
                    return False
            elif self.parent and (key in self.parent.stats):
                if not self.parent._comp(key, value):
                    return False
            else:
                return False
        return True

    def _comp(self, key, value):
        if key in self.stats:
            return self.stats[key] == value
        elif self.parent:
            return self.parent._comp(key, value)
        return False