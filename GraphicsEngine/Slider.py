# pylint: disable=W,R,C,import-error


from UIElement import UIElement
from Options import TEXT_COLOR, TEXT_BG2_COLOR, TEXT_BG3_COLOR
from Organizers import Draggable
from RenderPrimitives import Image

import pygame

class Slider(UIElement):
    
    def __init__(self, x:int, y:int, length:int, orientation:int, start_point:float, thickness=3, bg_color=TEXT_BG2_COLOR, fg_color=TEXT_BG3_COLOR, drag_color=TEXT_COLOR):
        self.x = x
        self.y = y
        self.length = length
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.orientation = orientation
        self.thickness = thickness
        self.pos = start_point
        self.drag_color = drag_color
        
        if self.orientation == 0: # horizontal
            s = pygame.Surface((6, thickness+4))
            s.fill(self.drag_color)
            self._drag_surface = Image.from_pygameSurface(s)
            self.bg = pygame.Surface((length, thickness))
            self.fg = pygame.Surface((1, thickness))
            self.drag = Draggable(self.x+(length*start_point)-3, self.y-2, 6, thickness+4, False, True, [self._drag_surface])
        else: # vertical
            s = pygame.Surface((thickness+4, 5))
            s.fill(self.drag_color)
            self._drag_surface = Image.from_pygameSurface(s)
            self.bg = pygame.Surface((thickness, length))
            self.fg = pygame.Surface((thickness, 1))
            self.drag = Draggable(self.x-2, self.y+(length*start_point)-3, thickness+4, 6, True, False, [self._drag_surface])
        
        self.drag.ignore_child_hovering = True
        self.bg.fill(self.bg_color)
        self.fg.fill(self.fg_color)
    
    def get_percent(self):
        return self.pos
    
    def set_percent(self, percent:float):
        self.pos = percent
        self.drag.x = self.x-3 + (self.length*self.pos)
    
    def _event(self, editor, X, Y):
        self.drag._event(editor, X, Y)
        if self.orientation == 0:
            self.drag.x = min(max(self.x, self.drag.x+3), self.x+self.length)-3
            self.pos = ((self.drag.x+3)-self.x) / (self.length)
            self.fg = pygame.transform.scale(self.fg, (max(self.length*self.pos, 1), self.thickness))
        if self.orientation == 1:
            self.drag.y = min(max(self.y, self.drag.y+3), self.y+self.length)-3
            self.pos = 1-((self.drag.y+3)-self.y) / (self.length)
            self.fg = pygame.transform.scale(self.fg, (self.thickness, max(1, self.length*self.pos)))
    
    def _update(self, editor, X, Y):
        editor.screen.blit(self.bg, (X+self.x, Y+self.y))
        editor.screen.blit(self.fg, (X+self.x, Y+self.y+(self.length*self.pos*self.orientation)))
        self.drag._update(editor, X, Y)

