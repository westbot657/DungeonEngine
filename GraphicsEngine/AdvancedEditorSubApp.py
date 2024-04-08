# pylint: disable=[W,R,C, import-error]

import tkinter.filedialog
from UIElement import UIElement
from RenderPrimitives import Image
from Options import PATH
from AttributePanel import AttributePanel
from ConstructionCanvas import ConstructionCanvas
from FunctionalElements import Button, BorderedButton
from AdvancedPanels.PanelTree import PanelTree
from AdvancedPanels.ShelfPanel import ShelfPanel
from CursorFocusTextBox import CursorFocusTextBox
from VisualCFG import VisualCFG
import tkinter
from threading import Thread

import json
import os

class VisibilityToggle:
    def __init__(self, sub_app, typ, button, alt_text1, alt_text2, frames):
        self.sub_app = sub_app
        self.typ = typ
        self.button = button
        self.alt_text1 = alt_text1
        self.alt_text2 = alt_text2
        self.frames = frames
        
    def __call__(self, *_, set=None, **__):
        if set is not None:
            self.sub_app.visibility_toggled[self.typ] = not set
        if self.sub_app.visibility_toggled[self.typ]:
            self.button._alt_text = self.alt_text2
            self.button._bg_color = self.button.bg_color = self.frames[0]
            self.button.hover_color = self.frames[1]
        else:
            self.button._alt_text = self.alt_text1
            self.button._bg_color = self.button.bg_color = self.frames[2]
            self.button.hover_color = self.frames[3]
            
        self.sub_app.visibility_toggled[self.typ] = not self.sub_app.visibility_toggled[self.typ]



class AdvancedEditorSubApp(UIElement):
    
    def __init__(self, code_editor, editor):
        self.code_editor = code_editor
        self.editor = editor
        self.children = []
        self.popouts = {}
        
        self.construction_canvas = ConstructionCanvas(self, editor, 102, 22, editor.width-452, editor.height-111)
        self.children.append(self.construction_canvas)
        
        self.visibility_types = [
            None,
            "weapon", "ammo", "armor", "item", None,
            "road", "room", None,
            "enemies", "combat", None,
            "script",
            None
        ]
        
        self.visibility_offsets = {}
        self.visibility_icons = {}
        self.visibility_toggles = {}
        self.visibility_toggled = {}
        self.visibility_groups = {}
        self.empty_visibility_toggle_spots = []
        
        self.search_box = CursorFocusTextBox(editor.width-350, 27, 348, 30, editor, "search...")
        self.children.append(self.search_box)
        
        self.object_tree = PanelTree(editor.width-352, 57, 350, editor.height-111, editor)
        self.children.append(self.object_tree)
        
        self.object_tree.get_search = self.search_box.get_content
        
        base_x = 102
        base_y = editor.height-100
        x_offset = 0
        seperator_width = 10
        
        for typ in self.visibility_types:
            if typ is None:
                img = Image(f"{PATH}/advanced_editor/empty_selector_spot.png", base_x+x_offset, base_y, seperator_width, 50)
                self.empty_visibility_toggle_spots.append(img)
                x_offset += seperator_width
                self.children.append(img)
                continue
            
            self.visibility_offsets.update({typ: x_offset})
            frames = [
                Image(f"{PATH}/advanced_editor/{typ}_visibility_selector.png", 0, 0, 50, 50),
                Image(f"{PATH}/advanced_editor/{typ}_visibility_selector_hovered.png", 0, 0, 50, 50),
                Image(f"{PATH}/advanced_editor/{typ}_visibility_selector_selected.png", 0, 0, 50, 50),
                Image(f"{PATH}/advanced_editor/{typ}_visibility_selector_selected_hovered.png", 0, 0, 50, 50)
            ]
            self.visibility_icons.update({typ: frames})
            
            button = Button(base_x+x_offset, base_y, 50, 50, "", frames[2], hover_color=frames[3], click_color=frames[2])
            alt_text1 = f"Hide {typ}" + ("" if typ in ["armor", "ammo", "enemies"] else "s")
            alt_text2 = f"Show {alt_text1[5:]}"
            button._alt_text = alt_text1
            self.visibility_toggled.update({typ: True})
            
            on_click = VisibilityToggle(self, typ, button, alt_text1, alt_text2, frames)
            self.visibility_toggles.update({typ: (button, on_click)})

            button.on_left_click = on_click
            self.children.append(button)
            self.visibility_groups.update({typ: []})
            x_offset += 50
        
        img = Image(f"{PATH}/advanced_editor/selector_block.png", base_x+x_offset, base_y, 25, 79)
        x_offset += 25
        self.children.append(img)
        self.empty_visibility_toggle_spots.append(img)
        
        self.open_dungeon_button = BorderedButton(base_x+x_offset+10, base_y+30, -1, None, " Open Dungeon... ")
        self.open_dungeon_button.on_left_click = self.click_load_dungeon
        self.children.append(self.open_dungeon_button)
        self.to_open = ""
        self.selected_directory = False
        self.getting_directory = False
        self.dir_getter = None
    
    def get_directory_task_thread(self):
        self.getting_directory = True
        self.selected_directory = False
        self.to_open = tkinter.filedialog.askdirectory(initialdir="./Dungeons/", title="Open Dungeon...")
        self.selected_directory = True
        self.getting_directory = False
    
    def click_load_dungeon(self, *_, **__):
        if not self.getting_directory:
            t = Thread(target=self.get_directory_task_thread)
            t.daemon = True
            t.start()
            self.dir_getter = t
    
    def _load_dungeon(self):
        VisualCFG.load(self.to_open)
        
    
    def load_dungeon(self):
        t = Thread(target=self._load_dungeon)
        t.daemon = True
        t.start()
    
    def create_panel(self, rect:tuple[int, int, int, int], label, bordered=False, tags=None, shelf_panel_height=35) -> AttributePanel:
        attr_panel = AttributePanel(*rect, bordered=bordered)
        self.create_shelf_panel(attr_panel, label, tags, shelf_panel_height)
        return attr_panel
    
    def create_shelf_panel(self, attribute_panel, label, tags=None, height=35):
        shelf_panel = ShelfPanel(340, height, label, attribute_panel, self.construction_canvas.canvas, self.object_tree._canvas, tags)
        self.object_tree.tree.append(shelf_panel)
    
    def _update(self, editor, X, Y):
        for child in self.children:
            child._update(editor, X, Y)
    
    def _event(self, editor, X, Y):
        
        if self.selected_directory:
            self.selected_directory = False
            if self.to_open:
                self.load_dungeon()
        
        if editor._do_layout_update:
            self._update_layout(editor)
        
        for child in self.children[::-1]:
            child._event(editor, X, Y)
            
    def _update_layout(self, editor):
        for button, _ in self.visibility_toggles.values():
            button.y = editor.height-100
        for blank in self.empty_visibility_toggle_spots:
            blank.y = editor.height-100
        
        self.construction_canvas.width = editor.width-452
        self.construction_canvas.height = editor.height-111
        self.construction_canvas.rebuild()
        self.search_box.x = editor.width-350
        self.object_tree.x = editor.width-352
        self.object_tree.height = editor.height-111
        self.open_dungeon_button.y = editor.height-70
