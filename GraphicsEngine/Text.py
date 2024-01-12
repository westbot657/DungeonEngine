# pylint: disable=W,R,C

from UIElement import UIElement
from RenderPrimitives import Color
from Options import TEXT_COLOR, TEXT_BG_COLOR, TEXT_SIZE, FONT

import pygame

class Text(UIElement):
    __slots__ = [
        "x", "y", "content", "_content",
        "min_width", "text_color", "text_bg_color",
        "text_size", "font", "surface", "width", "height"
    ]

    def __init__(self, x:int, y:int, min_width:int=1, content:str="", text_color:Color|tuple|int=TEXT_COLOR, text_bg_color:Color|tuple|int=TEXT_BG_COLOR, text_size:int=TEXT_SIZE):
        assert min_width >= 1, "Min width must be 1 or more"
        self.x = x
        self.y = y
        self.content = self._content = content
        self.min_width = min_width
        self.text_color = Color.color(text_color)
        self.text_bg_color = Color.color(text_bg_color)
        self.text_size = text_size
        self.font = pygame.font.Font(FONT, text_size)
        self.surface = self.font.render(self.content, True, tuple(self.text_color))
        self.width, self.height = self.surface.get_size()

    def set_text(self, text:str):
        self.content = text

    def _event(self, *_):
        if self.content != self._content:
            self._content = self.content
            self.surface = self.font.render(self.content, True, tuple(self.text_color))
            self.width = self.surface.get_width()
        
    def _update(self, editor, X, Y):
        _x, _y = self.surface.get_size()
        if self.text_bg_color:
            editor.screen.fill(tuple(self.text_bg_color), (X+self.x-1, Y+self.y-1, max(_x, self.min_width)+2, _y+2))
        editor.screen.blit(self.surface, (X+self.x, Y+self.y))

