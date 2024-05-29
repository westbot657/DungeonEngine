# pylint: disable=W,R,C,import-error

from UIElement import UIElement
from AdvancedPanels.PanelTextBox import PanelTextBox
from VisualLoader import VisualLoader, CellSlot, AttributeCell
from Options import PATH, TEXT_COLOR, TEXT_BG_COLOR, TEXT_BG2_COLOR, TEXT_BG3_COLOR
from ConstructionCanvas import ConstructionCanvas
from FunctionalElements import Button, BorderedButton
from ContextTree import ContextTree
from RenderPrimitives import Image

import pygame
import time

class CellEditor(UIElement):
    
    class TransferSlot(UIElement):
        def __init__(self, parent, x, y, width, height):
            self.parent = parent
            self.x = x
            self.y = y
            self.width = self._width = width
            self.height = self._height = height
            
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
                        "  list": self.new_list,
                    },
                    ContextTree.Line(),
                    {
                        "  f(x) -> int": self.new_f_int,
                        "  f(x) -> float": self.new_f_float,
                        # "  f(x) -> percent: self.new_f_percent"
                        "  f(x) -> str": self.new_f_str,
                        "  f(x) -> list": self.new_f_list,
                    }
                ], 200, 20, group="main-ctx", hover_color=TEXT_BG3_COLOR, click_color=TEXT_BG3_COLOR
            )
        
        def on_add_clicked(self, editor):
            self.ctx_tree.openAtMouse(editor._e_instance)
        
        def hist(self, cell, editor):
            def undo():
                self.cell = None
                cell.slot = None
            def redo():
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
        def new_list(self, editor):
            cell = AttributeCell(editor, [], "list", True)
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
        def new_f_list(self, editor):
            cell = AttributeCell(editor, {}, "list", True)
            self.cell = cell
            cell.slot = self
            self.ctx_tree.close()
            self.hist(cell, editor)
            
        def drop_acceptor(self, cell, editor):
            old_slot = cell.slot
            
            self.cell = cell
            cell.slot = self
            
            def undo():
                old_slot.cell = cell
                self.cell = None
                
            def redo():
                old_slot.cell = None
                self.cell = cell
                
            editor.add_history(redo, undo, "Moved Attribute")

        
        def _event(self, editor, X, Y):
            
            if self.cell:
                self.cell._event(editor, X+self.x, Y+self.y)
                self.width = self.cell.width
                self.height = self.cell.height
            else:
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

            if self.hovered and self.empty_mouse:
                editor.screen.fill((0, 120, 212), (X+self.x-1-dw, Y+self.y-1-dh, self.width+dw+2, self.height+dh+2))
            
            else:
                editor.screen.fill(TEXT_COLOR, (X+self.x-1-dw, Y+self.y-1-dh, self.width+dw+2, self.height+dh+2))
        
            if not self.cell:
                editor.screen.fill(TEXT_BG_COLOR, (X+self.x-dw2, Y+self.y-dh2, self.width+dw2, self.height+dh2))
                self.add_button._update(editor, X+self.x, Y+self.y)
            else:
                self.cell._update(editor, X+self.x, Y+self.y)
            
        
        
    
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
            
            self.children = []
            
            self.cell = None
            self.screen = pygame.Surface((self.width, self.height-1))
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
            self.mouse_pos[1] -= self.y + Y
            self.last_X = X
            self.last_Y = Y
            
        def _event(self, editor, X, Y):
            self.override_values(X, Y)
            if self.height != self._height:
                self.screen = pygame.Surface((self.width, self.height-1))
            
            if self.collapse_time:
                dt = (time.time() - self.collapse_time) * 3
                if dt >= 1:
                    self.collapse_time = 0
                    dt = 1
                
                if self.collapsed:
                    self.x = self.base_x - (self.width * dt)
                else:
                    self.x = self.base_x - (self.width - (self.width*dt))
            
            handle_collision = editor.collides(editor.mouse_pos, (self.x+self.width, self.y+((self.height/2)-15), 15, 30))
            
            
            
            if self.cell:
                if handle_collision and editor.left_mouse_down():
                    self.collapsed = not self.collapsed
                    t = time.time()
                    if (dt := t - self.collapse_time) < 1:
                        self.collapse_time = t-(1-dt)
                    else:
                        self.collapse_time = t
                
            else:
                self.x = self.base_x - self.width
                self.collapsed = True
            
            for child in self.children[::-1]:
                child._event(self._canvas, 0, 0)
            
            self.hovered = False
            editor._e_instance.check_hover(editor, (self.x, self.y, self.width, self.height), self)
        
        def _update(self, editor, X, Y):
            self.screen.fill(TEXT_BG2_COLOR)
            
            dw = min(0, self.x)
            
            if self.cell:
                editor.screen.fill(TEXT_COLOR, (self.x-dw, self.y-1, self.width+15+dw, self.height+1))
                editor.screen.fill(TEXT_BG2_COLOR, (self.x+self.width, self.y, 14, self.height-1))
                if self.collapsed:
                    self.window_handles[0]._update(editor, self.x+self.width, self.y+((self.height/2)-15))
                else:
                    self.window_handles[1]._update(editor, self.x+self.width, self.y+((self.height/2)-15))
                    
            else:
                editor.screen.fill(TEXT_BG3_COLOR, (self.x-dw, self.y-1, self.width+15+dw, self.height+1))
                editor.screen.fill(TEXT_BG2_COLOR, (self.x+self.width, self.y, 14, self.height-1))
                self.window_handles[2]._update(editor, self.x+self.width, self.y+((self.height/2)-15))
            
            for child in self.children:
                child._update(self._canvas, 0, 0)
            
            editor.screen.blit(self.screen, (X+self.x, Y+self.y))

    def __init__(self, editor, aesa):
        self.editor = editor
        self.aesa = aesa
        
        self.transfer_slot = CellEditor.TransferSlot(self, 700, editor.height-65, 200, 24)
        
        self.config_pane1 = CellEditor.ConfigPane(editor, self, 102-400, 0, 400, 300)
        self.config_pane2 = CellEditor.ConfigPane(editor, self, 102-400, 0, 400, 300)
        self.config_pane3 = CellEditor.ConfigPane(editor, self, 102-400, 0, 400, 300)
        
    def get_pane1_open(self) -> bool:
        return self.config_pane1.cell is None

    def get_pane2_open(self) -> bool:
        return self.config_pane2.cell is None
    
    def get_open_in_pane1(self, cell):
        def func(_):
            self.open_in_pane1(cell)
        return func
    
    def get_open_in_pane2(self, cell):
        def func(_):
            self.open_in_pane2(cell)
        return func
    
    def open_in_pane1(self, cell):
        self.config_pane1.cell = cell
        self.config_pane1.collapse_time = time.time()
        self.config_pane1.collapsed = False
    
    def open_in_pane2(self, cell):
        self.config_pane2.cell = cell
        self.config_pane2.collapse_time = time.time()
        self.config_pane2.collapsed = False
    
    def _update_layout(self, editor):
        self.transfer_slot.y = editor.height-65
        
        space = editor.height - 122
        self.config_pane1.height = self.config_pane2.height = self.config_pane3.height = space/3
        self.config_pane2.y = self.config_pane1.y + (space/3)
        self.config_pane3.y = self.config_pane2.y + (space/3)
    
    def _event(self, editor, X, Y):
        if editor._do_layout_update:
            self._update_layout(editor)
        
        self.transfer_slot._event(editor, X, Y)
        
        self.config_pane3.cell = self.transfer_slot.cell
        
        self.config_pane1._event(editor, X, Y)
        self.config_pane2._event(editor, X, Y)
        self.config_pane3._event(editor, X, Y)
        
    def _update(self, editor, X, Y):
        
        if editor._e_instance.right_mouse_down():
            if editor._hovering and isinstance(editor._hovering, CellSlot) and editor._hovering.cell not in [self.transfer_slot.cell, self.config_pane1.cell, self.config_pane2.cell, self.config_pane3.cell]:
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
                        ContextTree([fields], 200, 20, group="main-ctx", hover_color=TEXT_BG2_COLOR, click_color=TEXT_BG2_COLOR).openAtMouse(editor._e_instance)
        
        self.transfer_slot._update(editor, X, Y)
        
        self.config_pane1._update(editor, X, Y)
        self.config_pane2._update(editor, X, Y)
        self.config_pane3._update(editor, X, Y)


