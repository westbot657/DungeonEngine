# pylint: disable=W,R,C, import-error

from UIElement import UIElement

import time


class Toasts(UIElement):
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.appearing = []
        self.toasts = []
        self.disappearing = []
        


    def toast(self, text:str, display_time:float=2):
        ...
    
    
    def _event(self, editor, X, Y):
        ...
    
    def _update(self, editor, X, Y):
        ...





