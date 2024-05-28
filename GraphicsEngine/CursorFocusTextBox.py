# pylint: disable=[W,R,C, import-error, no-member]

from UIElement import UIElement
from MultilineTextBox import MultilineTextBox
from ConstructionCanvas import ConstructionCanvas
from Text import Text
from Options import TEXT_BG3_COLOR

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
        self.text_box = MultilineTextBox(1, 1, width, height, *args, **kwargs)
        self.mouse_pos = [0, 0]
        self.screen = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self._canvas = ConstructionCanvas._Canvas(editor, self)
        self.shadow_text_obj = Text(4, 0, 1, self.shadow_text, text_color=TEXT_BG3_COLOR, text_size=self.text_box.text_size, text_bg_color=self.text_box.text_bg_color)
        self.offsetX = 0
        self.last_X = 0
        self.last_Y = 0
        self.focused = False
    
    def on_enter(self, method):
        self.text_box.on_enter(method)
    
    def on_save(self, method):
        self.text_box.on_save(method)
    
    def get_content(self):
        return self.text_box.get_content()

    def set_content(self, content):
        self.text_box.set_content(content)
    
    def clear_selection(self):
        self.text_box.clear_selection()
    
    def unfocus(self):
        self.text_box.unfocus()
    
    def collides(self, mouse, rect) -> bool:
        mx, my = mouse
        x, y, w, h = rect
        #print("Scrollable: v")
        # if self.shadow_text == "enter label...":
        #     _x, _y = self.editor.mouse_pos
        if self.editor.collides(self.editor.mouse_pos, (self.x+self.last_X, self.y+self.last_Y, self.width, self.height)):
            # print("COLLISION")
            #print(f"Scrollable: \033[38;2;20;200;20m{mouse} \033[38;2;200;200;20m{rect}\033[0m")
            # print((x, y, w, h), (mx, my), (self.last_X, self.last_Y))
            if x <= mx < x + w and y <= my < y + h:
                return True

        return False
    
    def set_text_color(self, color):
        self.text_box.set_text_color(color)
    
    def override_values(self, X, Y):
        self.mouse_pos = list(self.editor.mouse_pos)
        self.mouse_pos[0] -= self.x + X
        self.mouse_pos[1] -= self.y + Y
        self.last_X = X
        self.last_Y = Y
    
    def _event(self, editor, X, Y):
        self.editor = editor
        self.override_values(X, Y)
        
        self.text_box._event(self._canvas, self.offsetX, 0)
        self.focused = self.text_box.focused

        cursor_x = self.text_box.cursor_location.col * self.text_box._width
        
        # if self.shadow_text == "enter label...":
        #     print(editor.mouse_pos, self.x, self.y, self.width, self.height, self.text_box.hovered)
        
        # self.offsetX needs to be <= 0
        
        leftX = -self.offsetX
        rightX = (-self.offsetX)+self.width
        
        if not (leftX + (self.text_box._width*2) < cursor_x < rightX - (self.text_box._width*2)):
            if leftX + (self.text_box._width*2) > cursor_x:
                dx = (leftX + (self.text_box._width*2)) - cursor_x
                self.offsetX = min(self.offsetX + dx, 0)
            if cursor_x > rightX - (self.text_box._width*2):
                dx = (rightX - (self.text_box._width*2)) - cursor_x
                self.offsetX = min(self.offsetX + dx, self.text_box._text_width)

    def _update(self, editor, X, Y):
        self.screen.fill((0, 0, 0, 0))
        self.text_box._update(self._canvas, self.offsetX, 0)
        
        if not self.text_box.get_content():
            self.shadow_text_obj._update(self._canvas, self.offsetX, 0)
        
        editor.screen.blit(self.screen, (X+self.x, Y+self.y))


