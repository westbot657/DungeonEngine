# pylint: disable=[W,R,C,import-error]

import re

from enum import IntEnum

class TextElement(IntEnum):

    #                 1 #####
    GAME_OBJECT   = 0x1_00000_0_000_0_0_0

    AMMO          = 0x1_10000_0_000_0_0_0
    ARMOR         = 0x1_01000_0_000_0_0_0
    WEAPON        = 0x1_00100_0_000_0_0_0
    ITEM          = 0x1_00010_0_000_0_0_0
    TOOL          = 0x1_00001_0_000_0_0_0

    #                         1 ###
    ENTITY        = 0x0_00000_1_000_0_0_0

    PLAYER        = 0x0_00000_1_100_0_0_0
    ENEMY         = 0x0_00000_1_010_0_0_0
    NPC           = 0x0_00000_1_001_0_0_0
    
    #                               # # #
    LOCATION      = 0x0_00000_0_000_1_0_0

    STATUS_EFFECT = 0x0_00000_0_000_0_1_0

    ATTACK        = 0x0_00000_0_000_0_0_1
    

class TextPattern:

    def __init__(self, *components):
        self.components = components


