# pylint: disable=W,R,C,import-error

from LoadingBar import LoadingBar
from Toasts import Toasts
from FunctionalElements import Button
from RenderPrimitives import Image
from Options import PATH, TEXT_COLOR, TEXT_BG_COLOR, TEXT_BG2_COLOR, TEXT_BG3_COLOR
from AdvancedPanels.PanelPlacer import PanelPlacer
from CursorFocusTextBox import CursorFocusTextBox
from Text import Text
from ContextTree import ContextTree
from ToggleSwitch import ToggleSwitch

from UIElement import UIElement

from typing import Any

import math
import time
import json
import glob
import os
import re

class AttributeCell(UIElement):
    
    _data_types = set()
    
    def __init__(self, editor, value:Any, data_type:str, modifieable:bool=True, new_ref=False, back_link=None):
        self.editor = editor
        self.value = value
        
        self.slot = None
        
        self.width = 150
        self.height = 24
        self.data_type = data_type
        self.children = []
        self.modifieable = modifieable
        self.new_ref = new_ref
        self.back_link = back_link
        self.configure_value()
        
        AttributeCell._data_types.update(data_type)
        
    def unfocus(self):
        match self.data_type.rsplit("-", 1)[-1]:
            case "ref"|"str"|"int"|"float":
                if hasattr(self, "display"):
                    self.display.unfocus()
            case _:
                pass
    
    def get_value(self):
        match self.data_type.rsplit("-", 1)[-1]:
            case "ref":
                return self.value.ref_id
            case "str":
                self.value = self.display.get_content()
            case "int":
                self.value = int(self.display.get_content())
            case "float":
                self.value = float(self.display.get_content())
            case "bool":
                self.value = self.toggle.state

        return self.value
    
    def setup_function(self, return_type):
        ico = Text(2, 3, 1, f"f(x) -> {return_type}", text_bg_color=None)
        self.children.append(ico)
        self.width = 180
        self.height = 24
    
    def toggle_sfx(self, state):
        self.editor.sound_system.get_audio(f"AESA_tick{1 if state else 2}", "editor").play()
        
        def redo():
            self.toggle.set_state(state)
        
        def undo():
            self.toggle.set_state(not state)
        
        self.editor.add_history(redo, undo, "Toggled Switch")
        
    
    def configure_value(self):
        self.children.clear()
        match self.data_type.rsplit("-", 1)[-1]:
            case "str":
                if isinstance(self.value, (str, int, float, bool)):
                    self.display = CursorFocusTextBox(10, 3, 160, 18, self.editor, content=str(self.value), text_bg_color=None)
                    self.display.text_box.allow_typing = self.modifieable
                    self.children.append(self.display)
                    self.width = 180
                    self.height = 24
                elif isinstance(self.value, dict):
                    self.setup_function("str")
            case "int":
                if isinstance(self.value, (int, float, bool)):
                    self.display = CursorFocusTextBox(10, 3, 160, 18, self.editor, content=str(int(self.value)), text_bg_color=None)
                    self.display.text_box.char_whitelist = [n for n in "0123456789"]
                    self.display.text_box.allow_typing = self.modifieable
                    self.children.append(self.display)
                    self.width = 180
                    self.height = 24
                elif isinstance(self.value, dict):
                    self.setup_function("int")
            case "float":
                if isinstance(self.value, (int, float, bool)):
                    self.display = CursorFocusTextBox(10, 3, 160, 18, self.editor, content=str(float(self.value)), text_bg_color=None)
                    self.display.text_box.char_whitelist = [n for n in "0123456789."]
                    self.display.text_box.allow_typing = self.modifieable
                    self.children.append(self.display)
                    self.width = 180
                    self.height = 24
                elif isinstance(self.value, dict):
                    self.setup_function("float")
            case "bool":
                if isinstance(self.value, (bool, int, float)):
                    self.toggle = ToggleSwitch(10, 3, 18, 0, self.value, TEXT_COLOR, (30, 200, 30), (200, 30, 30), TEXT_COLOR, ToggleSwitch.Style.SQUARE, True)
                    self.toggle.on_state_change(self.toggle_sfx)
                    if self.value: self.toggle.set_state(self.value)
                    self.children.append(self.toggle)
                elif isinstance(self.value, dict):
                    self.setup_function("bool")
            case "ref":
                self.display = CursorFocusTextBox(10, 3, 160, 18, self.editor, content=self.value.ref_id, text_bg_color=None)
                self.display.text_box.allow_typing = False
                self.display.set_text_color(TEXT_BG3_COLOR)
                self.children.append(self.display)
                self.width = 180
                self.height = 24
        
    def _event(self, editor, X, Y):
        self.editor = editor
        
        for child in self.children[::-1]:
            child._event(editor, X, Y)
    
    def _update(self, editor, X, Y):
        
        dw2 = min(X, 0)
        dh2 = min(Y, 0)
        
        editor.screen.fill(TEXT_BG2_COLOR, (X-dw2, Y-dh2, self.width+dw2, self.height+dh2))
        
        for child in self.children:
            child._update(editor, X, Y)

class CellSlot(UIElement):
    
    lock_icon = Image(f"{PATH}/advanced_editor/lock.png", 0, 0, 20, 20)
    
    def __init__(self, editor, parent, x:int, y:int, width:int, height:int, data_types:list, cell=None, locked=False, generator=False, ignored_values=None):
        self.editor = editor
        self.parent = parent
        self.x = x
        self.y = y
        self.width = self._width = width
        self.height = self._height = height
        self.data_types = data_types
        self.cell = cell
        self.locked = locked
        self.hovered = False
        self.empty_mouse = True
        self.generator = generator
        self.ignored_values = ignored_values or []
        self.has_add = False
        
        if isinstance(data_types, list):
            AttributeCell._data_types.update(*data_types)
        
        if self.cell and not generator:
            self.cell.slot = self
            
        if self.generator:
            self.label = Text(2, 2, 1, "Create Reference", text_bg_color=None)
        elif not self.locked:
            if isinstance(self.data_types, (list, tuple)) and (not any(re.findall(r"ref", t) for t in self.data_types)):
                self.add_button = Button(2, 2, -1, 20, "+", None, hover_color=None, click_color=None)
                self.add_button.on_left_click = self.on_add_clicked
                fields = []
                self.has_add = True
                for data_type in self.data_types:
                    def create(d):
                        def new_of_type(*_, **__):
                            if d in ["int", "float", "percent"]:
                                value = 0
                            elif d == "str":
                                value = ""
                            elif d == "bool":
                                value = False
                            else:
                                raise ValueError(f"default value not implemented for type '{data_type}'")
                            cell = AttributeCell(editor, value, d, True)
                            self.cell = cell
                            cell.slot = self
                            self.ctx_tree.close()
                            editor.sound_system.get_audio("AESA_vwoop2", "editor").play()
                            # print(f"making new '{d}' value!")
                            def undo():
                                self.cell = None
                                cell.slot = None
                            def redo():
                                self.cell = cell
                                cell.slot = self
                            editor.add_history(redo, undo, "Created new value")
                        return new_of_type
                    fields.append({f"  {data_type}": create(data_type)})
                
                # print(fields)
                self.ctx_tree = ContextTree(fields, 200, 20, group="main-ctx", hover_color=TEXT_BG2_COLOR, click_color=TEXT_BG2_COLOR)
                # self.ctx_tree.parent = self.add_button

    def get_ignored_values(self):
        out = self.ignored_values.copy()
        
        out += self.parent.get_reference_tree()
        
        return out
    
    def on_add_clicked(self, editor):
        # print("open context tree?")
        # self.ctx_tree.open()
        self.ctx_tree.openAtMouse(editor._e_instance)
        
    
    # def open_edit_ctx_tree(self):
    #     ...
    
    def _event(self, editor, X, Y):
        
        if not self.generator:
            if self.cell:
                self.cell._event(editor, X+self.x, Y+self.y)
                self.width = self.cell.width
                self.height = self.cell.height
            else:
                self.width = self._width
                self.height = self._height
                if (not self.locked) and self.has_add:
                    self.add_button._event(editor, X+self.x, Y+self.y)
        
        self.hovered = False
        editor._e_instance.check_hover(editor, (X+self.x, Y+self.y, self.width, self.height), self)
        
        if self.hovered:
            if self.generator:
                if editor.left_mouse_down():
                    ref = VisualLoader.ObjectReference(self.cell)
                    cell = AttributeCell(editor, ref, (self.data_types or "ref"), False, True, back_link=self.parent)
                    editor.holding = True
                    editor.held = cell
                    editor.hold_offset = (editor.mouse_pos[0]-(X+self.x), editor.mouse_pos[1]-(Y+self.y))
                    editor.sound_system.get_audio("AESA_vwoop1", "editor").play()
                    
            elif self.cell and not self.locked:
                if editor.left_mouse_down():
                    editor.holding = True
                    editor.held = self.cell
                    editor.hold_offset = (editor.mouse_pos[0]-(X+self.x), editor.mouse_pos[1]-(Y+self.y))
                    if self.cell.back_link and self.parent:
                        self.cell.back_link.referencers.remove(self.parent)
                    self.cell.unfocus()
                    # self.cell.slot = None
                    self.cell = None
                    editor.sound_system.get_audio("AESA_vwoop1", "editor").play()
                # if editor.right_mouse_down():
                #     self.open_edit_ctx_tree()
                if editor.holding:
                    self.empty_mouse = False
            elif editor.holding or editor.drop_requested:
                if isinstance(editor.held, AttributeCell) and not self.locked:
                    if editor.held.data_type in self.data_types and editor.held.get_value() not in self.get_ignored_values():
                        self.empty_mouse = True
                        
                        if editor.drop_requested:
                            editor.accept_drop(1, self.drop_acceptor)
                    else:
                        self.empty_mouse = False
                else:
                    self.empty_mouse = False
            else:
                self.empty_mouse = True
    
    def drop_acceptor(self, cell, editor):
        
        editor.sound_system.get_audio("AESA_vwoop2", "editor").play()
        
        if cell.new_ref:
            
            self.cell = cell
            cell.slot = self
            cell.new_ref = False
            
            if cell.back_link and self.parent:
                cell.back_link.referencers.append(self.parent)
                
            
            def undo():
                self.cell = None
                cell.slot = None
                cell.new_ref = True
                
                if cell.back_link and self.parent:
                    cell.back_link.referencers.remove(self.parent)
                
            def redo():
                self.cell = cell
                cell.slot = self
                cell.new_ref = False
                
                if cell.back_link and self.parent:
                    cell.back_link.referencers.append(self.parent)
            
            editor.add_history(redo, undo, "Added Attribute")
        else:
        
            old_slot = cell.slot
            
            self.cell = cell
            cell.slot = self
            
            if cell.back_link and self.parent:
                cell.back_link.referencers.append(self.parent)
            
            if old_slot is self:
                return
            
            def undo():
                
                self.cell = None
                old_slot.cell = cell
                cell.slot = old_slot
                
                if cell.back_link and self.parent:
                    cell.back_link.referencers.remove(self.parent)
            
            def redo():
                old_slot.cell = None
                self.cell = cell
                cell.slot = self
                
                if cell.back_link and self.parent:
                    cell.back_link.referencers.append(self.parent)
        
            editor.add_history(redo, undo, "Moved Attribute")

    def _update(self, editor, X, Y):
        dw = min(X+self.x-1, 0)
        dh = min(Y+self.y-1, 0)
        dw2 = min(X+self.x, 0)
        dh2 = min(Y+self.y, 0)
        if self.locked:
            editor.screen.fill(TEXT_BG3_COLOR, (X+self.x-1-dw, Y+self.y-1-dh, self.width+dw+2, self.height+dh+2))
            
        elif self.hovered and self.empty_mouse:
            editor.screen.fill((0, 120, 212), (X+self.x-1-dw, Y+self.y-1-dh, self.width+dw+2, self.height+dh+2))
            
        else:
            editor.screen.fill(TEXT_COLOR, (X+self.x-1-dw, Y+self.y-1-dh, self.width+dw+2, self.height+dh+2))
        
        if not self.cell:
            editor.screen.fill(TEXT_BG_COLOR, (X+self.x-dw2, Y+self.y-dh2, self.width+dw2, self.height+dh2))
        elif self.generator:
            editor.screen.fill(TEXT_BG2_COLOR, (X+self.x-dw2, Y+self.y-dh2, self.width+dw2, self.height+dh2))
        
        if self.locked:
            self.lock_icon._update(editor, (X+self.x+self.width+2) if self.cell else (X+self.x+(self.width/2)-10), (Y+self.y+(self.height/2))-10)
        
        if self.generator:
            self.label._update(editor, X+self.x, Y+self.y)
        elif self.cell:
            self.cell._update(editor, X+self.x, Y+self.y)
        elif self.has_add and not self.locked:
            self.add_button._update(editor, X+self.x, Y+self.y)


class VisualLoader:
    
    _engine_loaded = False
    _engine_editable = False
    
    class ObjectReference:
        def __init__(self, ref_id:str):
            self.ref_id = ref_id
            self.broken_reference = False
        
        def get_ref(self):
            return VisualLoader._refernce_map[self.ref_id.split(":", 1)[0]][self.ref_id]
    
        def get(self, data_name:str):
            self.get_ref().get(data_name)
    
        def set_ref(self, ref_id:str):
            self.ref_id = ref_id
        
        def set(self, data_name:str, value:Any):
            self.get_ref().set(data_name, value)
        
        def verify(self):
            valid = self.ref_id in VisualLoader._refernce_map[self.ref_id.split(":", 1)[0]].keys()
            self.broken_reference = not valid
            return valid
    
    class InheretenceLink:
        def __init__(self, reference, attr:str, fallback:dict=None):
            self.reference: VisualLoader.ObjectReference = reference
            self.attr = attr
            
            self.has_fallback = False
            self.fallback = None
            if fallback and self.attr in fallback.keys():
                self.has_fallback = True
                self.fallback = fallback[self.attr]
    
        def get(self):
            if self.reference:
                return self.reference.get(self.attr)
            else:
                return self.fallback
        
        def set(self, value:Any):
            if self.reference:
                self.reference.set(self.attr, value)
            elif self.has_fallback:
                self.fallback = value
        
        def verify(self):
            return bool(self.reference) or self.has_fallback
    
    class VisualObject:
        def __init__(self, source:str, dungeon:str, uid:str, data:dict, locked:bool=False):
            self.source = source
            self.dungeon = dungeon
            self.uid = uid
            self.data = data
            self.locked = locked
            
            VisualLoader._refernce_map[self.dungeon].update({self.uid: self})
        
        def __repr__(self):
            return f"VisualObject( {self.uid} )"
        
        def ref(self):
            return VisualLoader.ObjectReference(self.uid)
    
        def get(self, data_name:str, default=None):
            if data_name in self.data:
                obj = self.data[data_name]
                if isinstance(obj, VisualLoader.ObjectReference):
                    return obj.get_ref()
                return obj
            return default

        def get_raw(self, data_name:str, default=None):
            if data_name in self.data:
                return self.data[data_name]
            return default
        
        def set(self, data_name:str, value:Any):
            self.data.update({data_name: value})
        
        def verify(self):
            results = []
            
            for key, val in self.data.items():
                if isinstance(val, (VisualLoader.ObjectReference, VisualLoader.InheretenceLink, VisualLoader.VisualObject)):
                    results.append(val.verify())

            return all(results)

    class MissingValue:
        _instance = None
        def __new__(cls):
            if not cls._instance:
                cls._instance = super().__new__(cls)
            return cls._instance
    
        def split(self, *args, **kwargs):
            return "[unspecified]".split(*args, **kwargs)

        def __str__(self):
            return "[unspecified]"
        
        def lower(self):
            return "[unspecified]"
    
    _refernce_map: dict[str, dict[str, VisualObject]] = {}
    
    @classmethod
    def analyze_project_structure(cls, root:str, dungeon_id:str) -> list[str]|str:
        """
        returns the list of files returned from glob.glob  \n
        if there are errors with the file structure, returns a string instead
        """
        to_load: list[str] = []
        
        # issues = []
        
        if not os.path.exists(f"{root}/{dungeon_id}.json"):
            return f"Folder does not contain a '{dungeon_id}.json' file."
        # to_load.append(f"{root}/{dungeon_id}.json")
        
        to_load += glob.glob("**/*.ds", root_dir=root, recursive=True) + \
                   glob.glob("**/*.dungeon_script", root_dir=root, recursive=True) + \
                   glob.glob("**/*.json", root_dir=root, recursive=True)
        
        if f"{root}/vcfg.json" in to_load:
            to_load.remove(f"{root}/vcfg.json")
        
        return [t.replace("\\", "/") for t in to_load]
    
    @staticmethod
    def blank(*_, **__): pass
    
    @classmethod
    def error(cls, msg:str, loading_bar:LoadingBar, load_toast:Toasts.Toast, toasts:Toasts):
        loading_bar.fill_color = (255, 30, 30)
        loading_bar.set_max_progress(1)
        loading_bar.set_progress(1)
        # loading_bar.width -= 25
        
        ctb_frames = [
            Image(f"{PATH}/advanced_editor/close_button.png", 0, 0, 20, 20),
            Image(f"{PATH}/advanced_editor/close_button_hovered.png", 0, 0, 20, 20)
        ]
        
        close_toast_button = Button(loading_bar.x+loading_bar.width-20, loading_bar.y-25, 20, 20, "", ctb_frames[0], hover_color=ctb_frames[1], click_color=ctb_frames[1])
        toast2 = toasts.toast(msg, 0.1, (255, 30, 30))
        toast2.keep_showing = True
        
        def on_click_button(*_, **__):
            load_toast.remove()
            toast2.keep_showing = False
            close_toast_button.on_left_click = cls.blank
        close_toast_button.on_left_click = on_click_button
        load_toast.children.append(close_toast_button)
    
    _category_map = {
        "weapons": "weapon",
        "enemies": "enemy",
        "tools": "tool",
        "items": "item",
        "attacks": "attack",
        "combats": "combat",
        "status_effects": "status_effect",
        "rooms": "room",
        "scripts": "script"
    }
    
    @classmethod
    def load(cls, root:str, loading_bar:LoadingBar, load_toast:Toasts.Toast, toasts:Toasts, aesa, loading_engine=False):
        
        if not cls._engine_loaded:
            load_toast.text_dsiplay.set_content("Loading Engine resources...")
            cls._engine_loaded = True
            cls.load("./", loading_bar, load_toast, toasts, aesa, True)
            load_toast.text_dsiplay.set_content("Loading dungeon...")

        root = root.replace("\\", "/")
        dungeon_id = root.rsplit("/", 1)[-1]
        
        if dungeon_id in cls._refernce_map.keys():
            toasts.toast("dungeon already loaded.")
            load_toast.remove()
            return
        
        if loading_engine:
            dungeon_id = "engine"
            result = [f"resources/{f}".replace("\\", "/") for f in (glob.glob("**/*.json", root_dir="./resources", recursive=True) +\
                     glob.glob("**/*.ds", root_dir="./resources", recursive=True) + \
                     glob.glob("**/*.dundeon_script", root_dir="./resources", recursive=True))]
            # print(f"engine load: {result}")
        else:
            result = cls.analyze_project_structure(root, dungeon_id)
        
        
        if not isinstance(result, list):
            cls.error(result, loading_bar, load_toast, toasts)
        else:
            loading_bar.set_max_progress(len(result))
            
            cls._refernce_map.update({dungeon_id: {}})
            
            cls.build_visuals(root, loading_bar, load_toast, toasts, result, dungeon_id, aesa, loading_engine)

    @classmethod
    def build_visuals(cls, root:str, loading_bar:LoadingBar, load_toast:Toasts.Toast, toasts:Toasts, result:list[str], dungeon_id:str, aesa, loading_engine:bool):
        loaded = 0
        for file_name in result:
            if file_name.startswith("resources/"):
                if file_name.endswith(".json"): # weapon/tool/armor/etc
                    fn = file_name.replace("resources/", "", 1).replace(".json", "")
                    # print(file_name)
                    with open(f"{root}/{file_name}", "r+", encoding="utf-8") as f:
                        data: dict[str, Any] = json.load(f)
                    # analyze files, look for external references
                    if file_name.startswith("resources/weapons/"):
                        if "parent" in data:
                            parent = VisualLoader.ObjectReference(data["parent"])
                            vdata = {
                                "template": data.get("template", False),
                                "parent": parent,
                                "name": data.get("name", VisualLoader.MissingValue()),
                                "damage": VisualLoader.InheretenceLink(parent, "damage", data),
                                "range": VisualLoader.InheretenceLink(parent, "range", data),
                                "max_durability": VisualLoader.InheretenceLink(parent, "max_durability", data),
                                "durability": VisualLoader.InheretenceLink(parent, "durability", data)
                            }
                        else:
                            vdata = {
                                "template": data.get("template", False),
                                "parent": VisualLoader.MissingValue(),
                                "name": data.get("name", VisualLoader.MissingValue()),
                                "damage": data.get("damage", VisualLoader.MissingValue()),
                                "range": data.get("range", VisualLoader.MissingValue()),
                                "max_durability": data.get("max_durability", VisualLoader.MissingValue()),
                                "durability": data.get("durability", VisualLoader.MissingValue())
                            }

                        VisualLoader.VisualObject(file_name, dungeon_id, f"{dungeon_id}:{fn}", vdata, loading_engine)

                    elif file_name.startswith("resources/ammo/"):
                        if "parent" in data:
                            parent = VisualLoader.ObjectReference(data["parent"])
                            vdata = {
                                "template": data.get("template", False),
                                "parent": parent,
                                "name": data.get("name", VisualLoader.MissingValue()),
                                "description": VisualLoader.InheretenceLink(parent, "description", data),
                                "bonus_damage": VisualLoader.InheretenceLink(parent, "bonus_damage", data),
                                "max_count": VisualLoader.InheretenceLink(parent, "max_count", data),
                                "count": VisualLoader.InheretenceLink(parent, "count", data)
                            }
                        else:
                            vdata = {
                                "template": data.get("template", False),
                                "parent": VisualLoader.MissingValue(),
                                "name": data.get("name", VisualLoader.MissingValue()),
                                "description": data.get("description", VisualLoader.MissingValue()),
                                "bonus_damage": data.get("bonus_damage", VisualLoader.MissingValue()),
                                "max_count": data.get("max_count", VisualLoader.MissingValue()),
                                "count": data.get("count", VisualLoader.MissingValue()),
                            }

                        VisualLoader.VisualObject(file_name, dungeon_id, f"{dungeon_id}:{fn}", vdata, loading_engine)

                    elif file_name.startswith("resources/armor/"):
                        if "parent" in data:
                            parent = VisualLoader.ObjectReference(data["parent"])
                            vdata = {
                                "template": data.get("template", False),
                                "parent": parent,
                                "name": data.get("name", VisualLoader.MissingValue()),
                                "description": VisualLoader.InheretenceLink(parent, "description", data),
                                "damage_reduction": VisualLoader.InheretenceLink(parent, "damage_reduction", data),
                                "max_durability": VisualLoader.InheretenceLink(parent, "max_cdurability", data),
                                "durability": VisualLoader.InheretenceLink(parent, "durability", data),
                                "events": VisualLoader.InheretenceLink(parent, "events", data)
                            }
                        else:
                            vdata = {
                                "template": data.get("template", False),
                                "parent": VisualLoader.MissingValue(),
                                "name": data.get("name", VisualLoader.MissingValue()),
                                "description": data.get("description", VisualLoader.MissingValue()),
                                "damage_reduction": data.get("damage_reduction", VisualLoader.MissingValue()),
                                "max_durability": data.get("max_cdurability", VisualLoader.MissingValue()),
                                "durability": data.get("durability", VisualLoader.MissingValue()),
                                "events": data.get("events", VisualLoader.MissingValue())
                            }

                        VisualLoader.VisualObject(file_name, dungeon_id, f"{dungeon_id}:{fn}", vdata, loading_engine)
                        
                    elif file_name.startswith("resources/tools/"):
                        if "parent" in data:
                            parent = VisualLoader.ObjectReference(data["parent"])
                            vdata = {
                                "template": data.get("template", False),
                                "parent": parent,
                                "name": data.get("name", VisualLoader.MissingValue()),
                                "description": VisualLoader.InheretenceLink(parent, "description", data),
                                "data": VisualLoader.InheretenceLink(parent, "data", data),
                                "max_durability": VisualLoader.InheretenceLink(parent, "max_cdurability", data),
                                "durability": VisualLoader.InheretenceLink(parent, "durability", data),
                                "events": VisualLoader.InheretenceLink(parent, "events", data)
                            }
                        else:
                            vdata = {
                                "template": data.get("template", False),
                                "parent": VisualLoader.MissingValue(),
                                "name": data.get("name", VisualLoader.MissingValue()),
                                "description": data.get("description", VisualLoader.MissingValue()),
                                "data": data.get("data", VisualLoader.MissingValue()),
                                "max_durability": data.get("max_cdurability", VisualLoader.MissingValue()),
                                "durability": data.get("durability", VisualLoader.MissingValue()),
                                "events": data.get("events", VisualLoader.MissingValue())

                            }

                        VisualLoader.VisualObject(file_name, dungeon_id, f"{dungeon_id}:{fn}", vdata, loading_engine)
                        
                    elif file_name.startswith("resources/items/"):
                        if "parent" in data:
                            parent = VisualLoader.ObjectReference(data["parent"])
                            vdata = {
                                "template": data.get("template", False),
                                "parent": parent,
                                "name": data.get("name", VisualLoader.MissingValue()),
                                "description": VisualLoader.InheretenceLink(parent, "description", data),
                                "data": VisualLoader.InheretenceLink(parent, "data", data),
                                "events": VisualLoader.InheretenceLink(parent, "events", data),
                                "max_count": VisualLoader.InheretenceLink(parent, "max_count", data),
                                "count": VisualLoader.InheretenceLink(parent, "count", data)
                            }
                        else:
                            vdata = {
                                "template": data.get("template", False),
                                "parent": VisualLoader.MissingValue(),
                                "name": data.get("name", VisualLoader.MissingValue()),
                                "description": data.get("description", VisualLoader.MissingValue()),
                                "data": data.get("data", VisualLoader.MissingValue()),
                                "events": data.get("events", VisualLoader.MissingValue()),
                                "max_count": data.get("max_count", VisualLoader.MissingValue()),
                                "count": data.get("count", VisualLoader.MissingValue()),
                            }

                        VisualLoader.VisualObject(file_name, dungeon_id, f"{dungeon_id}:{fn}", vdata, loading_engine)
                        
                    elif file_name.startswith("resources/enemies/"):
                        ...
                    elif file_name.startswith("resources/attacks/"):
                        ...
                    elif file_name.startswith("resources/status_effects/"):
                        ...
                    elif file_name.startswith("resources/sounds/"):
                        ...
                    elif file_name.startswith("resources/loot_tables/"):
                        ...
                    elif file_name.startswith("resources/interactable/"):
                        ...

            elif file_name.startswith("rooms/"):
                if file_name.endswith(".json"):
                    fn = f"{dungeon_id}/{file_name.replace(".json", "")}"
                    
                    with open(f"{root}/{file_name}", "r+", encoding="utf-8") as f:
                        data: dict[str, Any] = json.load(f)
                    
                    events: dict = data.get("events", {})
                    
                    vdata = {
                        "name": data.get("name", VisualLoader.MissingValue()),
                        "on_enter": events.get("on_enter", VisualLoader.MissingValue()),
                        "on_exit": events.get("on_exit", VisualLoader.MissingValue()),
                        "on_input": events.get("on_input", VisualLoader.MissingValue()),
                        "interactions": data.get("interactions", VisualLoader.MissingValue())
                    }
                    
                    VisualLoader.VisualObject(file_name, dungeon_id, fn, vdata)
                    
            elif file_name.startswith("scripts/"):
                if file_name.endswith((".ds", ".dungeon_script")):
                    fn = f"{dungeon_id}/{file_name.replace(".dungeon_script", "").replace(".ds", "")}"
                    
                    VisualLoader.VisualObject(file_name, dungeon_id, fn, {"file": f"Dungeons/{dungeon_id}/{file_name}"}, loading_engine)
                    
            elif file_name.startswith("combats/"):
                ... # special combat editor system is required first

            loaded += 1
            loading_bar.set_progress(loaded)


        missing = []
        
        if not loading_engine:
            if os.path.exists(f"{root}/vcfg.json"):
                with open(f"{root}/vcfg.json", "r+", encoding="utf-8") as f:
                    config = json.load(f)
            else:
                with open(f"{root}/vcfg.json", "w+", encoding="utf-8") as f:
                    f.write("{}")
                config = {}
        else:
            config = {}

        load_toast.text_dsiplay.set_content("Building Panels...")
        for id, ref in VisualLoader._refernce_map[dungeon_id].items():
            if not ref.verify():
                missing.append(ref)
            
            if id not in config:
                config.update({id: "stashed"})
            # print(f"id : {id}")
            cat = re.match(f"(?:{dungeon_id}(?::|/))(?P<category>[^/]+)(?:/)", id).groupdict()["category"]
            category = cls._category_map.get(cat, cat)
            panel_data = {"ref": ref, "type": f"{category}-base"}
            if config[id] == "stashed":
                aesa.create_stashed_panel(category, (300, 400), ref.get("name", id), id, True, ref.get("keywords", []) + [dungeon_id], panel_data=panel_data)
            
            else:
                panel = aesa.create_panel(category, (config[id][0], config[id][1], 300, 400), ref.get("name", id), id, True, ref.get("keywords", []) + [dungeon_id], panel_data=panel_data)

                aesa.visibility_groups[panel.shelf_panel.category].append(panel)
                
                shelf_panel = aesa.object_tree.tree[-1]
                placer = PanelPlacer(shelf_panel)
                shelf_panel._placer = placer


        # print(missing)
        # print(cls._refernce_map)

        if not loading_engine:
            toasts.toast(f"Panels loaded!" + (f"\n{len(missing)} object{'s have' if len(missing) > 1 else " has"} broken or unloaded references." if missing else ""))
            with open(f"{root}/vcfg.json", "w+", encoding="utf-8") as f:
                json.dump(config, f)

        load_toast.keep_showing = False

