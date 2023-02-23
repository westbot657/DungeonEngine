# pylint: disable=[W,R,C,import-error]

import re

from enum import Enum, auto

from typing import Any

class _TextElementType(Enum):
    AMMO = auto()
    ARMOR = auto()
    ITEM = auto()
    TOOL = auto()
    WEAPON = auto()
    GAME_OBJECT = auto()

    PLAYER = auto()
    ENEMY = auto()
    ENTITY = auto()

    ATTACK = auto()
    LOCATION = auto()
    STATUS_EFFECT = auto()

class TextElement:
    def __init__(self, types):
        self.types = list(types)
    
    def __or__(self, other):
        if isinstance(other, TextElement):
            return TextElement(self.types + other.types)
        raise TypeError(f"unsupported operand type(s) for |: 'TextElement' and '{type(other)}'")

    def check(self, text:str) -> tuple[Any, str]:
        ...

class TextPattern:

    def __init__(self, *components):
        self.components: list[TextElement|str] = list(components)

    def check(self, text:str) -> list[Any]:
        ...
