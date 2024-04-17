# pylint: disable=W,R,C,import-error

from UIElement import UIElement


class PanelPlacer(UIElement):
    def __init__(self, parent_shelf):
        self.parent_shelf = parent_shelf
        
        
    def _event(self, editor, X, Y):
        ...
    
    def _update(self, editor, X, Y):
        ...
