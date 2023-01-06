# pylint: disable=[W,R,C,import-error]

class Identifier:
    def __init__(self, namespace:str, path:str, name:str):
        self.namespace = namespace
        self.path = path
        self.name = name

    def __repr__(self):
        return f"{self.namespace}:{self.name} ({self.path})"

    
