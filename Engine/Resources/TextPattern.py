# pylint: disable=[W,R,C,import-error]

import re

from enum import Enum


class _TEValue:
    def __init__(self, parent_TEValue=None):
        self.parent_TEValue = parent_TEValue

    def isParentOf(self, possible_child):
        parent = possible_child
        while parent is not None:
            if parent is self:
                return True

            parent = parent.parent_TEValue
        return False

    def __eq__(self, other):
        return self is other

    def __gt__(self, other):
        if self is other: return False
        return self.isParentOf(other)

    def __ge__(self, other):
        return self.isParentOf(other)
    
    def __lt__(self, other):
        if self is other: return False
        return other.isParentOf(self)
    
    def __le__(self, other):
        return other.isParentOf(self)

    def __ne__(self, other):
        return self is not other

    def __or__(self, other): # binary or: x | y
        ...

class TextElement(Enum):

    GAME_OBJECT = _TEValue()

    AMMO = _TEValue(GAME_OBJECT)
    ARMOR = _TEValue(GAME_OBJECT)
    WEAPON = _TEValue(GAME_OBJECT)
    ITEM = _TEValue(GAME_OBJECT)
    TOOL = _TEValue(GAME_OBJECT)

    ENTITY = _TEValue()

    PLAYER = _TEValue(ENTITY)
    ENEMY = _TEValue(ENTITY)
    NPC = _TEValue(ENTITY)
    
    LOCATION = _TEValue()

    STATUS_EFFECT = _TEValue()

    ATTACK = _TEValue()

class TextPattern:

    def __init__(self, *components):
        self.components: list[TextElement|str] = list(components)

    


