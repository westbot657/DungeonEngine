# pylint: disable=W,R,C,import-error

from UIElement import UIElement


class PanelPlacer(UIElement):
    def __init__(self, parent_shelf):
        self.parent_shelf = parent_shelf
        self.width = 33
        self.height = 33
        
    def _event(self, editor, X, Y):
        editor.check_hover(editor, (X, Y, self.width, self.height), self)
        
        if self.hovered:
            if editor.left_mouse_down():
                editor.holding = True
                editor.held = self
                self.parent_shelf.placer = None
                editor.hold_offset = (editor.mouse_pos[0]-X, editor.mouse_pos[1]-Y)
        
    
    def _update(self, editor, X, Y):
        ...
