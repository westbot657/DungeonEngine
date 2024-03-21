# pylint: disable=[W,R,C, no-member]

try:
    from GraphicsEngine.UIElement import UIElement
    from GraphicsEngine.Options import TEXT_BG_COLOR, TEXT_BG2_COLOR
except ImportError:
    from UIElement import UIElement
    from Options import TEXT_BG_COLOR, TEXT_BG2_COLOR

from typing import Any
import pygame


class ConstructionCanvas(UIElement):
    
    class _Canvas:
        def __init__(self, editor, canvas):
            super().__setattr__("_editor", editor)
            super().__setattr__("_canvas", canvas)
        
        def __getattribute__(self, __name: str) -> Any:
            if __name == "_editor":
                return super().__getattribute__("_editor")
            elif __name == "_canvas":
                return super().__getattribute__("_canvas")
            elif __name == "Width":
                #co = getattr(super().__getattribute__("_scrollable"), "offsetX")
                cx = getattr(super().__getattribute__("_canvas"), "x")# - getattr(super().__getattribute__("_scrollable"), "offsetX")
                cw = getattr(super().__getattribute__("_canvas"), "width")# - getattr(super().__getattribute__("_scrollable"), "offsetX")
                if hasattr(super().__getattribute__("_editor"), "x"):
                    fx = getattr(super().__getattribute__("_editor"), "x")
                else: fx = 0
                if hasattr(super().__getattribute__("_editor"), "get_width"):
                    fw = getattr(super().__getattribute__("_editor"), "get_width")()
                else: fw = getattr(super().__getattribute__("_editor"), "width")
                if fx + fw <= fx + cx + cw: return fw - cx
                return cw# - co
            elif __name == "Height":
                #co = getattr(super().__getattribute__("_scrollable"), "offsetY")
                cx = getattr(super().__getattribute__("_canvas"), "y")# - getattr(super().__getattribute__("_scrollable"), "offsetY")
                cw = getattr(super().__getattribute__("_canvas"), "height")# - getattr(super().__getattribute__("_scrollable"), "offsetY")
                if hasattr(super().__getattribute__("_editor"), "y"):
                    fx = getattr(super().__getattribute__("_editor"), "y")
                else: fx = 0
                if hasattr(super().__getattribute__("_editor"), "get_height"):
                    fw = getattr(super().__getattribute__("_editor"), "get_height")()
                else: fw = getattr(super().__getattribute__("_editor"), "height")
                if fx + fw <= fx + cx + cw: return fw - cx
                return cw# - co
            elif __name == "X":
                return max(0, getattr(super().__getattribute__("_canvas"), "x"))
            elif __name == "Y":
                return max(0, getattr(super().__getattribute__("_canvas"), "y"))
            elif hasattr(super().__getattribute__("_canvas"), __name):
                return getattr(super().__getattribute__("_canvas"), __name)
            elif hasattr(super().__getattribute__("_editor"), __name):
                return getattr(super().__getattribute__("_editor"), __name)
            else:
                raise AttributeError
        def __setattr__(self, __name: str, __value) -> None:
            if __name == "_editor":
                super().__setattr__("_editor", __value)
            elif hasattr(super().__getattribute__("_canvas"), __name):
                setattr(super().__getattribute__("_canvas"), __name, __value)
            elif hasattr(super().__getattribute__("_editor"), __name):
                setattr(super().__getattribute__("_editor"), __name, __value)
            else:
                setattr(super().__getattribute__("_canvas"), __name, __value)

    
    def __init__(self, advanced_editor, editor, x, y, width, height):
        self.advanced_editor = advanced_editor
        self.editor = editor
        self.canvas = ConstructionCanvas._Canvas(editor, self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.offsetX = 0
        self.offsetY = 0
        self.scale = 1.0
        self.grid_size = 100
        # self.sub_grid_segments = 2 # cut each section in half n times
        self.show_grid = True
        self.children = []
        self.panning = False
        self.pan_origin = [0, 0]
    
        # == scrollable canvas stuff ==
        self.mouse_pos = [0, 0]
        self.screen = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        
        # =============================
    
    
    def collides(self, mouse, rect) -> bool:
        mx, my = mouse
        x, y, w, h = rect
        #print("Scrollable: v")
        if self.canvas._editor.collides(self.editor.mouse_pos, (self.x, self.y, self.width, self.height)):
            #print(f"Scrollable: \033[38;2;20;200;20m{mouse} \033[38;2;200;200;20m{rect}\033[0m")
            if x <= (mx-self.offsetX) < x + w and y <= (my-self.offsetY) < y + h:
                return True

        return False
    
    def override_values(self):
        self.mouse_pos = list(self.editor.mouse_pos)
        self.mouse_pos[0] -= self.x - (self.offsetX * self.scale)
        self.mouse_pos[1] -= self.y - (self.offsetY * self.scale)
        self.mouse_pos[0] /= self.scale
        self.mouse_pos[1] /= self.scale
    
    def _event(self, editor, X, Y):
        mx, my = editor.mouse_pos
        self.override_values()
        
        for group, visible in [i for i in self.advanced_editor.visibility_toggled.items()][::-1]:
            if visible:
                for child in self.advanced_editor.visibility_groups[group][::-1]:
                    child._event(self.canvas, -self.offsetX, -self.offsetY)
        
        if editor.collides((mx, my), (self.x, self.y, self.width, self.height)):
            if editor.middle_mouse_down():
                self.pan_origin = [
                    (self.offsetX * self.scale) + mx,
                    (self.offsetY * self.scale) + my
                ]
                self.panning = True
            if editor.scroll != 0 and editor._hovering is None:
                _mx, _my = self.mouse_pos
                _scale = self.scale
                self.scale = min(max(0.5, self.scale + (editor.scroll * 0.125)), 3)
                # diff = self.scale - _scale
                
                pix_diff_w = (self.width / _scale) - (self.width / self.scale)
                side_ratio_x = ((mx - self.x)) / self.width
                self.offsetX += pix_diff_w * side_ratio_x
                
                
                pix_diff_h = (self.height / _scale) - (self.height / self.scale)
                side_ratio_y = ((my - self.y)) / self.height
                self.offsetY += pix_diff_h * side_ratio_y
                
                self.screen = pygame.Surface((self.width/self.scale, self.height/self.scale), pygame.SRCALPHA, 32)
        
        if editor.middle_mouse_up():
            self.panning = False
        
        if self.panning:
            dx, dy = self.pan_origin
            self.offsetX = (dx - mx) / self.scale
            self.offsetY = (dy - my) / self.scale
        
        

    def rebuild(self):
        self.screen = pygame.Surface((self.width/self.scale, self.height/self.scale), pygame.SRCALPHA, 32)

    def _update(self, editor, X, Y):
        self.screen.fill(TEXT_BG_COLOR)
        
        if self.show_grid:
            # draw grid
            _x = -1
            _y = -1
            _width = (self.width/self.scale) + (self.grid_size) # add one extra grid space off each side of the screen
            _height = (self.height/self.scale) + (self.grid_size)
            _ex = int(_width // (self.grid_size))
            _ey = int(_height // (self.grid_size))
            dx = self.offsetX % (self.grid_size)
            dy = self.offsetY % (self.grid_size)
            if _ex+_ey+2 < 40:
                for i in range(_x, _ex+1):
                    x = (i * self.grid_size) - dx
                    # self.screen.fill(TEXT_BG2_COLOR, (x-1, -1, 3, _height))
                    pygame.draw.line(self.screen, TEXT_BG2_COLOR, (x, -1), (x, _height), 3)
                for i in range(_y, _ey+1):
                    y = (i * self.grid_size) - dy
                    # self.screen.fill(TEXT_BG2_COLOR, (-1, y-1, _width, 3))
                    pygame.draw.line(self.screen, TEXT_BG2_COLOR, (-1, y), (_width, y), 3)
        
        viewport_rect = pygame.Rect(self.offsetX, self.offsetY, (self.width/self.scale), (self.height/self.scale))

        for group, visible in self.advanced_editor.visibility_toggled.items():
            if visible:
                for child in self.advanced_editor.visibility_groups[group]:
                    if viewport_rect.colliderect(child.get_collider()):
                        child._update(self.canvas, -self.offsetX, -self.offsetY)
        
        
        sx, sy = self.screen.get_size()
        editor.screen.blit(pygame.transform.scale(self.screen, (sx*self.scale, sy*self.scale)), (X+self.x, Y+self.y))

