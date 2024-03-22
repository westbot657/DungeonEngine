# pylint: disable=[W,R,C, import-error, no-member]

from UIElement import UIElement
from AttributePanel import AttributePanel
from ConstructionCanvas import ConstructionCanvas
from Options import SCROLL_MULTIPLIER

import pygame

class PanelTree(UIElement):
    
    def __init__(self, x, y, width, height, editor):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tree = []
        self.screen = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.mouse_pos = [0, 0]
        self.editor = editor
        self._canvas = ConstructionCanvas._Canvas(editor, self)
        self.offsetY = 0
        self.content_height = 0
        self._search = ""
    
    def get_search(self):
        return ""
    
    def override_values(self):
        self.mouse_pos = list(self.editor.mouse_pos)
        self.mouse_pos[0] -= self.x
        self.mouse_pos[1] -= self.y# - self.offsetY
        
    def _update_layout(self, editor):
        self.screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        
    
    def _event(self, editor, X, Y):
        y = 0
        mx, my = editor.mouse_pos
        if editor._do_layout_update:
            self._update_layout(editor)
        self.override_values()
        
        if editor.collides((mx, my), (self.x, self.y, self.width, self.height)):
            if editor.scroll != 0:
                self.offsetY = min(max(-self.content_height, self.offsetY + 0.5*SCROLL_MULTIPLIER*editor.scroll), 0)
        
        self._search = self.get_search()
        
        last = None
        for obj in self.tree:
            if obj.label.contains(self._search):
                obj._event(self._canvas, 5, y+self.offsetY)
                y += obj.effective_height + 5
                last = obj
        self.content_height = y-((last.effective_height)+5 if last else 0)
        
    
    def _update(self, editor, X, Y):
        y = 0
        
        self.screen.fill((0, 0, 0, 0))
        
        for obj in self.tree:
            if obj.label.contains(self._search):
                obj._update(self._canvas, 5, y+self.offsetY)
                y += obj.effective_height + 5
        editor.screen.blit(self.screen, (self.x, self.y))
    

