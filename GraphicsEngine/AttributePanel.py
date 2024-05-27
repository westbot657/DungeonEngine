# pylint: disable=[W,R,C, no-member, import-error]

from UIElement import UIElement
from Options import PATH, TEXT_BG2_COLOR, TEXT_BG3_COLOR
from RenderPrimitives import Image
from CursorFocusTextBox import CursorFocusTextBox
from MultilineTextBox import MultilineTextBox
from Text import Text
from VisualLoader import VisualLoader, AttributeCell, CellSlot

import pygame
import time

class AttributePanel(UIElement):
    ts = pygame.image.load(f"{PATH}/advanced_editor/attribute_panel_sheet.png")
    gs = pygame.image.load(f"{PATH}/advanced_editor/attribute_panel_glow.png")
    texture_scale = 5
    m = 5
    
    segments = {
        "top_left": {
            "normal": Image.from_pygameSurface(ts, (0, 0, 6, 6)).scale(texture_scale),
            "*": Image.from_pygameSurface(ts, (0, 18, 6, 6)).scale(texture_scale),
            "glow": Image.from_pygameSurface(gs, (0, 0, 8*m, 8*m)).scale(m/texture_scale)
        },
        "top_middle": {
            "normal": Image.from_pygameSurface(ts, (6, 0, 6, 6)).scale(texture_scale),
            "*": Image.from_pygameSurface(ts, (6, 18, 6, 6)).scale(texture_scale),
            "glow": Image.from_pygameSurface(gs, (8*m, 0, 8*m, 8*m)).scale(texture_scale)
        },
        "top_right": {
            "normal": Image.from_pygameSurface(ts, (12, 0, 6, 6)).scale(texture_scale),
            "*": Image.from_pygameSurface(ts, (12, 18, 6, 6)).scale(texture_scale),
            "glow": Image.from_pygameSurface(gs, (16*m, 0, 8*m, 8*m)).scale(m/texture_scale)
        },
        "top_left_strip": {
            "normal": Image.from_pygameSurface(ts, (0, 6, 6, 2)).scale(texture_scale),
            "h": Image.from_pygameSurface(ts, (0, 24, 6, 2)).scale(texture_scale),
            "h_top": Image.from_pygameSurface(ts, (0, 42, 6, 2)).scale(texture_scale),
            "h_left": Image.from_pygameSurface(ts, (0, 60, 6, 2)).scale(texture_scale),
            "h_top_left": Image.from_pygameSurface(ts, (0, 78, 6, 2)).scale(texture_scale)
        },
        "top_middle_strip": {
            "normal": Image.from_pygameSurface(ts, (6, 6, 6, 2)).scale(texture_scale),
            "h_top": Image.from_pygameSurface(ts, (6, 42, 6, 2)).scale(texture_scale),
            "*": Image.from_pygameSurface(ts, (6, 24, 6, 2)).scale(texture_scale)
        },
        "top_right_strip": {
            "normal": Image.from_pygameSurface(ts, (12, 6, 6, 2)).scale(texture_scale),
            "h": Image.from_pygameSurface(ts, (12, 24, 6, 2)).scale(texture_scale),
            "h_top": Image.from_pygameSurface(ts, (12, 42, 6, 2)).scale(texture_scale),
            "h_right": Image.from_pygameSurface(ts, (12, 60, 6, 2)).scale(texture_scale),
            "h_top_right": Image.from_pygameSurface(ts, (12, 78, 6, 2)).scale(texture_scale)
        },
        "middle_left": {
            "normal": Image.from_pygameSurface(ts, (0, 8, 6, 4)).scale(texture_scale),
            "h_left": Image.from_pygameSurface(ts, (0, 62, 6, 4)).scale(texture_scale),
            "*": Image.from_pygameSurface(ts, (0, 26, 6, 4)).scale(texture_scale),
            "glow": Image.from_pygameSurface(gs, (0, 8*m, 8*m, 8*m)).scale(texture_scale)
        },
        # "middle_middle": {
        #     "*": Image.from_pygameSurface(ts, (6, 6, 6, 6)).scale(texture_scale)
        # },
        "middle_right": {
            "normal": Image.from_pygameSurface(ts, (12, 8, 6, 4)).scale(texture_scale),
            "h_right": Image.from_pygameSurface(ts, (12, 62, 6, 4)).scale(texture_scale),
            "*": Image.from_pygameSurface(ts, (12, 26, 6, 4)).scale(texture_scale),
            "glow": Image.from_pygameSurface(gs, (16*m, 8*m, 8*m, 8*m)).scale(texture_scale)
        },
        "bottom_left": {
            "normal": Image.from_pygameSurface(ts, (0, 12, 6, 6)).scale(texture_scale),
            "h": Image.from_pygameSurface(ts, (0, 30, 6, 6)).scale(texture_scale),
            "h_bottom": Image.from_pygameSurface(ts, (0, 48, 6, 6)).scale(texture_scale),
            "h_left": Image.from_pygameSurface(ts, (0, 66, 6, 6)).scale(texture_scale),
            "h_bottom_left": Image.from_pygameSurface(ts, (0, 84, 6, 6)).scale(texture_scale),
            "glow": Image.from_pygameSurface(gs, (0, 16*m, 8*m, 8*m)).scale(m/texture_scale)
        },
        "bottom_middle": {
            "normal": Image.from_pygameSurface(ts, (6, 12, 6, 6)).scale(texture_scale),
            "h_bottom": Image.from_pygameSurface(ts, (6, 12, 6, 6)).scale(texture_scale),
            "*": Image.from_pygameSurface(ts, (6, 12, 6, 6)).scale(texture_scale),
            "glow": Image.from_pygameSurface(gs, (8*m, 16*m, 8*m, 8*m)).scale(texture_scale)
        },
        "bottom_right": {
            "normal": Image.from_pygameSurface(ts, (12, 12, 6, 6)).scale(texture_scale),
            "h": Image.from_pygameSurface(ts, (12, 30, 6, 6)).scale(texture_scale),
            "h_bottom": Image.from_pygameSurface(ts, (12, 48, 6, 6)).scale(texture_scale),
            "h_right": Image.from_pygameSurface(ts, (12, 66, 6, 6)).scale(texture_scale),
            "h_bottom_right": Image.from_pygameSurface(ts, (12, 84, 6, 6)).scale(texture_scale),
            "glow": Image.from_pygameSurface(gs, (16*m, 16*m, 8*m, 8*m)).scale(m/texture_scale)
        }
    }

    def __init__(self, editor, parent, x:int, y:int, width:int, height:int, bordered:bool, bg_color=TEXT_BG2_COLOR, data=None):
        self.parent = parent
        self.x = self._x = x
        self.y = self._y = y
        self.width = self._width = width
        self.height = self._height = height
        self.children = []
        self.bordered = bordered
        self.scroll_directions = 0b0000 # left, up, right, down
        self.glowing = False
        self.glow_time = 0
        self.bg_color = bg_color
        self.visible = True
        self.data = data
        self.hovered = False
        self.border_hovered = False
        self.shelf_panel = None
        self.rebuild()
        self.build_data(editor)
        self.referencers = []

    def get_reference_tree(self):
        out = [self.parent_ref.uid]
        
        for ref in self.referencers:
            out += ref.get_reference_tree()

        return out

    def build_common(self, editor):
        
        locked = self.data["ref"].locked
        
        id_textbox = CursorFocusTextBox(10, 6, 280, 19, editor, text_size=15, content=self.data["ref"].uid, text_bg_color=TEXT_BG2_COLOR)
        n = self.data["ref"].get("name")
        name_textbox = CursorFocusTextBox(10, 30, 280, 25, editor, shadow_text="[unnamed]" if locked else "name...", text_size=20, content=(n if isinstance(n, str) else ""), text_bg_color=TEXT_BG2_COLOR)
        
        parent_label = Text(15, 63, 1, "parent: ", text_bg_color=None, text_color=TEXT_BG3_COLOR)
        
        parent = self.data["ref"].get_raw("parent", None)
        if isinstance(parent, VisualLoader.ObjectReference):
            parent_cell = AttributeCell(editor, parent, "ref", False)
        else:
            parent_cell = None
        
        parent_data_cell = CellSlot(self, 15+parent_label.width, 60, 180, 24, ["ref"], parent_cell, locked, ignored_values=[self.data["ref"].uid])
        
        reference_generator = CellSlot(self, 15, 365, 132, 20, None, self.data["ref"].uid, False, True)
        
        if locked:
            id_textbox.text_box.allow_typing = False
            name_textbox.text_box.allow_typing = False
            
            id_textbox.set_text_color(TEXT_BG3_COLOR)
            name_textbox.set_text_color(TEXT_BG3_COLOR)
        
        self.children = [
            id_textbox,
            name_textbox,
            parent_label,
            parent_data_cell,
            
            reference_generator
        ]

    def build_data(self, editor):
        
        if not self.data: return
        
        self.parent_ref = self.data["ref"]
        
        # Use data to build children.
        if "type" in self.data:
            match self.data["type"]:
                case "weapon-base":
                    self.build_common(editor)
                    
                    
                    
                case "weapon-instance":
                    ...
                case "armor-base":
                    self.build_common(editor)
                case "armor-instance":
                    ...
                case "ammo-base":
                    self.build_common(editor)
                case "ammo-instance":
                    ...
                case "tool-base":
                    self.build_common(editor)
                case "tool-instance":
                    ...
                case "item-base":
                    self.build_common(editor)
                case "item-instance":
                    ...
                case "attack-base":
                    ...
                case "attack-instance":
                    ...
                case "combat-base":
                    ...
                case "combat-instance":
                    ...
                case "enemy-base":
                    ...
                case "enemy-instance":
                    ...
                case "status_effect-base":
                    ...
                case "status_effect-instance":
                    ...
                case "room":
                    ...
                case "script":
                    ...
                case _:
                    raise TypeError(f"Unknown object type! '{self.data["type"]}'")
    
    def rebuild(self):
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.bg = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.bg.fill(self.bg_color, (self.texture_scale, self.texture_scale, self.width-(2*self.texture_scale), self.height-(2*self.texture_scale)))
        self.glow_surface = pygame.Surface((self.width+(6*self.texture_scale), self.height+(6*self.texture_scale)), pygame.SRCALPHA, 32)
        
        self.glow_surface.blit(
            pygame.transform.scale(self.segments["top_left"]["glow"].surface, (8*self.texture_scale, 8*self.texture_scale)), (0, 0)
        )
        self.glow_surface.blit(
            pygame.transform.scale(self.segments["top_middle"]["glow"].surface, (max(0, self.width-(10*self.texture_scale)), 8*self.texture_scale)), (8*self.texture_scale, 0)
        )
        self.glow_surface.blit(
            pygame.transform.scale(self.segments["top_right"]["glow"].surface, (8*self.texture_scale, 8*self.texture_scale)), (self.width-(2*self.texture_scale), 0)
        )
        
        self.glow_surface.blit(
            pygame.transform.scale(self.segments["middle_left"]["glow"].surface, (8*self.texture_scale, max(self.height-(10*self.texture_scale), 0))), (0, 8*self.texture_scale)
        )
        self.glow_surface.blit(
            pygame.transform.scale(self.segments["middle_right"]["glow"].surface, (8*self.texture_scale, max(self.height-(10*self.texture_scale), 0))), (self.width-(2*self.texture_scale), 8*self.texture_scale)
        )
        
        self.glow_surface.blit(
            pygame.transform.scale(self.segments["bottom_left"]["glow"].surface, (8*self.texture_scale, 8*self.texture_scale)), (0, self.height-(2*self.texture_scale))
        )
        self.glow_surface.blit(
            pygame.transform.scale(self.segments["bottom_middle"]["glow"].surface, (max(0, self.width-(10*self.texture_scale)), 8*self.texture_scale)), (8*self.texture_scale, self.height-(2*self.texture_scale))
        )
        self.glow_surface.blit(
            pygame.transform.scale(self.segments["bottom_right"]["glow"].surface, (8*self.texture_scale, 8*self.texture_scale)), (self.width-(2*self.texture_scale), self.height-(2*self.texture_scale))
        )
        
        
        if self.bordered:
            self.surface.blit(
                pygame.transform.scale(self.segments["top_left"]["*"].surface, (6*self.texture_scale, 6*self.texture_scale)), (0, 0)
            )
            self.surface.blit(
                pygame.transform.scale(self.segments["top_middle"]["*"].surface, (self.width-(12*self.texture_scale), 6*self.texture_scale)), (6*self.texture_scale, 0)
            )
            self.surface.blit(
                pygame.transform.scale(self.segments["top_right"]["*"].surface, (6*self.texture_scale, 6*self.texture_scale)), (self.width-(6*self.texture_scale), 0)
            )
            
            self.surface.blit(
                pygame.transform.scale(self.segments["top_left_strip"]["h" + ("_top" if self.scroll_directions & 0b0100 else "") + ("_left" if self.scroll_directions & 0b1000 else "")].surface, (6*self.texture_scale, 2*self.texture_scale)), (0, 6*self.texture_scale)
            )
            self.surface.blit(
                pygame.transform.scale(self.segments["top_middle_strip"]["h_top" if self.scroll_directions & 0b0100 else "*"].surface, (self.width-(12*self.texture_scale), 2*self.texture_scale)), (6*self.texture_scale, 6*self.texture_scale)
            )
            self.surface.blit(
                pygame.transform.scale(self.segments["top_right_strip"]["h" + ("_top" if self.scroll_directions & 0b0100 else "") + ("_right" if self.scroll_directions & 0b0010 else "")].surface, (6*self.texture_scale, 2*self.texture_scale)), (self.width-(6*self.texture_scale), 6*self.texture_scale)
            )
            
            self.surface.blit(
                pygame.transform.scale(self.segments["middle_left"]["h_left" if self.scroll_directions & 0b1000 else "*"].surface, (6*self.texture_scale, self.height-(14*self.texture_scale))), (0, 8*self.texture_scale)
            )
            # self.surface.blit(
            #     pygame.transform.scale(self.segments["middle_middle"]["*"].surface, (self.width-(12*self.texture_scale), self.height-(14*self.texture_scale))), (6*self.texture_scale, 8*self.texture_scale)
            # )
            self.surface.blit(
                pygame.transform.scale(self.segments["middle_right"]["h_right" if self.scroll_directions & 0b0010 else "*"].surface, (6*self.texture_scale, self.height-(14*self.texture_scale))), (self.width-(6*self.texture_scale), 8*self.texture_scale)
            )
            
            self.surface.blit(
                pygame.transform.scale(self.segments["bottom_left"]["h" + ("_bottom" if self.scroll_directions & 0b0001 else "") + ("_left" if self.scroll_directions & 0b1000 else "")].surface, (6*self.texture_scale, 6*self.texture_scale)), (0, self.height-(6*self.texture_scale))
            ),
            self.surface.blit(
                pygame.transform.scale(self.segments["bottom_middle"]["h_bottom" if self.scroll_directions & 0b0001 else "*"].surface, (self.width-(12*self.texture_scale), 6*self.texture_scale)), (6*self.texture_scale, self.height-(6*self.texture_scale))
            )
            self.surface.blit(
                pygame.transform.scale(self.segments["bottom_right"]["h" + ("_bottom" if self.scroll_directions & 0b0001 else "") + ("_right" if self.scroll_directions & 0b0010 else "")].surface, (6*self.texture_scale, 6*self.texture_scale)), (self.width-(6*self.texture_scale), self.height-(6*self.texture_scale))
            )
        else:
            self.surface.blit(
                pygame.transform.scale(self.segments["top_left"]["normal"].surface, (6*self.texture_scale, 6*self.texture_scale)), (0, 0)
            )
            self.surface.blit(
                pygame.transform.scale(self.segments["top_middle"]["normal"].surface, (max(0, self.width-(12*self.texture_scale)), 6*self.texture_scale)), (6*self.texture_scale, 0)
            )
            self.surface.blit(
                pygame.transform.scale(self.segments["top_right"]["normal"].surface, (6*self.texture_scale, 6*self.texture_scale)), (self.width-(6*self.texture_scale), 0)
            )
            
            self.surface.blit(
                pygame.transform.scale(self.segments["top_left_strip"]["normal"].surface, (6*self.texture_scale, 2*self.texture_scale)), (0, 6*self.texture_scale)
            )
            self.surface.blit(
                pygame.transform.scale(self.segments["top_middle_strip"]["normal"].surface, (max(0, self.width-(12*self.texture_scale)), 2*self.texture_scale)), (6*self.texture_scale, 6*self.texture_scale)
            )
            self.surface.blit(
                pygame.transform.scale(self.segments["top_right_strip"]["normal"].surface, (6*self.texture_scale, 2*self.texture_scale)), (self.width-(6*self.texture_scale), 6*self.texture_scale)
            )
            
            self.surface.blit(
                pygame.transform.scale(self.segments["middle_left"]["normal"].surface, (6*self.texture_scale, max(0, self.height-(14*self.texture_scale)))), (0, 8*self.texture_scale)
            )
            # self.surface.blit(
            #     pygame.transform.scale(self.segments["middle_middle"]["*"].surface, (self.width-(12*self.texture_scale), self.height-(14*self.texture_scale))), (6*self.texture_scale, 8*self.texture_scale)
            # )
            self.surface.blit(
                pygame.transform.scale(self.segments["middle_right"]["normal"].surface, (6*self.texture_scale, max(0, self.height-(14*self.texture_scale)))), (self.width-(6*self.texture_scale), 8*self.texture_scale)
            )
            
            self.surface.blit(
                pygame.transform.scale(self.segments["bottom_left"]["normal"].surface, (6*self.texture_scale, 6*self.texture_scale)), (0, self.height-(6*self.texture_scale))
            ),
            self.surface.blit(
                pygame.transform.scale(self.segments["bottom_middle"]["normal"].surface, (max(0, self.width-(12*self.texture_scale)), 6*self.texture_scale)), (6*self.texture_scale, self.height-(6*self.texture_scale))
            )
            self.surface.blit(
                pygame.transform.scale(self.segments["bottom_right"]["normal"].surface, (6*self.texture_scale, 6*self.texture_scale)), (self.width-(6*self.texture_scale), self.height-(6*self.texture_scale))
            )

    def set_glow(self, duration:int):
        self.glow_time = time.time()+duration
        self.glowing = True

    def _event(self, editor, X, Y):
        if self.visible:
        
            for child in self.children[::-1]:
                child._event(editor, self.x, self.y)

            if self.glowing:
                if self.glow_time == 0:
                    self.glowing = False
                elif time.time() >= self.glow_time > 0:
                    self.glow_time = 0

            if editor.collides(editor.mouse_pos, (self.x, self.y, self.width, self.height)):
                if editor._hovering is None:
                    self.hovered = editor._hovered = True
                    editor._hovering = self
            else:
                self.hovered = False
                self.border_hovered = False
                
            if self.hovered:
                if not editor.collides(editor.mouse_pos, (self.x+5, self.y+5, self.width-10, self.height-10)):
                    self.border_hovered = True
                else:
                    self.border_hovered = False
            else:
                self.border_hovered = False
            
            if self.border_hovered and self.parent:
                if editor.left_mouse_down():
                    self.parent.visibility_groups[self.shelf_panel.category].remove(self)
                    editor.sound_system.get_audio("AESA_pick_up", "editor").play()
                    editor.holding = True
                    editor.held = self
                    editor.hold_offset = (editor.mouse_pos[0]-self.x, editor.mouse_pos[1]-self.y)
                    # self._x = self.x
                    # self._y = self.y
                    self.x = 0
                    self.y = 0

        else:
            self.hovered = False
            self.border_hovered = False

    def _update(self, editor, X, Y):
        if self.visible:
            editor.screen.blit(self.bg, (X+self.x, Y+self.y))
            
            for child in self.children:
                child._update(editor, X+self.x, Y+self.y)
        
            if self.glowing:
                editor.screen.blit(self.glow_surface, (X+self.x-(3*self.texture_scale), Y+self.y-(3*self.texture_scale)))
            editor.screen.blit(self.surface, (X+self.x, Y+self.y))
        
    def get_collider(self):
        return (self.x, self.y, self.width, self.height)

