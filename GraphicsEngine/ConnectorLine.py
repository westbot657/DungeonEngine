# pylint: disable=[W,R,C,import-error]

from UIElement import UIElement
from Pathfinding import Pathfinding
from Options import TEXT_COLOR

import pygame

from enum import Enum, auto

class ConnectorLine(UIElement):
    
    class Pathing(Enum):
        LINEAR = auto()
        ASTAR = auto()
        NONE = auto()
    
    def __init__(self, start:tuple[int, int], end:tuple[int, int], plane:Pathfinding.Plane, pathing:Pathing=Pathing.LINEAR, line_thickness=2, line_color=TEXT_COLOR):
        self.start = start
        self.end = end
        self.plane = plane
        self.pathing = pathing
        self.line_thickness = line_thickness
        self.line_color = line_color
        
        self.build_line()
        
    def build_line(self):
        self.path = None
        if self.pathing == ConnectorLine.Pathing.LINEAR:
            if raw_path := Pathfinding.astar_linear(self.plane, self.start, self.end):
                self.path = Pathfinding.vectorize(raw_path)
        elif self.pathing == ConnectorLine.Pathing.ASTAR:
            if raw_path := Pathfinding.astar(self.plane, self.start, self.end):
                self.path = Pathfinding.vectorize(raw_path)

        if self.path is None:
            self.path = {
                self.start,
                (self.end[0], self.start[1]),
                self.end
            }

    def _event(self, editor, X, Y):
        if self.path:
            ...
        
    def _update(self, editor, X, Y):
        
        if self.path:
            pygame.draw.lines(editor.screen, self.line_color, False, self.path, self.line_thickness)
            
        

