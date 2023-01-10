# pylint: disable=[W,R,C,import-error]

class Identifier:
    def __init__(self, namespace:str, path:str, name:str|None=None):
        self.namespace = namespace
        self.path = path
        self.name = name

    def ID(self):
        return f"{self.namespace}:{self.name}" if self.name else f"{self.namespace}"

    def __repr__(self):
        if self.name:
            return f"{self.namespace}:{self.name} ({self.path})"
        else:
            return f"{self.namespace} ({self.path})"

    
