# pylint: disable=W,R,C,import-error

from UIElement import UIElement
from Text import Text
from MultilineTextBox import MultilineTextBox
from ConstructionCanvas import ConstructionCanvas
from Options import TEXT_BG_COLOR, TEXT_BG2_COLOR, SCROLL_MULTIPLIER
from NumberedTextArea import NumberedTextArea
from FunctionalElements import BorderedButton
from Slider import Slider
from Toasts import Toasts

import pygame
import re
from mergedeep import merge

class SettingsApp(UIElement):
    
    DEFAULT_CONFIG = {
        "General Settings": {},
        "Game Settings": {
            "game_volume": 1
        },
        "Editor Settings": {
            "editor_volume": 0.35
        }
    }
    
    def load_config(self):
        self.config: dict[str, dict[str, str|float|bool]] = {}
        with open(f"./settings.toml", "r+", encoding="utf-8") as f:
            category = ""
            for line in f.readlines():
                if re.match(r" *#", line): continue
                if m := re.match(r" *\[(?P<category>[^\]]+)\]", line):
                    category = m.groupdict()["category"]
                    if category not in self.config:
                        self.config.update({category: {}})
                elif m := re.match(r" *(?P<attr>[^=]+) *= *(?P<val>.*)", line):
                    d = m.groupdict()
                    attr = d["attr"].strip()
                    val = d["val"].strip()
                    if m := re.match(r"(?P<v>\d+(?:\.\d+)?)%", val):
                        val = float(m.groupdict()["v"])/100
                    elif m := re.match(r"\d+(?:\.\d+)?", val):
                        val = float(val)
                    elif val == "False":
                        val = False
                    elif val == "True":
                        val = True
                    
                    self.config[category].update({attr: val})
    
    def save_config(self):
        lines = []
        for category, vals in self.config.items():
            lines.append(f"[{category}]")
            for attr, val in vals.items():
                if attr in ["game_volume", "editor_volume"]:
                    lines.append(f"{attr} = {int(val*100)}%")
                else:
                    lines.append(f"{attr} = {val}")
            lines.append("")
        
        with open(f"./settings.toml", "w+", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
    
    def load_component_values(self, *_, **__):
        
        ### XXX Editor Settings XXX ###
        
        editor_vol = self.config["Editor Settings"]["editor_volume"]
        self.editor_volume_slider.set_percent(editor_vol)
        self.editor_volume_text_box.set_content(str(int(editor_vol*100)))

    def save_component_values(self):
        
        ### XXX Editor Settings XXX ###
        self.config["Editor Settings"]["editor_volume"] = self.editor_volume_slider.get_percent()

    def reset_config(self, *_, **__):
        self.config = merge({}, self.DEFAULT_CONFIG)
        self.save_config()
        self.load_component_values()

    def __init__(self, code_editor, editor):
        self.code_editor = code_editor
        self.editor = editor
        self.children = []
        self.load_config()
        self._canvas = ConstructionCanvas._Canvas(editor, self)
        self.screen = pygame.Surface((editor.width-50, editor.height-40))
        self.center = self.screen.get_width()/2
        
        self.toasts = Toasts(editor.width-355, editor.height-20, 350)
        
        
        self.x = 50
        self.y = 20
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
        
        self.width = editor.width - 66
        self.height = editor.height - 40
        
        ### XXX Apply & Save / Reset / Reset to Defaults XXX ###
        
        self.full_reset_button = BorderedButton(0, self.y+10, 215, 23, " Reset to Defaults", text_size=19)
        self.full_reset_button.on_left_click = self.reset_config

        self.reset_button = BorderedButton(0, self.y+10, 80, 23, " Reset", text_size=19)
        self.reset_button.on_left_click = self.load_component_values

        self.apply_changes_button = BorderedButton(0, self.y+10, 155, 23, " Apply & Save", text_size=19)
        self.apply_changes_button.on_left_click = self.apply_settings
        

        ### XXX ######################################## XXX ###
        
        
        y_offset = 20
        
        self.general_settings_label = Text(20, y_offset, 1, "General Settings", text_size=30)
        self.children.append(self.general_settings_label)
        y_offset += self.general_settings_label.height + 20
        ### XXX General Settings XXX ###
        
        ### XXX ################ XXX ###
        y_offset += 300
        
        
        self.game_settings_label = Text(20, y_offset, 1, "Game Settings", text_size=30)
        self.children.append(self.game_settings_label)
        y_offset += self.game_settings_label.height + 20
        ### XXX Game Settings XXX ###
        
        ### XXX ############# XXX ###
        y_offset += 300
        
        self.editor_settings_label = Text(20, y_offset, 1, "Editor Settings", text_size=30)
        self.children.append(self.editor_settings_label)
        y_offset += self.editor_settings_label.height + 20
        ### XXX Editor Settings XXX ###
        
        
        editor_vol = self.config["Editor Settings"]["editor_volume"]
        self.editor_volume_label = Text(20, y_offset, 1, "Editor Volume", text_size=20)
        self.children.append(self.editor_volume_label)
        self.editor_volume_slider = Slider(self.editor_volume_label.width+70, y_offset+10, 300, 0, editor_vol, 6)
        self.children.append(self.editor_volume_slider)
        self.editor_volume_text_box = MultilineTextBox(self.editor_volume_label.width+420, y_offset, 1, 20, str(int(editor_vol*100)), text_size=20, single_line=True)
        self.editor_volume_text_box.on_enter(self.editor_volume_text_box_enter)
        self.editor_volume_text_box.char_whitelist = [c for c in "1234567890"]
        self.children.append(self.editor_volume_text_box)
        y_offset += 20
        
        
        
        ### XXX ############### XXX ###
        y_offset += 300
        
        self.total_scroll = max(0, min(y_offset, self.height)-self.height/2)
        
        self.mouse_pos = [0, 0]
        self.scroll = 0
        
        self.apply_settings()

    def open_menu(self):
        self.load_config()
        self.load_component_values()

    def apply_settings(self, *_, **__):
        self.save_component_values()
        self.save_config()
        self.editor.sound_system.set_volume("editor", self.config["Editor Settings"]["editor_volume"])
        
        if _:
            self.toasts.toast("Settings Saved!", border_color=(40, 200, 40))

    def editor_volume_text_box_enter(self, textbox):
        num = int(textbox.get_content())
        num = min(max(0, num), 100)
        textbox.set_content(str(num))
        self.editor_volume_slider.set_percent(num/100)

    def position_objects(self, editor):
        y_offset = 20
        
        self.full_reset_button.x = editor.width - 235
        self.reset_button.x = self.full_reset_button.x - 90
        self.apply_changes_button.x = self.reset_button.x - 165
        
        self.toasts.x = editor.width-355
        self.toasts.y = editor.height-20
        
        self.general_settings_label.y = y_offset
        y_offset += self.general_settings_label.height + 20
        ### XXX General Settigns XXX ###
        
        y_offset += 300
        
        
        self.game_settings_label.y = y_offset
        y_offset += self.game_settings_label.height + 20
        ### XXX Game Settings XXX ###
        
        y_offset += 300
        
        self.editor_settings_label.y = y_offset
        y_offset += self.editor_settings_label.height + 20
        ### XXX Editor Settings XXX ###
        
        y_offset += 300
        
        
        self.total_scroll = max(0, min(y_offset, self.height)-self.height/2)
        self.width = editor.width
        self.height = editor.height

    def _update_layout(self, editor):
        self.width = editor.width - 66
        self.height = editor.height - 40
        self.screen = pygame.Surface((self.width, self.height))
        self.center = self.screen.get_width()/2
        
        self.position_objects(editor)

    def override_values(self, editor):
        self.mouse_pos = list(editor.mouse_pos)
        self.mouse_pos[0] -= self.x
        self.mouse_pos[1] -= self.y - self.scroll
        
    def _event(self, editor, X, Y):
        if editor._do_layout_update:
            self._update_layout(editor)
        
        self.override_values(editor)
        
        self.full_reset_button._event(editor, X, Y)
        self.reset_button._event(editor, X, Y)
        self.apply_changes_button._event(editor, X, Y)
        self.toasts._event(editor, X, Y)
        
        for child in self.children[::-1]:
            child._event(self._canvas, 0, -self.scroll)
            
        if editor.collides(editor.mouse_pos, (self.x, self.y, self.width, self.height)):
            if editor.scroll is not None:
                self.scroll -= editor.scroll * SCROLL_MULTIPLIER
                
                self.scroll = min(max(0, self.scroll), self.total_scroll)
        
        self.show_scrollbar = self.total_scroll != 0
        
        if self.show_scrollbar:
            self.scroll_hovered = False
            self.scroll_bar_height = ((self.height-40)**2)/(self.total_scroll + (self.height-40))
            # print(self.scroll_bar_height)
        
            if editor.collides(editor.mouse_pos, ((self.x+self.width-66)+self.scroll_collision_inset, self.y+self.scroll_bar_y, self.scroll_bar_width-(2*self.scroll_collision_inset), self.scroll_bar_height)):
                # print(f"Hovering scroll!")
                if editor._hovering is None:
                    editor._hovering = NumberedTextArea.fake_hover
                    editor._hovered = NumberedTextArea.fake_hover._hovered = True
                self.scroll_hovered = True
                if editor.left_mouse_down():
                    self.scroll_dragging = True
                    self.scroll_click_offset = editor.mouse_pos[1]-self.scroll_bar_y
            elif editor.collides(editor.mouse_pos, ((self.x+self.width-66)+self.scroll_collision_inset, self.y, self.scroll_bar_width-(2*self.scroll_collision_inset), (self.height-40))):
                # print(f"Hovering scroll area!")
                if editor._hovering is None:
                    editor._hovering = NumberedTextArea.fake_hover
                    editor._hovered = NumberedTextArea.fake_hover._hovered = True
                if editor.left_mouse_down():
                    self.scroll_dragging = True
                    self.scroll_bar_y = min(max(0, editor.mouse_pos[1]-self.y-(self.scroll_bar_height/2)), self.height-self.scroll_bar_height)
                    self.scroll_click_offset = editor.mouse_pos[1]-self.scroll_bar_y

            if not editor.mouse[0]:
                self.scroll_dragging = False
        
        else:
            self.scroll_dragging = False

        if self.scroll_dragging:
            self.scroll_bar_y = min(max(0, editor.mouse_pos[1]-self.scroll_click_offset), (self.height-40)-self.scroll_bar_height)
            
            ratio = self.scroll_bar_y / (((self.height-40)-self.scroll_bar_height))
            self.scroll = ((self.total_scroll)*ratio)
        elif self.total_scroll:
            ratio = self.scroll / (self.total_scroll) #
            self.scroll_bar_y = ((self.height-40)-self.scroll_bar_height) * ratio
        
        if not self.editor_volume_text_box.focused:
            self.editor_volume_text_box.set_content(str(int(self.editor_volume_slider.get_percent()*100)))

    def _update(self, editor, X, Y):
        self.screen.fill(TEXT_BG_COLOR)

        for child in self.children:
            child._update(self._canvas, 0, -self.scroll)

        editor.screen.blit(self.screen, (self.x, self.y))
        
        self.full_reset_button._update(editor, X, Y)
        self.reset_button._update(editor, X, Y)
        self.apply_changes_button._update(editor, X, Y)
        
        
        if self.show_scrollbar:
            # print("rendering scroll")
            editor.screen.fill(self.scroll_bg, ((self.x+self.width-66)+self.scroll_collision_inset, self.y, self.scroll_bar_width-(2*self.scroll_collision_inset), (self.height-40)))
            editor.screen.fill((self.scroll_bar_click_color if self.scroll_dragging else (self.scroll_bar_hover_color if self.scroll_hovered else self.scroll_bar_color)), ((self.x+self.width-66)+self.scroll_visibility_inset, self.y+self.scroll_bar_y, self.scroll_bar_width-(2*self.scroll_visibility_inset), self.scroll_bar_height))
        
        self.toasts._update(editor, X, Y)
        