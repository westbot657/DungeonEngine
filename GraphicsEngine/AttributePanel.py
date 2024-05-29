# pylint: disable=[W,R,C, no-member, import-error]

from UIElement import UIElement
from Options import PATH, TEXT_BG2_COLOR, TEXT_BG3_COLOR, TEXT_COLOR
from RenderPrimitives import Image
from CursorFocusTextBox import CursorFocusTextBox
from MultilineTextBox import MultilineTextBox
from Text import Text
from VisualLoader import VisualLoader, AttributeCell, CellSlot
from AdvancedPanels.PanelTextBox import PanelTextBox
from ContextTree import ContextTree

from Editor import Editor

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
        self.top_children = []
        self.bordered = bordered
        self.scroll_directions = 0b0000 # left, up, right, down
        self.glowing = False
        self.glow_time = 0
        self.bg_color = bg_color
        self.visible = True
        self.data = data
        self.generator = None
        self.hovered = False
        self.border_hovered = False
        self.shelf_panel = None
        self.has_data = False
        self.build_data(editor)
        self.rebuild()
        self.referencers = []

    def get_reference_tree(self):
        out = [self.parent_ref.uid]
        
        for ref in self.referencers:
            out += ref.get_reference_tree()

        return out

    def build_common(self, editor, ref_type):
        
        locked = self.data["ref"].locked
        
        id_textbox = CursorFocusTextBox(10, 6, 280, 19, editor, text_size=15, content=self.data["ref"].uid, text_bg_color=TEXT_BG2_COLOR)
        n = self.data["ref"].get("name")
        
        parent_label = Text(15, 63, 1, "parent:  ", text_bg_color=None, text_color=TEXT_BG3_COLOR)
        
        parent = self.data["ref"].get_raw("parent", None)
        if isinstance(parent, VisualLoader.ObjectReference):
            parent_cell = AttributeCell(editor, parent, f"{ref_type}-ref", False)
        else:
            parent_cell = None
        
        parent_data_cell = CellSlot(editor, self, 15+parent_label.width, 60, 180, 24, [f"{ref_type}-ref"], parent_cell, locked, ignored_values=[self.data["ref"].uid])
        
        self.generator = reference_generator = CellSlot(editor, self, 15, 365, 132, 20, f"{ref_type}-ref", self.data["ref"].uid, False, True)
        name_textbox = CursorFocusTextBox(10, 30, 280, 25, editor, shadow_text="[unnamed]" if locked else "name...", text_size=20, content=(n if isinstance(n, str) else ""), text_bg_color=TEXT_BG2_COLOR)
        
        
        if locked:
            id_textbox.text_box.allow_typing = False
            name_textbox.text_box.allow_typing = False
            
            id_textbox.set_text_color(TEXT_BG3_COLOR)
            name_textbox.set_text_color(TEXT_BG3_COLOR)
        
        self.children = [
            id_textbox,
            parent_label,
            parent_data_cell,
            name_textbox,
            reference_generator
        ]

    def attr_cell(self, label_text:str, value:str, y:int, y2:int, offset:int, width:int, classes:tuple[type], val_type:str, data_types:list[str], locked:bool, editor) -> tuple[Text, CellSlot]:
        label = Text(15, y, 1, label_text, text_bg_color=None, text_color=TEXT_BG3_COLOR)
        val = self.data["ref"].get(value)
        if isinstance(val, classes):
            cell = AttributeCell(editor, val, val_type, not locked)
        else:
            cell = None
        slot = CellSlot(editor, self, 15+label.width+offset, y2, width, 24, data_types, cell, locked)
        
        return label, slot

    def stash(self, editor):
        self.ctx_tree.close()
        
        _x = self.x
        _y = self.y
        
        self.shelf_panel.placer = self.shelf_panel._placer
        self.shelf_panel.aesa.visibility_groups[self.shelf_panel.category].remove(self)
        
        def redo():
            self.shelf_panel.placer = self.shelf_panel._placer
            self.shelf_panel.aesa.visibility_groups[self.shelf_panel.category].remove(self)
        
        def undo():
            self.x = _x
            self.y = _y
            self.shelf_panel.aesa.visibility_groups[self.shelf_panel.category].append(self)
            self.shelf_panel.placer = None
        
        editor.add_history(redo, undo, "Stashed panel")
    
    def show_shelf(self, editor):
        self.ctx_tree.close()
        
        if self.shelf_panel.aesa.object_tree._search in self.shelf_panel.label.lower():
            self.shelf_panel.aesa.object_tree.offsetY -= self.shelf_panel.y-5
        else:
            self.shelf_panel.aesa.toasts.toast("Current search query is\nhiding this shelf panel.")
        

    def hide(self, editor):
        self.ctx_tree.close()
        # the panel is visible if this function is reachable
        self.shelf_panel.visibility_toggle(editor)
        
        def redo():
            self.shelf_panel.visibility_toggle(editor)
        
        editor.add_history(redo, redo, "Toggled panel visibility")


    def build_data(self, editor):
        if not self.data: return
        self.parent_ref = self.data["ref"]
        if "type" in self.data:
            
            self.has_data = True
            
            self.ctx_tree = ContextTree([
                {
                    "  Stash": self.stash
                },
                {
                    "  Show on Shelf": self.show_shelf
                },
                {
                    "  Hide": self.hide
                }
            ], 200, 20, group="main-ctx", hover_color=TEXT_BG2_COLOR, click_color=TEXT_BG2_COLOR)
            
            
            match self.data["type"]:
                case "weapon-base":
                    # self.height = 300
                    self.build_common(editor, "weapon")
                    
                    # self.children[4].y -= 100
                    
                    locked = self.data["ref"].locked
                    
                    damage_label = Text(15, 93, 1, "Damage:  ", text_bg_color=None, text_color=TEXT_BG3_COLOR)
                    dmg = self.data["ref"].get("damage")
                    if isinstance(dmg, (int, float, dict)):
                        damage_cell = AttributeCell(editor, dmg, "int", not locked)
                    else:
                        damage_cell = None
                    damage_slot = CellSlot(editor, self, 15+damage_label.width, 90, 180, 24, ["int", "float"], damage_cell, locked)
                    
                    
                    range_label = Text(15, 123, 1, "Range:  ", text_bg_color=None, text_color=TEXT_BG3_COLOR)
                    rng = self.data["ref"].get("range")
                    if isinstance(rng, (int, float, dict)):
                        range_cell = AttributeCell(editor, rng, "int", not locked)
                    else:
                        range_cell = None
                    range_slot = CellSlot(editor, self, 15+damage_label.width, 120, 180, 24, ["int", "float"], range_cell, locked)
                    
                    
                    durability_label = Text(15, 153, 1, "Durability:", text_bg_color=None, text_color=TEXT_BG3_COLOR)
                    dura_label1 = Text(15, 183, 1, "Max:     ", text_bg_color=None, text_color=TEXT_BG3_COLOR)
                    dura_label2 = Text(15, 213, 1, "Default: ", text_bg_color=None, text_color=TEXT_BG3_COLOR)
                    
                    dura = self.data["ref"].get("durability")
                    if isinstance(dura, (int, float, dict)):
                        dura_cell = AttributeCell(editor, dura, "int", not locked)
                    else:
                        dura_cell = None
                    
                    dura_max = self.data["ref"].get("max_durability")
                    if isinstance(dura_max, (int, float, dict)):
                        dura_max_cell = AttributeCell(editor, dura_max, "int", not locked)
                    else:
                        dura_max_cell = None
                    
                    dura_max_slot = CellSlot(editor, self, 15+dura_label2.width, 180, 180, 24, ["int", "float"], dura_max_cell, locked)
                    dura_slot = CellSlot(editor, self, 15+dura_label2.width, 210, 180, 24, ["int", "float"], dura_cell, locked)
                    
                    # TODO: events sub-menu
                    
                    self.children += [
                        damage_label,
                        damage_slot,
                        range_label,
                        range_slot,
                        durability_label,
                        dura_label1,
                        dura_label2,
                        dura_slot,
                        dura_max_slot
                    ]
                    
                case "weapon-instance":
                    ...
                case "armor-base":
                    # self.height = 500
                    self.build_common(editor, "armor")
                    
                    # self.children[4].y += 100
                    
                    locked = self.data["ref"].locked
                    
                    desc_label, desc_slot = self.attr_cell(
                        "Description: ", "description", 93, 120, 0, 180,
                        (str), "str", ["str"], locked, editor
                    )
                    desc_slot.x = self.children[2].x
                    
                    dmg_label, dmg_slot = self.attr_cell(
                        "Damage Reduction: ", "damage_reduction", 153, 180, 0, 180,
                        (int, float, dict), "int", ["int", "float"], locked, editor
                    )
                    dmg_slot.x = desc_slot.x
                    
                    durability_label = Text(15, 213, 1, "Durability:", text_bg_color=None, text_color=TEXT_BG3_COLOR)
                    dura_label1 = Text(15, 243, 1, "Max:     ", text_bg_color=None, text_color=TEXT_BG3_COLOR)
                    dura_label2 = Text(15, 273, 1, "Default: ", text_bg_color=None, text_color=TEXT_BG3_COLOR)
                    
                    dura = self.data["ref"].get("durability")
                    if isinstance(dura, (int, float, dict)):
                        dura_cell = AttributeCell(editor, dura, "int", not locked)
                    else:
                        dura_cell = None
                    
                    dura_max = self.data["ref"].get("max_durability")
                    if isinstance(dura_max, (int, float, dict)):
                        dura_max_cell = AttributeCell(editor, dura_max, "int", not locked)
                    else:
                        dura_max_cell = None
                    
                    dura_max_slot = CellSlot(editor, self, 15+dura_label2.width, 240, 180, 24, ["int", "float"], dura_max_cell, locked)
                    dura_slot = CellSlot(editor, self, 15+dura_label2.width, 270, 180, 24, ["int", "float"], dura_cell, locked)
                    
                    # TODO: events sub-menu
                    
                    self.children += [
                        desc_label, desc_slot,
                        dmg_label, dmg_slot,
                        durability_label,
                        dura_label1, dura_max_slot,
                        dura_label2, dura_slot,
                    ]
                    
                case "armor-instance":
                    ...
                case "ammo-base":
                    self.build_common(editor, "ammo")
                    
                    locked = self.data["ref"].locked
                    
                    desc_label, desc_slot = self.attr_cell(
                        "Description: ", "description", 93, 120, 0, 180,
                        (str), "str", ["str"], locked, editor
                    )
                    desc_slot.x = self.children[2].x # 'parent' slot x-pos
                    
                    dmg_label, dmg_slot = self.attr_cell(
                        "Bonus Damage: ", "bonus_damage", 153, 180, 0, 180,
                        (int, float, dict), "int", ["int", "float"], locked, editor
                    )
                    dmg_slot.x = desc_slot.x
                    
                    durability_label = Text(15, 213, 1, "Stack Size:", text_bg_color=None, text_color=TEXT_BG3_COLOR)
                    dura_label1 = Text(15, 243, 1, "Max:     ", text_bg_color=None, text_color=TEXT_BG3_COLOR)
                    dura_label2 = Text(15, 273, 1, "Default: ", text_bg_color=None, text_color=TEXT_BG3_COLOR)
                    
                    dura = self.data["ref"].get("count")
                    if isinstance(dura, (int, dict)):
                        dura_cell = AttributeCell(editor, dura, "int", not locked)
                    else:
                        dura_cell = None
                    
                    dura_max = self.data["ref"].get("max_count")
                    if isinstance(dura_max, (int, dict)):
                        dura_max_cell = AttributeCell(editor, dura_max, "int", not locked)
                    else:
                        dura_max_cell = None
                    
                    dura_max_slot = CellSlot(editor, self, 15+dura_label2.width, 240, 180, 24, ["int"], dura_max_cell, locked)
                    dura_slot = CellSlot(editor, self, 15+dura_label2.width, 270, 180, 24, ["int"], dura_cell, locked)
                    
                    self.children += [
                        desc_label, desc_slot,
                        dmg_label, dmg_slot,
                        durability_label,
                        dura_label1, dura_label2,
                        dura_max_slot, dura_slot
                    ]
                    
                case "ammo-instance":
                    ...
                case "tool-base":
                    self.build_common(editor, "tool")
                case "tool-instance":
                    ...
                case "item-base":
                    self.build_common(editor, "item")
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
                case "room-base":
                    locked = self.data["ref"].locked
        
                    id_textbox = CursorFocusTextBox(10, 6, 280, 19, editor, text_size=15, content=self.data["ref"].uid, text_bg_color=TEXT_BG2_COLOR)
                    n = self.data["ref"].get("name")
                    
                    self.generator = reference_generator = CellSlot(editor, self, 15, 365, 132, 20, "room-ref", self.data["ref"].uid, False, True)
                    name_textbox = CursorFocusTextBox(10, 30, 280, 25, editor, shadow_text="[unnamed]" if locked else "name...", text_size=20, content=(n if isinstance(n, str) else ""), text_bg_color=TEXT_BG2_COLOR)
                    
                    on_enter_label = Text(15, 80,  1, "Enter Script: ", text_bg_color=None, text_color=TEXT_BG3_COLOR)
                    on_input_label = Text(15, 140, 1, "Input Script: ", text_bg_color=None, text_color=TEXT_BG3_COLOR)
                    on_exit_label  = Text(15, 200, 1, "Exit Script: ",  text_bg_color=None, text_color=TEXT_BG3_COLOR)
                    
                    on_enter = self.data["ref"].get("on_enter")
                    if isinstance(on_enter, dict) and "#script" in on_enter:
                        on_enter_cell = AttributeCell(editor, VisualLoader.ObjectReference(on_enter["#script"]), "script-ref", False)
                    else:
                        on_enter_cell = None
                    
                    on_enter_slot = CellSlot(editor, self, 15, 100, 200, 24, ["script-ref"], on_enter_cell, locked)
                    
                    on_input = self.data["ref"].get("on_input")
                    if isinstance(on_input, dict) and "#script" in on_input:
                        on_input_cell = AttributeCell(editor, VisualLoader.ObjectReference(on_input["#script"]), "script-ref", False)
                    else:
                        on_input_cell = None
                    
                    on_input_slot = CellSlot(editor, self, 15, 160, 200, 24, ["script-ref"], on_input_cell, locked)
                    
                    on_exit = self.data["ref"].get("on_exit")
                    if isinstance(on_exit, dict) and "#script" in on_exit:
                        on_exit_cell = AttributeCell(editor, VisualLoader.ObjectReference(on_exit["#script"]), "script-ref", False)
                    else:
                        on_exit_cell = None
                    
                    on_exit_slot = CellSlot(editor, self, 15, 220, 200, 24, ["script-ref"], on_exit_cell, locked)
                    
                    if locked:
                        id_textbox.text_box.allow_typing = False
                        name_textbox.text_box.allow_typing = False
                        
                        id_textbox.set_text_color(TEXT_BG3_COLOR)
                        name_textbox.set_text_color(TEXT_BG3_COLOR)
                    
                    # TODO: interactions sub-menu
                    
                    self.children = [
                        id_textbox,
                        on_enter_label,
                        on_enter_slot,
                        on_input_label,
                        on_input_slot,
                        on_exit_label,
                        on_exit_slot,
                        name_textbox,
                        reference_generator
                    ]
                    
                case "script-base":
                    locked = self.data["ref"].locked
                    id_textbox = CursorFocusTextBox(10, 6, 280, 19, editor, text_size=15, content=self.data["ref"].uid, text_bg_color=TEXT_BG2_COLOR)
                    
                    edit_box = PanelTextBox(5, 30, 285, 320, 320, self.data["ref"].get("file"), editor)
                    
                    self.generator = reference_generator = CellSlot(editor, self, 15, 365, 132, 20, f"script-ref", self.data["ref"].uid, False, True)
                    
                    if locked:
                        id_textbox.text_box.allow_typing = False
                        id_textbox.set_text_color(TEXT_BG3_COLOR)
                    
                    self.children = [
                        id_textbox,
                        reference_generator
                    ]
                    self.top_children = [
                        edit_box
                    ]
                    
                case _:
                    raise TypeError(f"Unknown object type! '{self.data["type"]}'")
    
    def save(self, editor) -> dict:
        ...
    
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
            
            if self.data and self.data["type"] == "script-base":
                tb = self.top_children[0].text_box
                if tb.saved and not tb._saved:
                    self.children[0].set_text_color(TEXT_COLOR)
                elif tb._saved and not tb.saved:
                    self.children[0].set_text_color((226, 162, 74))
            
            for child in self.top_children[::-1]:
                child._event(editor, self.x, self.y)
        
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
                
                if editor.right_mouse_down() and self.has_data:
                    # print(f"open ctx menu?  {Editor._e_instance} mouse: {Editor._e_instance.mouse_pos}")
                    self.ctx_tree.openAtMouse(Editor._e_instance)
                
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

            for child in self.top_children:
                child._update(editor, X+self.x, Y+self.y)
        
    def get_collider(self):
        return (self.x, self.y, self.width, self.height)

