# pylint: disable=W,R,C,import-error

from UIElement import UIElement
from AdvancedPanels.PanelTextBox import PanelTextBox
from VisualLoader import VisualLoader, CellSlot, AttributeCell
from Options import TEXT_COLOR, TEXT_BG_COLOR, TEXT_BG2_COLOR, TEXT_BG3_COLOR

class CellEditor(UIElement):
    
    class TransferSlot(UIElement):
        def __init__(self, parent, x, y, width, height):
            self.parent = parent
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            
            self.cell = None
            self.hovered = False
            
    
    
    class ConfigPane(UIElement):
        def __init__(self, parent, x:int, y:int, width:int, height:int):
            self.parent = parent
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.collapsed = True
            self.collapse_time = 0

    def __init__(self, editor, aesa):
        self.editor = editor
        self.aesa = aesa
        self.x = 102
        self.y = 21
        
        self.transfer_slot = CellEditor.TransferSlot(self, 0, 0, 200, 24)
        
        self.config_pane1 = CellEditor.ConfigPane(self, 0, 0, 300, 300)
        self.config_pane2 = CellEditor.ConfigPane(self, 0, 0, 300, 300)
        # self.config_pane3 = CellEditor.ConfigPane(self, 0, 0, 300, 300)
        
        
        
    
    def _event(self, editor, X, Y):
        ...
    
    def _update(self, editor, X, Y):
        ...


