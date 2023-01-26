# pylint: disable=[W,R,C,import-error]

import re

class Identifier:
    def __init__(self, namespace:str, path:str, name:str|None=None):
        self.namespace = namespace
        self.path = path
        self.name = name

    def ID(self):
        return f"{self.namespace}:{self.name}" if self.name else f"{self.namespace}"

    def full(self):
        return f"{self.namespace}:{self.path}{self.name}"

    def __repr__(self):
        if self.name:
            return f"{self.namespace}:{self.name} ({self.path})"
        else:
            return f"{self.namespace} ({self.path})"


    @classmethod
    def fromString(cls, string):
        if m := re.match(r"(?P<namespace>[a-z_][a-z0-9_]*):(?P<path>(?:(?:[a-z_][a-z0-9_]*)/)*)(?P<name>[a-z][a-z0-9_]*)", string):
            d = m.groupdict()
            namespace = d.get("namespace", "")
            path = d.get("path", "")
            name = d.get("name", "")
            return cls(namespace, path, name)
    
    @classmethod
    def fromFile(cls, file_name):
        if m := re.match(r"resources/(?P<path>[a-z_][a-z0-9_]*/)(?P<name>[a-z_][a-z0-9_]*).json", file_name):
            d = m.groupdict()
            namespace = "engine"
            path = d.get("path", "")
            name = d.get("name", "")
        
        elif m := re.match(r"Dungeons/(?P<namespace>[a-z_][a-z0-9_]*)/resources/(?P<path>[a-z_][a-z0-9_]*/)(?P<name>[a-z_][a-z0-9_]*).json", file_name):
            d = m.groupdict()
            namespace = d.get("namespace", "")
            path = d.get("path", "")
            name = d.get("name", "")
        else:
            print(f"Unknown identifier format: '{file_name}'")
            return None
        return cls(namespace, path, name)
