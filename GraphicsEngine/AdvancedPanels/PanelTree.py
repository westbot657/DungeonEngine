# pylint: disable=[W,R,C, import-error, no-member]

from UIElement import UIElement
from AttributePanel import AttributePanel
from ConstructionCanvas import ConstructionCanvas
from Options import SCROLL_MULTIPLIER, PATH
from SoundSystem import SoundSystem

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
        self._y = 0
        self.last_X = 0
        self.last_Y = 0
    
    def get_search(self): # this method gets overwritten
        return ""
    
    def collides(self, mouse, rect) -> bool:
        mx, my = mouse
        x, y, w, h = rect
        #print("Scrollable: v")
        
        if self._canvas._editor.collides(self.editor.mouse_pos, (self.x, self.y, self.width, self.height)):
            #print(f"Scrollable: \033[38;2;20;200;20m{mouse} \033[38;2;200;200;20m{rect}\033[0m")
            # print((x, y, w, h), (mx, my-self.offsetY))
            if x <= mx < x + w and y <= my < y + h:
                return True

        return False
    
    def override_values(self, X, Y):
        self.mouse_pos = list(self.editor.mouse_pos)
        self.mouse_pos[0] -= self.x+5
        self.mouse_pos[1] -= self.y
        
    def _update_layout(self, editor):
        self.screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        
    
    def _event(self, editor, X, Y):
        self._y = 0
        mx, my = editor.mouse_pos
        if editor._do_layout_update:
            self._update_layout(editor)
        self.override_values(X, Y)
        
        if editor.collides((mx, my), (self.x, self.y, self.width, self.height)):
            if editor.scroll != 0:
                self.offsetY = min(max(-self.content_height, self.offsetY + 0.5*SCROLL_MULTIPLIER*editor.scroll), 0)
        
        self._search = self.get_search().lower()
        
        last = None
        for obj in self.tree:
            if (self._search in obj.label.lower()) or any(tag.startswith(self._search) for tag in obj.tags):
                obj._event(self._canvas, 5, self._y + self.offsetY)
                # self.mouse_pos[1] -= obj.effective_height+5
                self._y += obj.effective_height + 5
                last = obj
            
        self.content_height = self._y-((last.effective_height)+5 if last else 0)
        
    
    def _update(self, editor, X, Y):
        y = 0
        
        self.screen.fill((0, 0, 0, 0))
        
        for obj in self.tree:
            if (self._search in obj.label.lower()) or any(tag.startswith(self._search) for tag in obj.tags):
                # self.mouse_pos[1] += obj.effective_height+5
                
                obj._update(self._canvas, 5, y+self.offsetY)
                y += obj.effective_height + 5
        editor.screen.blit(self.screen, (self.x, self.y))
    

