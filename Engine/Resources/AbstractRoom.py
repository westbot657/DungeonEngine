# pylint: disable=[W,R,C,import-error]

try:
    from .Room import Room
    from .Identifier import Identifier
except ImportError:
    from Room import Room
    from Identifier import Identifier

import glob, json, re

class AbstractRoom:
    _loaded = {}
    _link_parents = []

    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data
        self.parent: AbstractRoom|None = None
        self.children: list[AbstractRoom] = []
        
        if "parent" in data:
            AbstractRoom._link_parents.append((self, data["parent"]))

        self.name: str = data.get("name", None)
        self.enter_message: str|dict = data.get("enter_message", None)
        self.exit_message: str|dict = data.get("exit_message", None)
        self.interactions: list = data.get("interactions", [])

    def _set_parent(self, parent):
        self.parent = parent
        parent.children.append(self)

    @classmethod
    def loadData(cls, dungeon_name:str, inline_handler):
        ...

    @classmethod
    def finishRoomLoading(cls):
        for room, parent_name in cls._link_parents:
            if parent_room := cls._loaded.get(parent_name, None):
                room._set_parent(parent_room)
            else:
                print(f"Failed to load parent room of '{room.identifier.ID()}': '{parent_name}'")
                cls._loaded.pop(room.identifier.ID())
                continue

