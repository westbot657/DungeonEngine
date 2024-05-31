# pylint: disable=W,R,C,import-error, no-member


from UIElement import UIElement
from Options import TEXT_COLOR, TEXT_BG_COLOR, TEXT_BG2_COLOR, TEXT_BG3_COLOR

from Text import Text

import pygame
import time
import math

from enum import Enum, auto

class ToggleSwitch(UIElement):
    
    class Style(Enum):
        ROUND = auto()
        SQUARE = auto()
    
    @staticmethod
    def empty_listener(s): pass
    
    def __init__(self, x, y, size, rotation=0, state=False, bg_color=TEXT_BG2_COLOR, on_color=TEXT_BG2_COLOR, off_color=TEXT_BG_COLOR, toggle_color=TEXT_BG3_COLOR, style:Style=Style.ROUND, labeled=False):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.size = size
        self.state = state
        self.bg_color = bg_color
        self.on_color = on_color
        self.off_color = off_color
        self.toggle_color = toggle_color
        self.style = style
        self.transition_time = 0
        self.toggle_pos = 0
        self.hovered = False
        self.labeled = labeled
        self.state_change_listener = ToggleSwitch.empty_listener
        
        if self.rotation == 0:
            self.bg = pygame.Surface((self.size*2, self.size), pygame.SRCALPHA, 32)
            self.fg = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
            
            self._true = Text(self.x + (self.size*2) + 2, self.y, 1, "True", text_size=self.size-4, text_bg_color=None)
            self._false = Text(self.x + (self.size*2) + 2, self.y, 1, "False", text_size=self.size-4, text_bg_color=None)
            self._true.y = self.y - ((self.size - self._true.height) / 2)
            self._false.y = self.y - ((self.size - self._false.height) / 2)
            
            
            if self.style == ToggleSwitch.Style.SQUARE:
                self.bg.fill(self.bg_color)
                self.bg.fill(self.on_color, (1, 1, self.size-1, self.size-2))
                self.bg.fill(self.off_color, (self.size, 1, self.size-1, self.size-2))
                self.fg.fill(self.toggle_color)
            else:
                pygame.draw.circle(self.bg, self.bg_color, (self.size/2, self.size/2), self.size/2)
                pygame.draw.circle(self.bg, self.bg_color, ((self.size/2) + self.size, self.size/2), self.size/2)
                self.bg.fill(self.bg_color, (self.size/2, 0, self.size, self.size))
                pygame.draw.circle(self.bg, self.on_color, (self.size/2, self.size/2), (self.size/2)-1)
                pygame.draw.circle(self.bg, self.off_color, ((self.size/2) + self.size, self.size/2), (self.size/2)-1)

                pygame.draw.circle(self.fg, self.toggle_color, (self.size/2, self.size/2), self.size/2)

        elif self.rotation == 1:
            
            self._true = Text(self.x + 5, self.y + (self.size/4), 1, "True", text_size=self.size-4, text_bg_color=None)
            self._false = Text(self.x + 5, self.y + (self.size/4), 1, "False", text_size=self.size-4, text_bg_color=None)
            self._true.y = self.y - ((self.size - self._true.height) / 2)
            self._false.y = self.y - ((self.size - self._false.height) / 2)
            
            self.bg = pygame.Surface((self.size, self.size*2), pygame.SRCALPHA, 32)
            self.fg = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
            if self.style == ToggleSwitch.Style.SQUARE:
                self.bg.fill(self.bg_color)
                self.bg.fill(self.on_color, (1, 1, self.size-2, self.size-1))
                self.bg.fill(self.off_color, (1, self.size, self.size-2, self.size-1))
                self.fg.fill(self.toggle_color)
            else:
                pygame.draw.circle(self.bg, self.bg_color, (self.size/2, self.size/2), self.size/2)
                pygame.draw.circle(self.bg, self.bg_color, (self.size/2, (self.size/2) + self.size), self.size/2)
                self.bg.fill(self.bg_color, (0, self.size/2, self.size, self.size))
                pygame.draw.circle(self.bg, self.off_color, (self.size/2, self.size/2), (self.size/2)-1)
                pygame.draw.circle(self.bg, self.on_color, (self.size/2, (self.size/2) + self.size), (self.size/2)-1)

                pygame.draw.circle(self.fg, self.toggle_color, (self.size/2, self.size/2), self.size/2)

    def set_state(self, state):
        """
        Sets the state of the object to the specified state.

        Parameters:
            state (bool): The state to set the object to.

        Returns:
            None
        """
        self.state = state
        self.transition_time = time.time()

    def on_state_change(self, callable):
        self.state_change_listener = callable

    def _event(self, editor, X, Y):
        if self.rotation == 0:
            editor._e_instance.check_hover(editor, (X+self.x, Y+self.y, self.size*2, self.size), self)

            if self.hovered:
                if editor.left_mouse_down():
                    self.state = not self.state
                    self.state_change_listener(self.state)
                    self.transition_time = time.time()


        elif self.rotation == 1:
            editor._e_instance.check_hover(editor, (X+self.x, Y+self.y, self.size, self.size*2), self)

            if self.hovered:
                if editor.left_mouse_down():
                    self.state = not self.state
                    self.state_change_listener(self.state)
                    self.transition_time = time.time()
        
        if self.transition_time:
            dt = (time.time() - self.transition_time) * 6
            if dt >= 1:
                self.transition_time = 0
                dt = 1

            if self.state:
                self.toggle_pos = math.sin(math.pi * (dt/2)) * self.size
            else:
                self.toggle_pos = (1 - math.sin(math.pi * (dt/2))) * self.size


    def _update(self, editor, X, Y):
        editor.screen.blit(self.bg, (X+self.x, Y+self.y))
        if self.rotation == 0:
            if self.style == ToggleSwitch.Style.ROUND:
                editor.screen.fill(self.on_color, (X+self.x+self.size/2, Y+self.y+1, self.toggle_pos+(self.size/4), self.size-2))
                editor.screen.fill(self.off_color, (X+self.x+self.toggle_pos+(self.size/2), Y+self.y+1, self.size-self.toggle_pos, self.size-2))
            editor.screen.blit(self.fg, (X+self.x+self.toggle_pos, Y+self.y))

        elif self.rotation == 1:
            editor.screen.blit(self.bg, (X+self.x, Y+self.y))
            if self.style == ToggleSwitch.Style.ROUND:
                editor.screen.fill(self.off_color, (X+self.x+1, Y+self.y+self.size/2, self.size-2, self.toggle_pos+(self.size/2)))
                editor.screen.fill(self.on_color, (X+self.x+1, Y+self.y+self.toggle_pos+(self.size/2), self.size-2, self.size-self.toggle_pos))
            editor.screen.blit(self.fg, (X+self.x, Y+self.y+self.toggle_pos))
        
        if self.labeled:
            if self.state:
                self._true._update(editor, X+self.x, Y+self.y)
            else:
                self._false._update(editor, X+self.x, Y+self.y)