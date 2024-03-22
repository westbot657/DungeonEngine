# pylint: disable=[W,R,C, import-error]

from UIElement import UIElement
from AttributePanel import AttributePanel


class PanelTree(UIElement):
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tree = []
        
    def _event(self, editor, X, Y):
        y = 0
        
        for obj in self.tree:
            obj._event(editor, X+self.x+5, Y+self.y+y)
            y += obj.effective_height + 5
        
    
    def _update(self, editor, X, Y):
        y = 0
        
        for obj in self.tree:
            obj._update(editor, X+self.x+5, Y+self.y+y)
            y += obj.effective_height + 5
    

