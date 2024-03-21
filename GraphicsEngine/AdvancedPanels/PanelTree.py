# pylint: disable=[W,R,C, import-error]

from UIElement import UIElement
from AttributePanel import AttributePanel


class PanelTree(UIElement):
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def _event(self, editor, X, Y):
        ...
    
    def _update(self, editor, X, Y):
        ...
    

