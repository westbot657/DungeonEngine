# pylint: disable=[W,R,C,import-error]

try:
    from .EngineDummy import Engine
    from .Identifier import Identifier
    from .EngineErrors import LocationError
except ImportError:
    from EngineDummy import Engine
    from Identifier import Identifier
    from EngineErrors import LocationError

import re

class Location:

    def __init__(self, dungeon:str, room_path:str, room:str):
        self.dungeon = dungeon
        self.room_path = room_path
        self.room = room

    def full(self):
        if self.room_path == self.room == "":
            return self.dungeon
        return f"{self.dungeon}:{self.room_path}{self.room}"

    def fullWith(self, **kwargs):
        return f"{kwargs.get('dungeon', self.dungeon)}:{kwargs.get('room_path', self.room_path)}{kwargs.get('room', self.room)}".strip(":")

    def setLocation(self, location):
        location: Location
        self.dungeon = location.dungeon
        self.room_path = location.room_path
        self.room = location.room

    def __eq__(self, other):
        if isinstance(other, str):
            try:
                other = Location.fromString(other)
            except LocationError:
                return False
        if not isinstance(other, Location): return False
        if self.full() == other.full():
            return True

    def __repr__(self):
        return self.full()

    @classmethod
    def fromString(cls, location:str):
        if isinstance(location, Location): return location
        if m := re.match(r"(?P<dungeon>[a-z_][a-z0-9_]*):(?P<room_path>(?:rooms/)?(?:[a-z_][a-z0-9_]*/)*)(?P<room>[a-z_][a-z0-9_]*)", location):
            d = m.groupdict()
            dungeon = d.get("dungeon", "")
            room_path = d.get("room_path", "")
            room = d.get("room", "")
            return cls(dungeon, room_path, room)

        elif m := re.match(r"(?P<dungeon>[a-z_][a-z0-9_])", location):
            d = m.groupdict()
            dungeon = d.get("dungeon")
            return cls(dungeon, "", "")

        else:
            raise LocationError(f"Unknown Location format: '{location}'")

    def _get_save(self, function_memory):
        return self.full()
