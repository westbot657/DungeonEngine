# pylint: disable=W,R,C,import-error

from UIElement import UIElement
from AdvancedPanels.PanelTextBox import PanelTextBox
from VisualLoader import VisualLoader, CellSlot, AttributeCell
from Options import PATH, TEXT_COLOR, TEXT_BG_COLOR, TEXT_BG2_COLOR, TEXT_BG3_COLOR
from ConstructionCanvas import ConstructionCanvas
from FunctionalElements import Button, BorderedButton
from ContextTree import ContextTree
from RenderPrimitives import Image
from Text import Text

import pygame
import time
import math

class CellEditor(UIElement):
    
    class TransferSlot(UIElement):
        def __init__(self, parent, x, y, width, height, hide_add=False):
            self.parent = parent
            self.x = x
            self.y = y
            self.width = self._width = width
            self.height = self._height = height
            self.hide_add = hide_add
            
            self.label = Text(0, -20, 1, "Cell Editor", text_bg_color=None)
            
            self.cell = None
            self.hovered = False
            self.empty_mouse = True
            
            self.add_button = Button(2, 2, -1, 20, "+", None, hover_color=None, click_color=None)
            self.add_button.on_left_click = self.on_add_clicked
            
            self.ctx_tree = ContextTree(
                [
                    {
                        "  int": self.new_int,
                        "  float": self.new_float,
                        # "  percent": self.new_percent,
                        "  str": self.new_str,
                        "  bool": self.new_bool,
                    },
                    ContextTree.Line(),
                    {
                        "  f(x) -> int": self.new_f_int,
                        "  f(x) -> float": self.new_f_float,
                        # "  f(x) -> percent: self.new_f_percent"
                        "  f(x) -> str": self.new_f_str,
                        "  f(x) -> bool": self.new_f_bool,
                    }
                ], 200, 20, group="main-ctx", hover_color=TEXT_BG3_COLOR, click_color=TEXT_BG3_COLOR
            )
        
        def on_add_clicked(self, editor):
            self.ctx_tree.openAtMouse(editor._e_instance)
        
        def hist(self, cell, editor):
            editor.sound_system.get_audio("AESA_vwoop2", "editor").play()
            
            # old_slot = cell.slot
            
            def undo():
                self.cell = None
                cell.slot = None
                
                # old_slot.cell = cell
            def redo():
                # old_slot.cell = None
                
                self.cell = cell
                cell.slot = self
            
            editor.add_history(redo, undo, "Created value")
        
        def new_int(self, editor):
            cell = AttributeCell(editor, 0, "int", True)
            self.cell = cell
            cell.slot = self
            self.ctx_tree.close()
            self.hist(cell, editor)
        def new_float(self, editor):
            cell = AttributeCell(editor, 0, "float", True)
            self.cell = cell
            cell.slot = self
            self.ctx_tree.close()
            self.hist(cell, editor)
        def new_str(self, editor):
            cell = AttributeCell(editor, "", "str", True)
            self.cell = cell
            cell.slot = self
            self.ctx_tree.close()
            self.hist(cell, editor)
        def new_bool(self, editor):
            cell = AttributeCell(editor, False, "bool", True)
            self.cell = cell
            cell.slot = self
            self.ctx_tree.close()
            self.hist(cell, editor)
        def new_f_int(self, editor):
            cell = AttributeCell(editor, {}, "int", True)
            self.cell = cell
            cell.slot = self
            self.ctx_tree.close()
            self.hist(cell, editor)
        def new_f_float(self, editor):
            cell = AttributeCell(editor, {}, "float", True)
            self.cell = cell
            cell.slot = self
            self.ctx_tree.close()
            self.hist(cell, editor)
        def new_f_str(self, editor):
            cell = AttributeCell(editor, {}, "str", True)
            self.cell = cell
            cell.slot = self
            self.ctx_tree.close()
            self.hist(cell, editor)
        def new_f_bool(self, editor):
            cell = AttributeCell(editor, {}, "bool", True)
            self.cell = cell
            cell.slot = self
            self.ctx_tree.close()
            self.hist(cell, editor)
            
        def drop_acceptor(self, cell, editor):
            
            editor.sound_system.get_audio("AESA_vwoop2", "editor").play()
            
            
            old_slot = cell.slot
            
            self.cell = cell
            cell.slot = self
            
            if old_slot is self:
                return
            
            def undo():
                self.cell = None
                cell.slot = old_slot
                old_slot.cell = cell
                
            def redo():
                old_slot.cell = None
                self.cell = cell
                cell.slot = self
                
            editor.add_history(redo, undo, "Moved Attribute")

        
        def _event(self, editor, X, Y):
            
            if self.cell:
                self.cell._event(editor, X+self.x, Y+self.y)
                self.width = self.cell.width
                self.height = self.cell.height
            else:
                if not self.hide_add:
                    self.add_button._event(editor, X+self.x, Y+self.y)
                self.width = self._width
                self.height = self._height
            
            self.hovered = False
            editor._e_instance.check_hover(editor, (X+self.x, Y+self.y, self.width, self.height), self)
            
            if self.hovered:
                if self.cell:
                    if editor.left_mouse_down():
                        editor.holding = True
                        editor.held = self.cell
                        editor.hold_offset = (editor.mouse_pos[0]-(X+self.x), editor.mouse_pos[1]-(Y+self.y))
                        self.cell.unfocus()
                        self.cell = None
                        editor.sound_system.get_audio("AESA_vwoop1", "editor").play()
                        
                    if editor.holding:
                        self.empty_mouse = False
                elif editor.holding or editor.drop_requested:
                    if isinstance(editor.held, AttributeCell):
                        if editor.drop_requested:
                            editor.accept_drop(2, self.drop_acceptor)
                        
                        self.empty_mouse = True
                    else:
                        self.empty_mouse = False
                else:
                    self.empty_mouse = True
        
        def _update(self, editor, X, Y):
            dw = min(X+self.x-1, 0)
            dh = min(Y+self.y-1, 0)
            dw2 = min(X+self.x, 0)
            dh2 = min(Y+self.y, 0)

            if not self.hide_add:
                self.label._update(editor, X+self.x, Y+self.y)

            if self.hovered and self.empty_mouse:
                editor.screen.fill((0, 120, 212), (X+self.x-1-dw, Y+self.y-1-dh, self.width+dw+2, self.height+dh+2))
            
            else:
                editor.screen.fill(TEXT_COLOR, (X+self.x-1-dw, Y+self.y-1-dh, self.width+dw+2, self.height+dh+2))
        
            if not self.cell:
                editor.screen.fill(TEXT_BG_COLOR, (X+self.x-dw2, Y+self.y-dh2, self.width+dw2, self.height+dh2))
                if not self.hide_add:
                    self.add_button._update(editor, X+self.x, Y+self.y)
            else:
                self.cell._update(editor, X+self.x, Y+self.y)
    
    class CellStorage(UIElement):
        
        _drag = Image(f"{PATH}/advanced_editor/cell_storage_drag.png", 0, 0, 220, 15)
        _open = Image(f"{PATH}/advanced_editor/cell_storage_open.png", 0, 0, 15, 15)
        _close = Image(f"{PATH}/advanced_editor/cell_storage_close.png", 0, 0, 15, 15)
        

        def __init__(self, editor, parent, x:int, y:int):
            self.parent = parent
            self.editor = editor
            self.x = x
            self.y = y
            self.collapsed = True
            self.collapse_time = 0
            self.width = 220
            self.height = 360
            self.hovered = False
            self.offsetY = 0
            self.children = []
            self.toggle_hovered = False
            self.drag_hovered = False
            self.dragging = False
            
            # self._canvas = ConstructionCanvas._Canvas(editor, self)
            
            # self.mouse_pos = [0, 0]
            # self.screen = pygame.Surface((self.width-2, self.height))
            
            self.label = Text(0, 0, 1, "Cell Storage", text_bg_color=TEXT_BG_COLOR)
            self.label.x = self.width/2 - self.label.width/2
            
            self.drag_pos = 45
            self.dp = 45
            self.drag_offset = 0
            
            self.cells = []
            
            self.slots = []
            for i in range(10):
                self.slots.append(
                    CellEditor.TransferSlot(self, 10, (i*33)+15, 200, 24, True)
                )
    
        # def override_values(self, X, Y):
        #     self.mouse_pos = list(self.editor.mouse_pos)
        #     self.mouse_pos[0] -= self.x + X + 1
        #     self.mouse_pos[1] -= self.y + Y - self.dp + 15
        #     self.last_X = X
        #     self.last_Y = Y
    
        def _event(self, editor, X, Y):
            # self.override_values(X, Y)
            
            self.toggle_hovered = editor.collides(editor.mouse_pos, (X+self.x-15, Y+self.y, 15, 15))

            if self.toggle_hovered:
                if editor.left_mouse_down():
                    self.collapsed = not self.collapsed
                    self.collapse_time = time.time()
                    self.collapse_point = self.drag_pos
            
            if self.collapse_time:
                dt = (time.time() - self.collapse_time) * 3
                if dt >= 1:
                    self.collapse_time = 0
                    dt = 1
                if self.collapsed:
                    self.dp = math.sin((1-dt)/2 * math.pi) * self.drag_pos

                else:
                    self.dp = math.sin(dt/2 * math.pi) * self.drag_pos
            
            else:
                self.dp = 0 if self.collapsed else self.drag_pos
            
            if editor.collides(editor.mouse_pos, (X+self.x, Y+self.y - (self.drag_pos if not self.collapsed else 0), 220, 15)):
                if editor._e_instance._hovering is None:
                    self.drag_hovered = editor._e_instance._hovered = True
                    editor._e_instance._hovering = self
                else:
                    self.drag_hovered = False
            else:
                self.drag_hovered = False

            if self.drag_hovered:
                
                # editor._e_instance.override_cursor = True
                # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)
                
                if editor.left_mouse_down():
                    self.drag_offset = editor.mouse_pos[1] - (Y+self.y - self.dp)
                    # print(self.drag_offset)
                    self.dragging = True
                    self.collapsed = False
                
            
            if self.dragging and editor.mouse[0] is False and self.collapse_time == 0:
                self.dragging = False
                if self.drag_pos >= 45:
                    self.collapsed = False
                else:
                    self.collapsed = True
                    self.drag_pos = 45
                
            if self.dragging:
                self.drag_pos = min(max(0, (Y+self.y)-editor.mouse_pos[1]+self.drag_offset), self.height-15)

            for slot in self.slots:
                slot._event(editor, X+self.x+1, Y+self.y-self.dp+15)
                
                slot.x = (220-slot.width)/2


        def _update(self, editor, X, Y):
            
            if self.collapsed:
                self._open._update(editor, X+self.x-15, Y+self.y)
            else:
                self._close._update(editor, X+self.x-15, Y+self.y)
            
            if self.dp < 35:
                self.label._update(editor, X+self.x, Y+self.y-20)
            
            self._drag._update(editor, X+self.x, Y+self.y - self.dp)
            
            # self.screen.fill(TEXT_BG_COLOR)
            editor.screen.fill(TEXT_COLOR, (X+self.x, Y+self.y - self.dp+15, 220, self.dp+2))
            editor.screen.fill(TEXT_BG_COLOR, (X+self.x+1, Y+self.y - self.dp+15, 218, self.dp+1))
            
            # draw cells
            for slot in self.slots:
                slot._update(editor, X+self.x+1, Y+self.y-self.dp+15)
            
            
            
            # editor.screen.blit(self.screen, (X+self.x+1, Y+self.y - self.dp+15))
            
            if self.dp >= 35:
                self.label._update(editor, X+self.x, Y+self.y - self.dp + 10)
            
    class ConfigPane(UIElement):
        
        window_handles = (
            Image(f"{PATH}/advanced_editor/cell_edit_open_enabled.png", 0, 0, 15, 30),
            Image(f"{PATH}/advanced_editor/cell_edit_close_enabled.png", 0, 0, 15, 30),
            Image(f"{PATH}/advanced_editor/cell_edit_open_disabled.png", 0, 0, 15, 30)
        )
        
        def __init__(self, editor, parent, x:int, y:int, width:int, height:int):
            self.parent = parent
            self.editor = editor
            self.x = x
            self.y = y
            self.base_x = 102
            self.width = width
            self.height = self._height = height
            self.collapsed = True
            self.collapse_time = 0
            self.hovered = False
            self.offsetY = 0
            self.children = []
            
            self.cell = None
            self.screen = pygame.Surface((self.width, self.height-31))
            self.mouse_pos = [0, 0]
            
            self._canvas = ConstructionCanvas._Canvas(editor, self)
        
        def collides(self, mouse, rect) -> bool:
            mx, my = mouse
            x, y, w, h = rect
            
            if self.editor.collides(self.editor.mouse_pos, (self.x+self.last_X, self.y+self.last_Y, self.width, self.height)):
                return x <= mx < x+w and y < my < y+h
            
            return False
        
        def override_values(self, X, Y):
            self.mouse_pos = list(self.editor.mouse_pos)
            self.mouse_pos[0] -= self.x + X
            self.mouse_pos[1] -= self.y + Y + 30
            self.last_X = X
            self.last_Y = Y
        
        def reset(self):
            self.cell = None
            self.collapsed = True
            self.children.clear()
        
        def setup(self):
            self.children.clear()
            
            match self.cell.data_type:
                case "str":
                    ...
                case "int":
                    ...
                case "float":
                    ...
                case "bool":
                    ...
                case _:
                    pass
        
        def _event(self, editor, X, Y):
            self.override_values(X, Y)
            if self.height != self._height:
                self.screen = pygame.Surface((self.width, self.height-31))
            
            if self.collapse_time:
                dt = (time.time() - self.collapse_time) * 3
                if dt >= 1:
                    self.collapse_time = 0
                    dt = 1
                
                if self.collapsed:
                    # self.x = self.base_x - (self.width * dt)
                    self.x = self.base_x - (self.width - (self.width*math.sin((1-dt)/2*math.pi)))
                    
                else:
                    # self.x = self.base_x - (self.width - (self.width*dt))
                    self.x = self.base_x - (self.width - (self.width*math.sin(dt/2*math.pi)))
                    
            
            handle_collision = editor.collides(editor.mouse_pos, (self.x+self.width, self.y+((self.height/2)-15), 15, 30))
            
            if self.cell:
                if self.cell.slot.cell is None:
                    self.cell = None
            
            
            if self.cell:
                
                if handle_collision and editor.left_mouse_down():
                    self.collapsed = not self.collapsed
                    t = time.time()
                    if (dt := t - self.collapse_time) < 1:
                        self.collapse_time = t-(1-dt)
                    else:
                        self.collapse_time = t
                
                for child in self.children[::-1]:
                    child._event(self._canvas, 0, 0)
            else:
                self.x = self.base_x - self.width
                self.collapsed = True
            
            
            self.hovered = False
            editor._e_instance.check_hover(editor, (self.x, self.y, self.width, self.height), self)
        
        def _update(self, editor, X, Y):
            self.screen.fill(TEXT_BG2_COLOR)
            
            dw = min(0, self.x)
            
            if self.cell:
                editor.screen.fill(TEXT_COLOR, (self.x-dw, self.y-1, self.width+15+dw, self.height+1))
                editor.screen.fill(TEXT_BG2_COLOR, (self.x-dw, self.y, self.width+14+dw, self.height-1))
                if self.collapsed:
                    self.window_handles[0]._update(editor, self.x+self.width, self.y+((self.height/2)-15))
                else:
                    self.window_handles[1]._update(editor, self.x+self.width, self.y+((self.height/2)-15))
                
                self.cell._update(editor, X+self.x+10, Y+self.y+5)
                
                for child in self.children:
                    child._update(self._canvas, 0, 0)
                
            else:
                editor.screen.fill(TEXT_BG3_COLOR, (self.x-dw, self.y-1, self.width+15+dw, self.height+1))
                editor.screen.fill(TEXT_BG2_COLOR, (self.x-dw, self.y, self.width+14+dw, self.height-1))
                self.window_handles[2]._update(editor, self.x+self.width, self.y+((self.height/2)-15))
            
            
            editor.screen.blit(self.screen, (X+self.x, Y+self.y+30))
            
            

    def __init__(self, editor, aesa):
        self.editor = editor
        self.aesa = aesa
        
        self.ctx_tree: ContextTree = None
        self.transfer_slot = CellEditor.TransferSlot(self, 700, editor.height-65, 200, 24)
        
        self.storage = CellEditor.CellStorage(editor, self, 930, editor.height-36)
        
        self.config_pane1 = CellEditor.ConfigPane(editor, self, 102-400, 21, 400, 300)
        self.config_pane2 = CellEditor.ConfigPane(editor, self, 102-400, 0, 400, 300)
        self.config_pane3 = CellEditor.ConfigPane(editor, self, 102-400, 0, 400, 300)
        
    def get_pane1_open(self) -> bool:
        return self.config_pane1.cell is None

    def get_pane2_open(self) -> bool:
        return self.config_pane2.cell is None
    
    def close_pane1(self, editor):
        self.config_pane1.reset()
        self.ctx_tree.close()
    
    def close_pane2(self, editor):
        self.config_pane2.reset()
        self.ctx_tree.close()
    
    def get_open_in_pane1(self, cell):
        def func(_):
            self.open_in_pane1(cell)
        return func
    
    def get_open_in_pane2(self, cell):
        def func(_):
            self.open_in_pane2(cell)
        return func
    
    def open_in_pane1(self, cell):
        if self.ctx_tree:
            self.ctx_tree.close()
        self.config_pane1.cell = cell
        self.config_pane1.collapse_time = time.time()
        self.config_pane1.collapsed = False
        self.config_pane1.setup()
    
    def open_in_pane2(self, cell):
        if self.ctx_tree:
            self.ctx_tree.close()
        self.config_pane2.cell = cell
        self.config_pane2.collapse_time = time.time()
        self.config_pane2.collapsed = False
        self.config_pane2.setup()
    
    def _update_layout(self, editor):
        self.transfer_slot.y = editor.height-65
        self.storage.y = editor.height-36
        
        space = editor.height - 122
        self.config_pane1.height = self.config_pane2.height = self.config_pane3.height = space/3
        self.config_pane2.y = self.config_pane1.y + (space/3)
        self.config_pane3.y = self.config_pane2.y + (space/3)
    
    def _event(self, editor, X, Y):
        if editor._do_layout_update:
            self._update_layout(editor)
        
        self.transfer_slot._event(editor, X, Y)
        
        self.storage._event(editor, X, Y)
        
        self.config_pane3.cell = self.transfer_slot.cell
        
        self.config_pane1._event(editor, X, Y)
        self.config_pane2._event(editor, X, Y)
        self.config_pane3._event(editor, X, Y)
        
    def _update(self, editor, X, Y):
        
        if editor._e_instance.right_mouse_down():
            if editor._hovering and isinstance(editor._hovering, CellSlot):
                if editor._hovering.cell in [self.config_pane1.cell, self.config_pane2.cell]:
                    if editor._hovering.cell is self.config_pane1.cell:
                        fields = {
                            "  Stop Editing (Pane 1)": self.close_pane1
                        }
                    else:
                        fields = {
                            "  Stop Editing (Pane 2)": self.close_pane2
                        }

                    self.ctx_tree = ContextTree([fields], 200, 20, group="main-ctx", hover_color=TEXT_BG2_COLOR, click_color=TEXT_BG2_COLOR)
                    self.ctx_tree.openAtMouse(editor._e_instance)
                elif editor._hovering.cell is not self.transfer_slot.cell:
                    slot = editor._hovering
                    if slot.cell:
                        if self.get_pane1_open() or self.get_pane2_open():
                            fields = {
                                "  Edit in Pane 1": None,
                                "  Edit in Pane 2": None
                            }
                            if self.get_pane1_open():
                                fields.update({"  Edit in Pane 1": self.get_open_in_pane1(slot.cell)})
                            if self.get_pane2_open():
                                fields.update({"  Edit in Pane 2": self.get_open_in_pane2(slot.cell)})
                            self.ctx_tree = ContextTree([fields], 200, 20, group="main-ctx", hover_color=TEXT_BG2_COLOR, click_color=TEXT_BG2_COLOR)
                            self.ctx_tree.openAtMouse(editor._e_instance)
                
        
        self.transfer_slot._update(editor, X, Y)
        
        self.storage._update(editor, X, Y)
        
        self.config_pane1._update(editor, X, Y)
        self.config_pane2._update(editor, X, Y)
        self.config_pane3._update(editor, X, Y)


