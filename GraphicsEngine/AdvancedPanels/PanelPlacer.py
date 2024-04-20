# pylint: disable=W,R,C,import-error

from RenderPrimitives import Image
from UIElement import UIElement
from Options import PATH


class PanelPlacer(UIElement):
    
    packaged_panel = (
        Image(f"{PATH}/advanced_editor/panel_crate.png", 0, 0, 33, 33),
        Image(f"{PATH}/advanced_editor/panel_crate_hovered.png", 0, 0, 33, 33),
        Image(f"{PATH}/advanced_editor/panel_crate_selected.png", 0, 0, 33, 33),
        Image(f"{PATH}/advanced_editor/panel_crate_selected_hovered.png", 0, 0, 33, 33)
    )
    
    def __init__(self, parent_shelf):
        self.parent_shelf = parent_shelf
        self.width = 33
        self.height = 33
        self.frame = 0
        self.hovered = False
        
    def _event(self, editor, X, Y):
        # print(f"event: {X}, {Y}")
        editor.check_hover(editor, (X, Y, self.width, self.height), self)
        
        if self.hovered:
            self.frame = 1
            if editor.left_mouse_down():
                self.frame = 2
                editor.holding = True
                editor.held = self
                self.parent_shelf.placer = None
                editor.hold_offset = (editor.mouse_pos[0]-X, editor.mouse_pos[1]-Y)
        else:
            self.frame = 0
            self.hovered = False
        
    
    def _update(self, editor, X, Y):
        PanelPlacer.packaged_panel[self.frame]._update(editor, X, Y)
