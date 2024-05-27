# pylint: disable=[W,R,C, import-error, no-member]

from UIElement import UIElement
from RenderPrimitives import Image
from Options import PATH
from AttributePanel import AttributePanel
from ConstructionCanvas import ConstructionCanvas
from FunctionalElements import Button, BorderedButton
from AdvancedPanels.PanelTree import PanelTree
from AdvancedPanels.ShelfPanel import ShelfPanel
from CursorFocusTextBox import CursorFocusTextBox
from VisualLoader import VisualLoader, CellSlot, AttributeCell
from Toasts import Toasts
from LoadingBar import LoadingBar
from Pathfinding import Pathfinding
from SoundSystem import SoundSystem
from MultilineTextBox import MultilineTextBox

from AdvancedPanels.PanelPlacer import PanelPlacer

from threading import Thread
import tkinter.filedialog
import tkinter
import pygame

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
            self.sub_app.editor.sound_system.get_audio("AESA_click2", "editor").play()
        else:
            self.button._alt_text = self.alt_text1
            self.button._bg_color = self.button.bg_color = self.frames[2]
            self.button.hover_color = self.frames[3]
            self.sub_app.editor.sound_system.get_audio("AESA_click", "editor").play()
            
        self.sub_app.visibility_toggled[self.typ] = not self.sub_app.visibility_toggled[self.typ]



class AdvancedEditorSubApp(UIElement):
    
    def __init__(self, code_editor, editor):
        self.code_editor = code_editor
        self.editor = editor
        self.children = []
        self.popouts = {}
        
        editor.sound_system.load(f"{PATH}/audio_assets/pick_up.wav", "AESA_pick_up", "editor")
        editor.sound_system.load(f"{PATH}/audio_assets/drop.wav",    "AESA_drop",    "editor")
        editor.sound_system.load(f"{PATH}/audio_assets/thud.wav",    "AESA_thud",    "editor")
        editor.sound_system.load(f"{PATH}/audio_assets/thud2.wav",   "AESA_thud2",   "editor")
        editor.sound_system.load(f"{PATH}/audio_assets/click.wav",   "AESA_click",   "editor")
        editor.sound_system.load(f"{PATH}/audio_assets/click2.wav",  "AESA_click2",  "editor")
        editor.sound_system.load(f"{PATH}/audio_assets/bloop1.wav",  "AESA_bloop1",  "editor")
        editor.sound_system.load(f"{PATH}/audio_assets/bloop2.wav",  "AESA_bloop2",  "editor")
        editor.sound_system.load(f"{PATH}/audio_assets/vibrate.wav", "AESA_vibrate", "editor")
        editor.sound_system.load(f"{PATH}/audio_assets/beep.wav",    "AESA_beep",    "editor")
        
        self.toasts = Toasts(editor.width-355, editor.height-20, 350)
        
        self.construction_canvas = ConstructionCanvas(self, editor, 102, 22, editor.width-452, editor.height-111)
        self.children.append(self.construction_canvas)
        
        self.canvas_action_hint_mask = pygame.Surface((editor.width-452, editor.height-111), pygame.SRCALPHA, 32)
        self.canvas_action_hint_mask.fill((0, 0, 0))
        self.canvas_action_hint_mask.set_alpha(10)
        self.canvas_action_hint_fade = 0
        self.canvas_action_hint = Image(f"{PATH}/advanced_editor/canvas_action_hint.png", 0, 0, 55, 55)
        
        self.shelf_action_hint_mask = pygame.Surface((350, editor.height-81), pygame.SRCALPHA, 32)
        self.shelf_action_hint_mask.fill((0, 0, 0))
        self.shelf_action_hint_mask.set_alpha(10)
        self.shelf_action_hint_fade = 0
        self.shelf_action_hint = Image(f"{PATH}/advanced_editor/shelf_action_hint.png", 0, 0, 55, 55)
        
        self.visibility_types = [
            None,
            "weapon", "ammo", "armor", "item", "tool", None,
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
        
        empty = Image(f"{PATH}/advanced_editor/empty_selector_spot.png", base_x+x_offset, base_y, seperator_width, 50)
        
        self.end_fill = empty.resize(editor.width-base_x+x_offset, empty.height)
        self.children.append(self.end_fill)
        self.empty_visibility_toggle_spots.append(self.end_fill)
        
        for typ in self.visibility_types:
            if typ is None:
                # e = empty.copy()
                # self.empty_visibility_toggle_spots.append(e)
                x_offset += seperator_width
                # self.children.append(e)
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
        
        
        self.open_dungeon_button = BorderedButton(base_x+x_offset+10, base_y+30, -1, None, " Open Dungeon ")
        self.open_dungeon_button.on_left_click = self.click_load_dungeon
        self.children.append(self.open_dungeon_button)
        self.to_open = ""
        self.selected_directory = False
        self.getting_directory = False
        self.dir_getter = None
        
        # self.create_stashed_panel("weapon", (200, 400), "Longsword", True, ["weapon", "melee"])
        # self.create_stashed_panel("weapon", (300, 400), "Shortsword", True, ["weapon", "melee"])
        # self.create_stashed_panel("weapon", (300, 400), "Broadsword", True, ["weapon", "melee"])
        # self.create_stashed_panel("weapon", (300, 400), "Bow", True, ["weapon", "ranged"])
        # self.create_stashed_panel("weapon", (300, 400), "Crossbow", True, ["weapon", "ranged"])
    
    def get_directory_task_thread(self):
        self.getting_directory = True
        self.selected_directory = False
        self.to_open = tkinter.filedialog.askdirectory(initialdir="./Dungeons/", title="Open Dungeon...")
        self.selected_directory = True
        self.getting_directory = False
    
    def click_load_dungeon(self, *_, **__):
        if not self.getting_directory:
            self.editor.sound_system.get_audio("AESA_click", "editor").play()
            t = Thread(target=self.get_directory_task_thread)
            t.daemon = True
            t.start()
            self.dir_getter = t
    
    def _load_dungeon(self):
        toast = self.toasts.toast("Loading dungeon...", 0, (10, 200, 30))
        loading_bar = LoadingBar(5, toast.height-5, toast.width-10, 15)
        toast.height += 25
        toast.children.append(loading_bar)
        toast.refresh()
        toast.keep_showing = True
        VisualLoader.load(self.to_open, loading_bar, toast, self.toasts, self)
        
        
    
    def load_dungeon(self):
        t = Thread(target=self._load_dungeon)
        t.daemon = True
        t.start()
    
    def create_stashed_panel(self, category, size:tuple[int, int], label:str, id:str, bordered=False, tags=None, shelf_panel_height=35, panel_data=None):
        panel = self.create_panel(category, (0, 0, size[0], size[1]), label, id, bordered, tags, shelf_panel_height, panel_data)
        shelf_panel = self.object_tree.tree[-1]
        placer = PanelPlacer(shelf_panel)
        shelf_panel.placer = shelf_panel._placer = placer
    
    def create_panel(self, category, rect:tuple[int, int, int, int], label, id, bordered=False, tags=None, shelf_panel_height=35, panel_data=None) -> AttributePanel:
        attr_panel = AttributePanel(self.construction_canvas.canvas, self, *rect, bordered=bordered, data=panel_data)
        self.create_shelf_panel(category, attr_panel, label, id, tags, shelf_panel_height, panel_data)
        return attr_panel
    
    def create_shelf_panel(self, category, attribute_panel, label, id, tags=None, height=35, panel_data=None):
        shelf_panel = ShelfPanel(340, height, label, id, category, attribute_panel, self.construction_canvas.canvas, self.object_tree._canvas, tags, panel_data["ref"].locked)
        attribute_panel.shelf_panel = shelf_panel
        self.object_tree.tree.append(shelf_panel)
    
    
    
    def panel_placer_acceptor(self, panel_placer, editor):
        shelf = panel_placer.parent_shelf
        panel = shelf.attr_panel
        mx, my = self.construction_canvas.get_relative_mouse(*editor.mouse_pos)
        x = (mx-(panel.width/2)) + 50
        y = (my-(panel.height/2)) + 50
        
        x = (100*(x//100))
        y = (100*(y//100))
        
        panel.x = panel._x = x
        panel.y = panel._y = y
        
        panel.set_glow(0.75)
        editor.sound_system.get_audio("AESA_thud", "editor").play()
        
        self.visibility_groups[shelf.category].append(panel)
        
        def redo():
            panel.x = panel._x = x
            panel.y = panel._y = y
            panel.set_glow(0.75)
            self.visibility_groups[shelf.category].append(panel)
            shelf.placer = None
        
        def undo():
            self.visibility_groups[shelf.category].remove(panel)
            shelf.placer = shelf._placer
        
        editor.add_history(redo, undo, "Placed Attribute Panel")
    
    def attribute_panel_acceptor(self, attr_panel, editor):
        mx, my = self.construction_canvas.get_relative_mouse(*editor.mouse_pos)
        
        x = (100*((mx - (editor.hold_offset[0])+50)//100))
        y = (100*((my - (editor.hold_offset[1])+50)//100))
        
        _x = attr_panel._x
        _y = attr_panel._y
        
        attr_panel.x = attr_panel._x = x
        attr_panel.y = attr_panel._y = y
        
        self.visibility_groups[attr_panel.shelf_panel.category].append(attr_panel)
        editor.sound_system.get_audio("AESA_thud", "editor").play()
        
        def redo():
            attr_panel.x = attr_panel._x = x
            attr_panel.y = attr_panel._y = y
        
        def undo():
            attr_panel.x = attr_panel._x = _x
            attr_panel.y = attr_panel._y = _y
        
        editor.add_history(redo, undo, "Moved Attribute Panel")
        
    
    def attribute_panel_acceptor_2(self, attr_panel, editor):
        x = attr_panel._x
        y = attr_panel._y
        
        attr_panel.shelf_panel.placer = attr_panel.shelf_panel._placer
        self.editor.sound_system.get_audio("AESA_drop", "editor").play()
        
        
        def redo():
            self.visibility_groups[attr_panel.shelf_panel.category].remove(attr_panel)
            attr_panel.shelf_panel.placer = attr_panel.shelf_panel._placer
            
        def undo():
            attr_panel.x = attr_panel._x = x
            attr_panel.y = attr_panel._y = y
            attr_panel.shelf_panel.placer = None
            self.visibility_groups[attr_panel.shelf_panel.category].append(attr_panel)
        
        editor.add_history(redo, undo, "Stashed Attribute Panel")

    def attr_cell_acceptor(self, cell, editor):
        if cell.new_ref: return
        
        slot = cell.slot
        def redo():
            # print(f"set None as cell of slot '{slot}'")
            slot.cell = None
            cell.slot = None
        
        def undo():
            # print(f"set '{cell}' as cell of slot '{slot}'")
            slot.cell = cell
            cell.slot = slot
        
        editor.add_history(redo, undo, "Removed attribute")

    def _update_layout(self, editor):
        for button, _ in self.visibility_toggles.values():
            button.y = editor.height-100
        for blank in self.empty_visibility_toggle_spots:
            blank.y = editor.height-100
        self.end_fill.width = editor.width - 450
        
        self.construction_canvas.width = editor.width-452
        self.construction_canvas.height = editor.height-111
        
        self.canvas_action_hint_mask = pygame.transform.scale(self.canvas_action_hint_mask, (max(1, editor.width-452), max(1, editor.height-111)))
        self.shelf_action_hint_mask = pygame.transform.scale(self.shelf_action_hint_mask, (350, max(1, editor.height-81)))
        
        self.construction_canvas.rebuild()
        self.search_box.x = editor.width-350
        self.object_tree.x = editor.width-352
        self.object_tree.height = editor.height-111
        self.open_dungeon_button.y = editor.height-70
        self.toasts.x = editor.width-355
        self.toasts.y = editor.height-20

    def _event(self, editor, X, Y):
        
        if self.selected_directory:
            self.selected_directory = False
            if self.to_open:
                self.load_dungeon()
        
        if editor._do_layout_update:
            self._update_layout(editor)
        
        for child in self.children[::-1]:
            child._event(editor, X, Y)
            
        if MultilineTextBox._focused is None:
            for key in editor.typing:
                if key == "\x1a":
                    if pygame.K_LSHIFT in editor.keys:
                        # print("redo!")
                        editor.redo()
                    else:
                        # print("undo!")
                        editor.undo()
        
        if editor.holding:
            if isinstance(editor.held, (PanelPlacer, AttributePanel)):
                if editor.collides(editor.mouse_pos, (self.construction_canvas.x, self.construction_canvas.y, self.construction_canvas.width, self.construction_canvas.height)):
                    if self.shelf_action_hint_fade < 80:
                        self.shelf_action_hint_fade = min(max(self.shelf_action_hint_fade+20, 10), 80)
                        self.shelf_action_hint_mask.set_alpha(self.shelf_action_hint_fade)
                    else:
                        self.shelf_action_hint_fade = 90
                    if self.canvas_action_hint_fade > 10:
                        self.canvas_action_hint_fade = min(max(self.canvas_action_hint_fade-20, 10), 80)
                        self.canvas_action_hint_mask.set_alpha(self.canvas_action_hint_fade)
                    else:
                        self.canvas_action_hint_fade = 0
                else:
                    if self.shelf_action_hint_fade > 10:
                        self.shelf_action_hint_fade = min(max(self.shelf_action_hint_fade-20, 10), 80)
                        self.shelf_action_hint_mask.set_alpha(self.shelf_action_hint_fade)
                    else:
                        self.shelf_action_hint_fade = 0
                    if self.canvas_action_hint_fade < 80:
                        self.canvas_action_hint_fade = min(max(self.canvas_action_hint_fade+20, 10), 80)
                        self.canvas_action_hint_mask.set_alpha(self.canvas_action_hint_fade)
                    else:
                        self.canvas_action_hint_fade = 90
        else:
            self.canvas_action_hint_fade = 0
            self.shelf_action_hint_fade = 0
        
        if editor.drop_requested:
            
            # vv if colliding with the construction canvas vv
            canvas_collision = editor.collides(editor.mouse_pos, (self.construction_canvas.x, self.construction_canvas.y, self.construction_canvas.width, self.construction_canvas.height))
            
            if isinstance(editor.held, PanelPlacer) and canvas_collision:
                editor.accept_drop(1, self.panel_placer_acceptor)
            elif isinstance(editor.held, AttributePanel):
                if canvas_collision:
                    editor.accept_drop(1, self.attribute_panel_acceptor)
                else:
                    editor.accept_drop(0, self.attribute_panel_acceptor_2)
            elif isinstance(editor.held, AttributeCell):
                editor.accept_drop(0, self.attr_cell_acceptor)
        
        self.toasts._event(editor, X, Y)
    
    def _update(self, editor, X, Y):
        for child in self.children:
            child._update(editor, X, Y)
            
        if self.canvas_action_hint_fade:
            editor.screen.blit(self.canvas_action_hint_mask, (102, 22))
            self.canvas_action_hint._update(editor, 102+(self.construction_canvas.width/2)-(27.5), 22+(self.construction_canvas.height/2)-(27.5))
        
        if self.shelf_action_hint_fade:
            editor.screen.blit(self.shelf_action_hint_mask, (self.object_tree.x, self.search_box.y-5))
            self.shelf_action_hint._update(editor, self.object_tree.x+(self.object_tree.width/2)-(27.5), self.search_box.y+((self.search_box.height+self.object_tree.height)/2)-(27.5))
            
        self.toasts._update(editor, X, Y)

