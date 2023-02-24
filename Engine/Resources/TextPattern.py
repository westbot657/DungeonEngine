# pylint: disable=[W,R,C,import-error]

import re

from enum import IntEnum

from typing import Any

class TextElement(IntEnum):
    AMMO          = 0b10000_000_0_0_0
    ARMOR         = 0b01000_000_0_0_0
    ITEM          = 0b00100_000_0_0_0
    TOOL          = 0b00010_000_0_0_0
    WEAPON        = 0b00001_000_0_0_0
    GAME_OBJECT   = 0b11111_000_0_0_0

    PLAYER        = 0b00000_100_0_0_0
    ENEMY         = 0b00000_010_0_0_0
    NPC           = 0b00000_001_0_0_0
    ENTITY        = 0b00000_111_0_0_0

    STATUS_EFFECT = 0b00000_000_1_0_0
    ATTACK        = 0b00000_000_0_1_0
    LOCATION      = 0b00000_000_0_0_1


class TextPattern:
    def __init__(self, components:list[TextElement]):
        self.components = components
        
    def _build(self, component:int, text:str) -> tuple[Any, str]:
        return None, text

    def check(self, text:str):
        pieces = []
        for component in self.components:
            piece, text = self._build(component, text)
            pieces.append(piece)

        return pieces





