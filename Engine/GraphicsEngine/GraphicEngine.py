# pylint: disable=[W,R,C,import-error,no-member]

try:
    from .GraphicElement import GraphicElement
    from .Keyboard import KeyBoard
    from .Mouse import Mouse
except ImportError:
    from GraphicElement import GraphicElement
    from Keyboard import KeyBoard
    from Mouse import Mouse

import pygame




class GraphicEngine(GraphicElement):

    def __init__(self):
        
        self.mouse = Mouse()
        self.keyboard = KeyBoard()
        self.children = []
        self.parent = self

    def update(self):
        ...






