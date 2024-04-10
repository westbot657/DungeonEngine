# pylint: disable=W,R,C,import-error

from UIElement import UIElement
from Options import TEXT_COLOR, TEXT_BG_COLOR

import pygame

class LoadingBar(UIElement):
    
    
    
    def __init__(self, x, y, width, height, max_progress=100, load_direction=0, fill_color=TEXT_COLOR, bg_color=TEXT_BG_COLOR):
        self.x = x
        self.y = y
        self.width = self._width = width
        self.height = self._height = height
        self.progress = 0
        self.max_progress = max_progress
        self.load_direction = load_direction
        self.fill_color = fill_color
        self.bg_color = bg_color
        self.surface = pygame.Surface((self.width, self.height))
        match load_direction:
            case 0: # left -> right
                self.load_x = 0
                self.load_y = 0
                self.load_width = 0
                self.load_height = self.height
            case 1: # up -> down
                self.load_x = 0
                self.load_y = 0
                self.load_width = self.width
                self.load_height = 0

    def set_progress(self, progress):
        self.progress = progress
        match self.load_direction:
            case 0: # left -> right
                self.load_width = (self.progress/self.max_progress)*self.width
            case 1: # up -> down
                self.load_height = (self.progress/self.max_progress)*self.height
    
    def set_max_progress(self, progress):
        self.max_progress = progress
        
        
    def _event(self, editor, X, Y):
        if self._width != self.width or self._height != self.height:
            self._width = self.width
            self._height = self.height
            self.surface = pygame.Surface((self.width, self.height))

    def _update(self, editor, X, Y):
        self.surface.fill(self.bg_color)
        self.surface.fill(self.fill_color, (self.load_x, self.load_y, self.load_width, self.load_height))
        
        editor.screen.blit(self.surface, (X+self.x, Y+self.y))