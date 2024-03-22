# pylint: disable=[W,R,C, import-error, no-member]

from UIElement import UIElement
from MultilineTextBox import MultilineTextBox
from ConstructionCanvas import ConstructionCanvas
from Text import Text

import pygame

class CursorFocusTextBox(UIElement):
    def __init__(self, x, y, width, height, editor, shadow_text="", *args, **kwargs):
        """
        *args and **kwargs are passed to MultilineTextBox, after the `content` paramater, and ignoring the single_line option  
        """
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.shadow_text = shadow_text
        self.editor = editor
        kwargs.update({"single_line": True})
        self.text_box = MultilineTextBox(0, 0, 1, 1, "", *args, **kwargs)
        self.mouse_pos = [0, 0]
        self.screen = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self._canvas = ConstructionCanvas._Canvas(editor, self)
        
        self.offsetX = 0
    
    def on_enter(self, method):
        self.text_box.on_enter(method)
    
    def on_save(self, method):
        self.text_box.on_save(method)
    
    def get_content(self):
        return self.text_box.get_content()
    
    def _event(self, editor, X, Y):
        ...
    
    def _update(self, editor, X, Y):
        ...


