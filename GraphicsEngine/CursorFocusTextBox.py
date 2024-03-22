# pylint: disable=[W,R,C, import-error, no-member]

from UIElement import UIElement
from MultilineTextBox import MultilineTextBox
from ConstructionCanvas import ConstructionCanvas
from Text import Text

import pygame

class CursorFocusTextBox(UIElement):
    def __init__(self, x, y, width, height, editor, shadow_text="", *args, **kwargs):
        """
        *args and **kwargs are passed to MultilineTextBox, after the `content` paramater  
        """
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.shadow_text = shadow_text
        self.editor = editor
        self.text_box = MultilineTextBox(0, 0, 1, 1, "", *args, **kwargs)
        self.mouse_pos = [0, 0]
        self.screen = pygame.Surface((width, height), pygame.SRCALPHA, 32)



