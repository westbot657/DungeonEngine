# pylint: disable=W,R,C,import-error

from UIElement import UIElement
from Text import Text
from CursorFocusTextBox import CursorFocusTextBox
from ConstructionCanvas import ConstructionCanvas
from Options import TEXT_BG_COLOR, TEXT_BG2_COLOR


import pygame

class SettingsApp(UIElement):
    def __init__(self, code_editor, editor):
        self.code_editor = code_editor
        self.children = []
        self._canvas = ConstructionCanvas._Canvas(editor, self)
        self.screen = pygame.Surface((editor.width-50, editor.height-40))
        self.center = self.screen.get_width()/2
        
        self.show_scrollbar = False
        self.scroll_bg = TEXT_BG2_COLOR
        self.scroll_bar_color = (100, 100, 100)
        self.scroll_bar_hover_color = (120, 120, 120)
        self.scroll_bar_click_color = (140, 140, 140)
        self.scroll_bar_height = 0
        self.scroll_bar_y = 0
        self.scroll_click_offset = 0
        self.scroll_target = 0
        self.scroll_clicked = False
        self.scroll_bar_width = 14 # this is the width of the full area where the scroll bar is, the bar itself will visibly be 2px thinner on each side (but will collide 1px thinner)
        self.scroll_visibility_inset = 2
        self.scroll_collision_inset = 1
        self.scroll_dragging = False
        self.scroll_hovered = False
        
        y_offset = 20
        
        self.general_settings_label = Text(20, y_offset, 1, "General Settings", text_size=30)
        self.children.append(self.general_settings_label)
        y_offset += self.general_settings_label.height + 10
        
        
        
        self.x = 50
        self.y = 20
        self.width = editor.width - 50
        self.height = editor.height - 40
        
        self.settings_height = max(0, y_offset-self.height)
        self.mouse_pos = [0, 0]
        self.scroll = 0
        
    def _update_layout(self, editor):
        self.width = editor.width - 50
        self.height = editor.height - 40
        self.screen = pygame.Surface((self.width, self.height))
        self.center = self.screen.get_width()/2

        
        
    def override_values(self, editor):
        self.mouse_pos = list(editor.mouse_pos)
        self.mouse_pos[0] -= self.x - self.scroll
        self.mouse_pos[1] -= self.y
        
    def _event(self, editor, X, Y):
        self.override_values(editor)
        
        for child in self.children[::-1]:
            child._event(self._canvas, 0, -self.scroll)
            
        if editor.collides(editor.mouse_pos, (self.x, self.y, self.width, self.height)): ...
        
    def _update(self, editor, X, Y):
        self.screen.fill(TEXT_BG_COLOR)

        for child in self.children:
            child._update(self._canvas, 0, -self.scroll)

        editor.screen.blit(self.screen, (self.x, self.y))
        
        
        if self.show_scrollbar:
            editor.screen.fill(self.scroll_bg, ((self.x+self.width)-self.scroll_bar_width+self.scroll_collision_inset-4, self.y, self.scroll_bar_width-(2*self.scroll_collision_inset), self.height))
            editor.screen.fill((self.scroll_bar_click_color if self.scroll_dragging else (self.scroll_bar_hover_color if self.scroll_hovered else self.scroll_bar_color)), ((self.x+self.width)-self.scroll_bar_width+self.scroll_visibility_inset-4, self.y+self.scroll_bar_y, self.scroll_bar_width-(2*self.scroll_visibility_inset), self.scroll_bar_height))
        
        