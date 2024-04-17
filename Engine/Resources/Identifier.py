# pylint: disable=[W,R,C,import-error]

from .EngineErrors import IdentifierError
from .Serializer import Serializer, Serializable


import re

@Serializable("Identifier")
class Identifier:
    def __init__(self, namespace:str, path:str, name:str|None=None):
        self.namespace = namespace
        self.path = path
        self.name = name

    def serialize(self):
        return {
            "namespace": Serializer.serialize(self.namespace),
            "path": Serializer.serialize(self.path),
            "name": Serializer.serialize(self.name)
        }
    
    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)

    def ID(self):
        return f"{self.namespace}:{self.name}" if self.name else f"{self.namespace}"

    def full(self):
        return f"{self.namespace}:{self.path}{self.name}"

    def fullWith(self, **kwargs):
        return f"{kwargs.get('namespace', self.namespace)}:{kwargs.get('path', self.path)}{kwargs.get('name', self.name)}"

    def __repr__(self):
        if self.name:
            return f"{self.namespace}:{self.name} ({self.path})"
        else:
            return f"{self.namespace} ({self.path})"

    def __eq__(self, other):
        if isinstance(other, str):
            try:
                other = Identifier.fromString(other)
            except IdentifierError:
                return False
        if not isinstance(other, Identifier): return False
        if self.full() == other.full():
            return True

    @classmethod
    def fromString(cls, string:str):
        if isinstance(string, Identifier): return string
        if m := re.match(r"(?P<namespace>[a-z_][a-z0-9_]*):(?P<path>(?:(?:[a-z_][a-z0-9_]*)/)*)(?P<name>[a-z][a-z0-9_]*)", string):
            d = m.groupdict()
            namespace = d.get("namespace", "")
            path = d.get("path", "")
            name = d.get("name", "")
            return cls(namespace, path, name)
        raise IdentifierError(f"Unknown identifier format: '{string}'")
    
    @classmethod
    def fromFile(cls, file_name):
        if isinstance(file_name, Identifier): return file_name
        if m := re.match(r"resources/(?P<path>[a-z_][a-z0-9_]*/)(?P<name>[a-z_][a-z0-9_]*).json", file_name.replace("\\", "/")):
            d = m.groupdict()
            namespace = "engine"
            path = d.get("path", "")
            name = d.get("name", "")

        elif m := re.match(r"Dungeons/(?P<namespace>[a-z_][a-z0-9_]*)/resources/(?P<path>[a-z_][a-z0-9_]*/)(?P<name>[a-z_][a-z0-9_]*).json", file_name.replace("\\", "/")):
            d = m.groupdict()
            namespace = d.get("namespace", "")
            path = d.get("path", "")
            name = d.get("name", "")

        elif m := re.match(r"Dungeons/(?P<dungeon_name>[a-z_][a-z0-9_]*)/(?P<path>rooms/([a-z_][a-z0-9_]*/)*)(?P<name>[a-z_][a-z0-9_]*).json", file_name.replace("\\", "/")):
            d = m.groupdict()
            namespace = d.get("dungeon_name", "")
            path = d.get("path", "")
            name = d.get("name", "")

        elif m := re.match(r"Dungeons/(?P<dungeon_name>[a-z_][a-z0-9_]*)/(?P<path>combats/([a-z_][a-z0-9_]*/)*)(?P<name>[a-z_][a-z0-9_]*).json", file_name.replace("\\", "/")):
            d = m.groupdict()
            namespace = d.get("dungeon_name", "")
            path = d.get("path", "")
            name = d.get("name", "")

        else:
            raise IdentifierError(f"Unknown identifier format: '{file_name}'")
        return cls(namespace, path, name)
