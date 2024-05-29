# pylint: disable=W,R,C,import-error

from UIElement import UIElement

from ConstructionCanvas import ConstructionCanvas
from MultilineTextBox import MultilineTextBox
from Options import TEXT_COLOR, TEXT_SIZE, TEXT_BG_COLOR, TEXT_BG2_COLOR, TEXT_BG3_COLOR, SCROLL_MULTIPLIER
from FunctionalElements import BorderedButton
from FileEditor import FileEditor
from MultilineText import MultilineText
from NumberedTextArea import NumberedTextArea

import pygame
import os

"""
- multiline text box
- scroll matches the concept art
- reference tabs that also match concept art
- may need to be a full re-implementation of the text box...
"""

class PanelTextBox(UIElement):
    
    def __init__(self, x, y, width, height, scroll_height, file_path, editor):
        self.editor = editor
        self.x = x
        self.y = y
        self.width = self._width = width
        self.height = self._height = height
        self.file_path = file_path
        
        self.text_box = MultilineTextBox(5, 0, width-5, height, text_bg_color=TEXT_BG2_COLOR)
        self.text_box.on_save(self.on_save)
        
        self.open_button = BorderedButton(0, 0, -1, 20, " Open File ")
        self.open_button.x = (self.width-self.open_button.width)/2
        self.open_button.y = (self.height-self.open_button.height)/2
        self.open_button.on_left_click = self.on_open_button_clicked
        
        self.close_button = BorderedButton(200, 365, -1, 20, " Close ")
        self.close_button.on_left_click = self.on_close_button_clicked
        
        self.error_msg = MultilineText(0, 0, 1, 1, "Couldn't load file!", text_bg_color=TEXT_BG2_COLOR)
        self.error_msg.x = (self.width-self.error_msg._text_width)/2
        self.error_msg.y = (self.height-self.error_msg._text_height)/2
        
        
        self.confirm_msg = MultilineText(0, 80, 1, 1, "       You haven't saved!       \nWould you like to close anyways?")
        self.confirm_msg.x = (self.width-self.confirm_msg._text_width)/2
        
        self.confirm_close_button = BorderedButton(0, 0, -1, 20, " Close ")
        self.confirm_close_button.off_left_click = self.on_confirm_button_clicked
        
        self.cancel_close_button = BorderedButton(0, 0, -1, 20, " Cancel ")
        self.cancel_close_button.on_left_click = self.on_cancel_button_clicked
        
        self.confirm_close_button.x = (self.width-self.confirm_close_button.width)/2
        self.confirm_close_button.y = ((self.height-self.confirm_close_button.height)/2) - 15
        
        self.cancel_close_button.x = (self.width-self.cancel_close_button.width)/2
        self.cancel_close_button.y = ((self.height-self.cancel_close_button.height)/2) + 15
        
        
        self.state = "open-menu"
        
        self.mouse_pos = [0, 0]
        self.screen = pygame.Surface((self.width, self.height))
        self._canvas = ConstructionCanvas._Canvas(editor, self)
        
        self.offsetX = 0
        self.offsetY = 0
        
        self.scroll_x = self.x + self.width
        self.scroll_y = 0
        self.scroll_width = 5
        self.scroll_height = 5
        self.scroll_space = scroll_height
        self.scroll_visible = False
        self.scroll_click_offset = 0
        self.scroll_bar_color = (0, 120, 212)
        self.scroll_bar_hover_color = (200, 200, 200)
        self.scroll_hovered = False
        self.scroll_dragging = False
        self.scroll_clicked = False
        
        self.last_X = 0
        self.last_Y = 0
        
        self.cutoff_bar = pygame.Surface((self.width+5, 5))
        self.cutoff_bar.fill((140, 140, 140))
    
    def collides(self, mouse, rect) -> bool:
        mx, my = mouse
        x, y, w, h = rect
        
        if self.editor.collides(self.editor.mouse_pos, (self.x+self.last_X, self.y+self.last_Y, self.width, self.height)):
            return x <= mx < x+w and y < my < y+h
        
        return False
    
    def override_values(self, X, Y):
        self.mouse_pos = list(self.editor.mouse_pos)
        self.mouse_pos[0] -= self.x + X
        self.mouse_pos[1] -= self.y + Y
        self.last_X = X
        self.last_Y = Y
    
    def on_confirm_button_clicked(self, editor):
        self.state = "open-menu"
    
    def on_cancel_button_clicked(self, editor):
        self.state = "editor"
    
    def on_save(self, _, content, __, ___):
        with open(self.file_path, "w+", encoding="utf-8") as f:
            f.write(content)
    
    def on_open_button_clicked(self, editor):
        
        if os.path.exists(self.file_path):
            with open(self.file_path, "r+", encoding="utf-8") as f:
                self.text_box.set_content(f.read())
            
            match self.file_path.rsplit(".", 1)[-1]:
                case "json"|"piskel":
                    self.text_box.color_text = FileEditor.json_colors
                case "ds"|"dungeon_script"|"dse":
                    self.text_box.color_text = FileEditor.ds_colors
                case "md":
                    self.text_box.color_text = FileEditor.md_colors
                case _:
                    pass
            
            self.text_box.refresh_surfaces()
            
            self.state = "editor"
        
        else:
            self.state = "404"
    
    def on_close_button_clicked(self, editor):
        self.text_box.unfocus()
        
        if self.text_box.saved:
            self.state = "open-menu"
        else:
            self.state = "confirm-close"
    
    def _event(self, editor, X, Y):
        self.editor = editor
        self.override_values(X, Y)
        
        match self.state:
            case "open-menu":
                self.open_button._event(editor, X+self.x, Y+self.y)
            case "404":
                self.error_msg._event(editor, X+self.x, Y+self.y)
            case "confirm-close":
                self.confirm_msg._event(editor, X+self.x, Y+self.y)
                self.confirm_close_button._event(editor, X+self.x, Y+self.y)
                self.cancel_close_button._event(editor, X+self.x, Y+self.y)
            case _:
                
                self.close_button._event(editor, X, Y)
                
                self.scroll_visible = self.text_box._text_height - self.text_box._height >= 0
                
                if self.scroll_visible:
                    self.scroll_hovered = False
                    self.scroll_height = (self.height*self.scroll_space)/(self.text_box._text_height + self.scroll_space - self.text_box._height)
                    
                    if editor.collides(editor.mouse_pos, ((X+self.scroll_x, Y+self.y+self.scroll_y, 5, self.scroll_height))):
                        if editor._hovering is None:
                            editor._hovering = NumberedTextArea.fake_hover
                            editor._hovered = NumberedTextArea.fake_hover = True
                        self.scroll_hovered = True
                        if editor.left_mouse_down():
                            self.scroll_dragging = True
                            self.scroll_click_offset = editor.mouse_pos[1] - self.scroll_y
                    
                    elif editor.collides(editor.mouse_pos, ((X+self.scroll_x, Y+self.y, 5, self.scroll_space))):
                        if editor._hovering is None:
                            editor._hovering = NumberedTextArea.fake_hover
                            editor._hovered = NumberedTextArea.fake_hover = True
                        if editor.left_mouse_down():
                            self.scroll_dragging = True
                            self.scroll_y = min(max(0, editor.mouse_pos[1]-self.y-(self.scroll_height/2)), self.scroll_space-self.scroll_height)
                            self.scroll_click_offset = editor.mouse_pos[1] - self.scroll_y
                    
                    if not editor.mouse[0]:
                        self.scroll_dragging = False
                else:
                    self.scroll_dragging = False
                
                
                self.text_box._event(self._canvas, self.offsetX, self.offsetY)
                
                if editor.scroll != 0 and self.text_box.hovered:
                    if pygame.K_LSHIFT in editor.keys: # pylint: disable=no-member
                        self.offsetX += editor.scroll * SCROLL_MULTIPLIER
                        self.offsetX = -min(max(0, -self.offsetX), self.text_box._text_width - 40)
                        
                    else:
                        self.offsetY += editor.scroll * SCROLL_MULTIPLIER
                        self.offsetY = -min(max(0, -self.offsetY), self.text_box._text_height - self.text_box._height)
                
                if self.scroll_dragging:
                    self.scroll_y = min(max(0, editor.mouse_pos[1]-self.scroll_click_offset), self.scroll_space-self.scroll_height)
                
                    ratio = self.scroll_y / ((self.scroll_space - self.scroll_height))
                    self.offsetY = -((self.text_box._text_height - self.text_box._height)*ratio)
                elif (self.text_box._text_height - self.text_box._height) != 0:
                    ratio = -self.offsetY / (self.text_box._text_height - self.text_box._height) #
                    self.scroll_y = (self.scroll_space-self.scroll_height) * ratio
    
    def _update(self, editor, X, Y):
        match self.state:
            case "open-menu":
                self.open_button._update(editor, X+self.x, Y+self.y)
            case "404":
                self.error_msg._update(editor, X+self.x, Y+self.y)
            case "confirm-close":
                self.confirm_msg._update(editor, X+self.x, Y+self.y)
                self.confirm_close_button._update(editor, X+self.x, Y+self.y)
                self.cancel_close_button._update(editor, X+self.x, Y+self.y)
            case _:
                self.screen.fill(TEXT_BG2_COLOR)
                self.text_box._update(self._canvas, self.offsetX, self.offsetY)
                editor.screen.blit(self.screen, (X+self.x, Y+self.y))
                
                if self.scroll_visible:
                    dw = min(X+self.scroll_x, 0)
                    dh = min(Y+self.y+self.scroll_y, 0)
                    
                    editor.screen.fill(self.scroll_bar_hover_color if (self.scroll_dragging or self.scroll_hovered) else self.scroll_bar_color, (X+self.scroll_x-dw, Y+self.y+self.scroll_y-dh, 5+dw, self.scroll_height+dh))
                
                editor.screen.blit(self.cutoff_bar, (X+self.x, Y+self.y+self.height-1))
                
                self.close_button._update(editor, X, Y)


