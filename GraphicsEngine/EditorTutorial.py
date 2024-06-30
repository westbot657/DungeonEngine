# pylint: disable=W,R,C,import-error,no-member

from UIElement import UIElement
from Options import PATH, TEXT_COLOR, TEXT_BG_COLOR, TEXT_BG2_COLOR, TEXT_BG3_COLOR
from FunctionalElements import Button, BorderedButton
from MultilineText import MultilineText

from Hyperlink import Hyperlink

import pygame

class EditorTutorial(UIElement):
    def __init__(self, aesa):
        self.aesa = aesa
        self.pages = {}
        self.masks = {}
    
        self.mask_opacity = 200
    
        self.page = 0
        
        self.animation = 0
        self.animation_state = 0
        self.animation_target = 0
        
        self.width = aesa.width
        self.height = aesa.height
        
        ### PAGE 0 ###
        p0_intro_text = MultilineText(self.aesa.x+70, self.aesa.y+30, 1, 1, "Welcome to the\nDungeon Editor!", text_size=40, text_bg_color=None)
        
        p0_text1 = MultilineText(self.aesa.x+70, p0_intro_text.y+p0_intro_text.height+30, 1, 1, "This tutorial will show you how to use the editor.\nIf you already know how to use the editor, you can skip it.\n\nIf you find part of this tutorial confusing,\nyou can create an issue on the Github     .\n\nPress Next to continue.", text_size=20, text_bg_color=None)
        
        p0_github_link = Hyperlink(self.aesa.x+526, p0_intro_text.y+p0_intro_text.height+122, 1, 1, "here", "https://github.com/Westbot657/DungeonEngine/issues", text_size=20, text_bg_color=None)
        
        self.pages.update({0: [p0_intro_text, p0_text1, p0_github_link]})
    
        ### PAGE 1 ###
        
        ### PAGE 2 ###
        
        ### PAGE 3 ###
        
        ### General ###
        
        self.mask = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.mask.fill((0, 0, 0, self.mask_opacity))
        
        self.next_button = BorderedButton(0, aesa.editor.height-50, -1, 20, "  Next >  ", bg_color=TEXT_BG2_COLOR, hover_color=TEXT_BG3_COLOR, click_color=TEXT_BG2_COLOR, border_color=TEXT_BG3_COLOR)
        self.next_button.on_left_click = self.next_button_event
    
        self.back_button = BorderedButton(0, aesa.editor.height-50, -1, 20, "  < Back  ", bg_color=TEXT_BG2_COLOR, hover_color=TEXT_BG3_COLOR, click_color=TEXT_BG2_COLOR, border_color=TEXT_BG3_COLOR)
        self.back_button.on_left_click = self.back_button_event
    
        self.next_button.x = aesa.editor.width - (self.next_button.width + 15)
        
        self.skip_button = BorderedButton(0, aesa.editor.height-75, self.next_button.width + self.back_button.width + 10, 20, "    Skip Tutorial  ", bg_color=TEXT_BG2_COLOR, hover_color=TEXT_BG3_COLOR, click_color=TEXT_BG2_COLOR, border_color=TEXT_BG3_COLOR)
        self.skip_button.on_left_click = self.skip_button_event
        
        self.back_button.x = self.skip_button.x = self.next_button.x - (self.back_button.width + 10)
    
    
    ### PAGE 0 ###
    
    
    
    ### PAGE 1 ###
    
    
    
    ### PAGE 2 ###
    
    
    
    ### PAGE 3 ###
    


    ### General ###
    
    def skip_button_event(self, *_, **__):
        self.aesa.seen_tutorial = True
        self.aesa.code_editor.settings_app.seen_tutorial_toggle.set_state(True)
        self.aesa.code_editor.settings_app.save_component_values()
        self.aesa.code_editor.settings_app.save_config()
        self.page = 0
    
    def back_button_event(self, *_, **__):
        if self.page > 0:
            self.page -= 1
    
    def next_button_event(self, *_, **__):
        if self.page < len(self.pages) - 1:
            self.page += 1
    
    def plain_mask_draw(self):
        self.mask = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.mask.fill((0, 0, 0, self.mask_opacity))
    
    def _update_layout(self, editor):
        if editor._do_layout_update:
            self.width = self.aesa.width
            self.height = self.aesa.height
            self.next_button.x = editor.width - (self.next_button.width + 15)
            self.back_button.x = self.skip_button.x = self.next_button.x - (self.back_button.width + 10)
            self.back_button.y = editor.height-50
            self.next_button.y = editor.height-50
            self.skip_button.y = editor.height-75
            
            self.mask = pygame.Surface((self.width, self.height))
            self.masks.get(self.page, self.plain_mask_draw)()

    def _event(self, editor, X, Y):
        self.back_button._event(editor, X, Y)
        self.next_button._event(editor, X, Y)
        self.skip_button._event(editor, X, Y)
    
        for child in self.pages.get(self.page, [])[::-1]:
            child._event(editor, X, Y)
    
    
        if not editor._hovered:
            mx, my = editor.mouse_pos
            _x = mx-self.aesa.x
            _y = my-self.aesa.y
            if 0 <= _x < self.width and 0 <= _y < self.height:
                if self.page in []:
                    if self.mask.get_at((_x, _y)) == (0, 0, 0, self.mask_opacity):
                        editor._hovered = True
                        editor._hovering = self
                else:
                    editor._hovered = True
                    editor._hovering = self
    
    def _update(self, editor, X, Y):
        
        editor.screen.blit(self.mask, (self.aesa.x, self.aesa.y))
        
        for child in self.pages.get(self.page, []):
            child._update(editor, X, Y)
            
             
        self.back_button._update(editor, X, Y)
        self.next_button._update(editor, X, Y)
        self.skip_button._update(editor, X, Y)
        
    