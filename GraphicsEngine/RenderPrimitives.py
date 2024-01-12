# pylint: disable=W,R,C

from UIElement import UIElement

import pygame
import time

class Color(list):
    __slots__ = ["r", "g", "b", "a"]
    def __init__(self, r, g, b, a=None):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
    def with_alpha(self):
        if self.a:
            return Color(self.r, self.g, self.b, self.a)
        else:
            return Color(self.r, self.g, self.b, 255)
    def without_alpha(self):
        return Color(self.r, self.g, self.b)
    
    def __list__(self) -> list:
        if self.a:
            return [self.r, self.g, self.b, self.a]
        else:
            return [self.r, self.g, self.b]
    
    def __tuple__(self) -> tuple:
        if self.a:
            return (self.r, self.g, self.b, self.a)
        else:
            return (self.r, self.g, self.b)
    def __iter__(self):
        if self.a:
            return iter((self.r, self.g, self.b, self.a))
        else:
            return iter((self.r, self.g, self.b))
    def __len__(self):
        if self.a: return 4
        else: return 3
    @classmethod
    def color(cls, obj, allow_none=True, allow_image=True):
        if obj is None and allow_none:
            return None
        elif obj is None:
            raise ValueError("Color cannot be None")
        if isinstance(obj, (Image, Animation)) and allow_image:
            return obj
        elif isinstance(obj, (Image, Animation)):
            raise Exception(f"Color cannot be an image/animation")
        if isinstance(obj, Color):
            return obj
        elif isinstance(obj, (list, tuple)) and len(obj) in (3, 4):
            return cls(*obj)
        elif isinstance(obj, int):
            b = obj % 256
            obj = obj // 256
            g = obj % 256
            obj = obj // 256
            r = obj % 256
            obj = obj // 256
            a = obj % 256
            return cls(r, g, b, a)
        else:
            raise ValueError(f"Invalid Color! ({obj})")



class Image(UIElement):
    
    __slots__ = [
        "surface", "_surface",
        "x", "y", "width", "height",
        "file_location", "_width", "_height"
    ]
    
    def __init__(self, file_location:str, x:int=0, y:int=0, width:int|None=None, height:int|None=None):
        self.surface = self._surface = pygame.image.load(file_location)
        self.x = self._x = x
        self.y = self._y = y
        self.width = self._width = width
        self.height = self._height = height
        self.file_location = file_location
        if width and (not height):
            w, h = self.surface.get_size()
            d = w/width
            self.height = self._height = h * d
            self.surface = pygame.transform.scale(self._surface, (width, h*d))
        elif height and (not width):
            w, h = self.surface.get_size()
            d = h/height
            self.width = self._width = w * d
            self.surface = pygame.transform.scale(self._surface, (w*d, height))
        elif width and height:
            self.surface = pygame.transform.scale(self._surface, (width, height))
        else:
            self.width, self.height = self._width, self._height = self.surface.get_size()

    def copy(self):
        i = Image(self.file_location)
        i.surface = i._surface = self.surface.copy()
        i.width = i._width = self.width
        i.height = i._height = self.height
        return i

    def section(self, x:int, y:int, w:int, h:int):
        i = Image(self.file_location)
        i.surface = i._surface = self._surface.subsurface((x, y, w, h))
        i.width = i._width = w
        i.height = i._height = h
        return i

    def partial_update(self):
        if self.width != self._width or self.height != self._height:
            self._width = self.width
            self._height = self.height
            self.surface = pygame.transform.scale(self._surface, (self.width, self.height))

    def resize(self, width:int, height:int):
        self.width = width
        self.height = height
        self.partial_update()
        return self

    def scale(self, amnt:float):
        
        self.width *= amnt
        self.height *= amnt
        self._width = self.width
        self._height = self.height
        self.surface = pygame.transform.scale(self._surface, (self.width, self.height))
        return self

    def _event(self, *_):
        self.partial_update()

    def _update(self, editor, X, Y):
        #self.partial_update()
        editor.screen.blit(self.surface, (X+self.x, Y+self.y))

from Options import PATH

class Animation(UIElement):
    
    __slots__ = [
        "x", "y", "sprite_sheet", "sprite_width",
        "sprite_height", "source", "offsetX", "offsetY",
        "_sheet", "_rX", "_rY", "_frames" "frames", "surface",
        "order", "loop", "fps", "s", "hovered", "_hovered",
        "current_frame", "t"
    ]
    
    def __init__(self, x:int, y:int, **options):
        """
        # options:\n

        ## animation source:\n
        ### Sprite sheet:\n
        Parameters:\n
        ----------\n
        `sprite_sheet`: str\n
            location of a sprite sheet\n
        `sprite_width`: int\n
            width of a grid-space on the sprite sheet\n
        `sprite_height`: int\n
            height of a grid-space on the sprite sheet\n
        `offset`: tuple[int, int] = (0, 0)\n
            start frame offset location from top left corner\n
        `resize`: tuple[int, int]\n
            size to resize frames to after taking them from the spritesheet\n
        frames are generated in order of left to right and then top to bottom\n
        OR\n
        ### Multiple Images\n
        Parameters:\n
        ----------\n
        `frames`: list[str, ...]\n
            list of paths for each frame in a sprite sheet\n
        OR\n
        ### Custom frames\n
        Paramaters:\n
        ----------\n
        `custom`: list[pygame.Surface]\n

        Parameters:\n
        ----------\n
        `order`: list[int, ...]\n
            the order in which to play frames\n
            if not given, frames are played in order on loop\n
        `fps`: float\n
            how many frames to play per second\n
        `loop`: bool = True\n
            whether to loop the animation or not\n

        Attributes:\n
        ----------\n
        `source`: str|list[str, ...]\n
            the image file location(s)\n
        `current_frame`: int\n
        `x`: int\n
        `y`: int\n
        
        """
        self.x = x
        self.y = y
        if "sprite_sheet" in options:
            self.sprite_sheet = self.source = options.get("sprite_sheet")
            self.sprite_width = options.get("sprite_width", None)
            self.sprite_height = options.get("sprite_height", None)
            
            self.offsetX, self.offsetY = options.get("offset", (0, 0))

            self._sheet = pygame.image.load(self.sprite_sheet)

            w, h = self._sheet.get_size()

            if self.sprite_width is None:
                self.sprite_width = w - self.offsetX

            if self.sprite_height is None:
                self.sprite_height = h - self.offsetY

            assert 0 < self.offsetX + self.sprite_width <= w, "width must be between 1 and the width of the sprite sheet"
            assert 0 < self.offsetY + self.sprite_height <= h, "height must be between 1 and the height of the sprite sheet"

            self._rX, self._rY = options.get("resize", (self.sprite_width, self.sprite_height))

            cols = w // self.sprite_width
            rows = h // self.sprite_height

            y = self.offsetY
            self._frames = []
            for _y in range(rows):
                if y + self.sprite_height > h: continue
                x = self.offsetX
                for _x in range(cols):
                    if x + self.sprite_width > w: continue
                    
                    self._frames.append(pygame.transform.scale(self._sheet.subsurface((x, y, self.sprite_width, self.sprite_height)), (self._rX, self._rY)))
                    #self._frames.append(pygame.transform.chop(self._sheet, (x, y, self.sprite_width, self.sprite_height)))
                    x += self.sprite_width
                y += self.sprite_height

        elif "frames" in options:
            self.frames = self.source = options.get("frames")

            self._frames = []
            err = None
            self.sprite_width = 0
            self.sprite_height = 0
            for src in self.frames:
                try:
                    
                    self._frames.append(pygame.image.load(src))
                    self.sprite_width, self.sprite_height = self._frames[0].get_size()
                except Exception:
                    err = src
                    break

            if err:
                raise ValueError(f"File not found: {err}")

        elif "custom" in options:
            self._frames = options.get("custom")
            self.sprite_width, self.sprite_height = self._frames[0].get_size()
            self.source = f"{PATH}/highlight.png"
            self.surface = self._frames[0]

        else:
            raise Exception("Animation is missing either 'sprite_sheet' or 'frames'")

        self.order = options.get("order", [*range(len(self._frames))])
        self.loop = options.get("loop", True)
        self.fps = options.get("fps", 1)
        self.s = 0
        self.hovered = False
        self._hovered = False

        self.current_frame = 0
        self.t = None

    def copy(self):
        a = Animation(self.x, self.y, custom=self._frames, order=self.order, loop=self.loop, fps=self.fps)
        a.current_frame = self.current_frame
        a.partial_update()
        return a
    
    def section(self, x:int, y:int, w:int, h:int):
        frames = []
        for f in self._frames:
            frames.append(f.subsurface((x, y, w, h)))
        a = Animation(self.x, self.y, custom=frames, order=self.order, loop=self.loop, fps=self.fps)
        a.current_frame = self.current_frame
        a.partial_update()
        return a

    def resize(self, width:int, height:int):
        frames = self._frames.copy()
        self._frames.clear()
        self.sprite_width, self.sprite_height = width, height
        for f in frames:
            self._frames.append(pygame.transform.scale(f, (width, height)))
        self.partial_update()
        return self

    def scale(self, amnt:float):
        frames = self._frames.copy()
        self._frames.clear()
        for f in frames:
            w, h = f.get_size()
            w *= amnt
            h *= amnt
            self.sprite_width, self.sprite_height = w, h
            self._frames.append(pygame.transform.scale(f, (w, h)))
        return self

    def _on_end(self):
        return self.on_end()

    def on_end(self):
        ...

    def _on_hover(self, editor):
        return self.on_hover(editor)
    
    def on_hover(self, editor):
        ...
    
    def _off_hover(self, editor):
        return self.off_hover(editor)
    
    def off_hover(self, editor):
        ...

    def partial_update(self, *_, **__):
        self.surface = self._frames[self.order[self.current_frame]]

    def _event(self, editor, X, Y):
        if self.fps > 0:
            if self.t is None:
                self.t = time.time()
            t = time.time()

            if t - self.t > 1/self.fps:
                self.t += 1/self.fps
                self.current_frame += 1
                if self.current_frame >= len(self.order):
                    if self.loop:
                        self.current_frame = 0
                    else:
                        self._on_end()

        self._hovered = self.hovered
        if editor.collides((editor.mouse_pos), (X+self.x, Y+self.y, self.sprite_width, self.sprite_height)):
            if editor._hovering is not None:
                editor._hovering = self
                self.hovered = editor._hovered = True
                if not self._hovered:
                    self._on_hover(editor)
        
        else:
            self.hovered = False
            if self._hovered:
                self._off_hover(editor)

    def _update(self, editor, X, Y):
        f = self._frames[self.order[self.current_frame]]
        editor.screen.blit(f, (X+self.x, Y+self.y))

    def __getitem__(self, item) -> Image:
        i = Image(self.source if isinstance(self.source, str) else self.source[0])
        i._surface = i.surface = self._frames[item]
        i.partial_update()
        return i

