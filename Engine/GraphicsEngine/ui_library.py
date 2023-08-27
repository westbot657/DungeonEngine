# pylint: disable=[W,R,C,import-error,no-member]
import pygame
#import PIL
import time
import pyperclip
import re
import os
import sys
import mouse
#from io import BytesIO
from enum import Enum, auto
from ctypes import windll

from win32api import GetMonitorInfo, MonitorFromPoint
from pygame._sdl2.video import Window



class Color(list):
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

PATH = "./Engine/GraphicsEngine/resources"

FONT = f"{PATH}/JetBrainsMono-Regular.ttf"
TEXT_SIZE = 14
TEXT_COLOR = Color(190, 190, 190)
TEXT_BG_COLOR = Color(31, 31, 31)
TEXT_HIGHLIGHT = Color(0, 122, 204, 127)
TAB_SIZE = 4
CURSOR_BLINK_TIME = 50
CURSOR_COLOR = Color(190, 190, 190)
SCROLL_MULTIPLIER = int(TEXT_SIZE*3)

pygame.init() # pylint: disable=no-member
pygame.font.init()


def expand_text_lists(ls):
    out = []
    
    for l in ls:
        _out = []
        for t in l:
            _out += [a for a in re.split(r"", t) if a]
        out.append(_out)
    return out

class UIElement:
    def _event(self, editor, X, Y):
        raise NotImplementedError(f"Please implement '_event' for {self}")
    def _update(self, editor, X, Y):
        raise NotImplementedError(f"Please implement '_update' for {self}")

class EditorMimic:
    def __init__(self, editor, overrider):
        super().__setattr__("_EditorMimic__editor", editor)
        super().__setattr__("_EditorMimic__overrider", overrider)
    def __getattribute__(self, __name: str):
        editor = super().__getattribute__("_EditorMimic__editor")
        overrider = super().__getattribute__("_EditorMimic__overrider")
        if hasattr(overrider, __name):
            return getattr(overrider, __name)
        elif hasattr(editor, __name):
            return getattr(editor, __name)
        else:
            raise AttributeError(f"'EditorMimic' object has no attribute '{__name}'")
    def __setattr__(self, __name: str, __value) -> None:
        if __name == "_editor":
            return super().__setattr__("_EditorMimic__editor", __value)
        editor = super().__getattribute__("_EditorMimic__editor")
        overrider = super().__getattribute__("_EditorMimic__overrider")
        if hasattr(overrider, __name):
            setattr(overrider, __name, __value)
        elif hasattr(editor, __name):
            setattr(editor, __name, __value)
        else:
            setattr(overrider, __name, __value)

class Text(UIElement):
    def __init__(self, x:int, y:int, min_width:int=1, content:str="", text_color:Color|tuple|int=TEXT_COLOR, text_bg_color:Color|tuple|int=TEXT_BG_COLOR, text_size:int=TEXT_SIZE):
        assert min_width >= 1, "Min width must be 1 or more"
        self.x = x
        self.y = y
        self.content = self._content = content
        self.min_width = min_width
        self.text_color = Color.color(text_color)
        self.text_bg_color = Color.color(text_bg_color)
        self.text_size = text_size
        self.font = pygame.font.Font(FONT, text_size)
        self.surface = self.font.render(self.content, True, tuple(self.text_color))
        self.width = self.surface.get_width()

    def _event(self, *_):
        if self.content != self._content:
            self._content = self.content
            self.surface = self.font.render(self.content, True, tuple(self.text_color))
            self.width = self.surface.get_width()
        
    def _update(self, editor, X, Y):
        _x, _y = self.surface.get_size()
        if self.text_bg_color:
            editor.screen.fill(self.text_bg_color, (X+self.x-1, Y+self.y-1, max(_x, self.min_width)+2, _y+2))
        editor.screen.blit(self.surface, (X+self.x, Y+self.y))

class Image(UIElement):
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

class Animation(UIElement):
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

class MultilineText(UIElement):
    def __init__(self, x:int, y:int, min_width:int=1, min_height:int=1, content:str="", text_color:Color|tuple|int=TEXT_COLOR, text_bg_color:Color|tuple|int=TEXT_BG_COLOR):
        assert min_width >= 1, "Min width must be 1 or more"
        assert min_height >= 1, "Min height must be 1 or more"
        self.x = x
        self.y = y
        self.min_width = min_width
        self.min_height = min_height
        self.content = content
        self.text_color = Color.color(text_color)
        self.text_bg_color = Color.color(text_bg_color)
        self.font = pygame.font.Font(FONT, TEXT_SIZE)
        self.surfaces = []
        for line in content.split("\n"):
            s = self.font.render(line, True, tuple(self.text_color))
            
            self.surfaces.append(s)

    def set_content(self, content:str=""):
        self.content = content
        self.surfaces.clear()
        for line in content.split("\n"):
            s = self.font.render(line, True, tuple(self.text_color))
            self.surfaces.append(s)

    def _event(self, *_):
        pass

    def _update(self, editor, X, Y):
        y = self.y
        w = self.min_width
        h = 0
        for s in self.surfaces:
            s:pygame.Surface
            w = max(w, s.get_width())
            h += s.get_height()
        h = max(self.min_height, h)

        if self.text_bg_color:
            editor.screen.fill(tuple(self.text_bg_color), (X+self.x-1, Y+self.y-1, w+2, h+2))

        h = 0
        for s in self.surfaces:
            editor.screen.blit(s, (X+self.x, Y+self.y+h))
            h += s.get_height()

class TextBox(UIElement):
    def __init__(self, x:int, y:int, min_width:int=1, content:str="", text_color:Color|tuple|int=TEXT_COLOR, text_bg_color:Color|tuple|int=TEXT_BG_COLOR, text_size:int=TEXT_SIZE):
        self.x = x
        self.y = y
        assert min_width >= 1, "Min width must be 1 or more"
        self.min_width = min_width
        #self.content = content
        self.text_color = Color.color(text_color)
        self.text_bg_color = Color.color(text_bg_color)
        self.text_size = text_size
        self.font = pygame.font.Font(FONT, text_size)
        self.surface = self.font.render(content, True, tuple(self.text_color))
        self.focused = False
        self.hovered = False
        self._letters = [l for l in content]
        self.cursor_location = 0
        self._cursor_surface = pygame.Surface((1, text_size))
        self._cursor_tick = 0
        self._blink = CURSOR_BLINK_TIME
        self._cursor_visible = False
        self._text_selection_end = None
        self._text_selection_start = None
        self._highlight = pygame.image.load(f"{PATH}/highlight.png")#pygame.Surface((1, self.text_size), pygame.SRCALPHA, 32) # pylint: disable=no-member
        #self._highlight.fill(TEXT_HIGHLIGHT)
        self.highlight = self._highlight.copy()

    def get_selection(self):
        if self._text_selection_start and self._text_selection_end:
            a = min(self._text_selection_start, self._text_selection_end)
            b = max(self._text_selection_start, self._text_selection_end)
            return self.get_content()[a:b]
        return None

    def set_selection(self, text:str):
        if self._text_selection_start and self._text_selection_end:
            a = min(self._text_selection_start, self._text_selection_end)
            b = max(self._text_selection_start, self._text_selection_end)
            content = self.get_content()
            pre = content[0:a]
            post = content[b-1:]
            self.set_content(pre + text + post)
            self._text_selection_start = self._text_selection_end = None

    def get_content(self):
        return "".join(self._letters)

    def set_content(self, content:str=""):
        self._letters = [l for l in content]
        #self.surface = self.font.render(content, True, self.text_color)
        self.cursor_location = min(self.cursor_location, len(self._letters))

    def refresh_highlight(self):
        if self._text_selection_start and self._text_selection_end:
            a = min(self._text_selection_start, self._text_selection_end)
            b = max(self._text_selection_start, self._text_selection_end)
            letter = self.font.render("T", True, (0, 0, 0))
            w = letter.get_width()
            width = (b - a) * w
            self.highlight = pygame.transform.scale(self._highlight, (width, self.text_size))

    def _event(self, editor, X, Y):
        w, h = self.surface.get_size()
        _x, _y = editor.mouse_pos

        #if max(editor.X, X + self.x) <= _x <= min(X + self.x + w, editor.Width) and max(editor.Y, Y + self.y) <= _y <= min(Y + self.y + h, editor.Height):
        if editor.collides((_x, _y), (X+self.x, Y+self.y, w, h)):
            self.hovered = editor._hovered = True
        else:
            self.hovered = False

        if editor.left_mouse_down():
            if self.hovered:
                letter = self.font.render("T", True, (0, 0, 0))
                w = letter.get_width()# - 1
                dx = _x - (X + self.x)

                self.cursor_location = min(int(round(dx/w)), len(self._letters))
                
                if pygame.K_LSHIFT in editor.keys and self._text_selection_start:
                    self._text_selection_end = self.cursor_location
                else:
                    self._text_selection_start = self.cursor_location
                    self._text_selection_end = None

                self.focused = True
                self._cursor_visible = True
                self._cursor_tick = 0
                
            else:
                self.focused = False
                self._cursor_visible = False

        if self.focused:
            for key in editor.new_keys:
                if pygame.K_LCTRL in editor.keys and key == pygame.K_c:
                    if self._text_selection_start and self._text_selection_end:
                        pyperclip.copy(self.get_selection())
                elif pygame.K_LCTRL in editor.keys and key == pygame.K_x:
                    if self._text_selection_start and self._text_selection_end:
                        pyperclip.copy(self.get_selection())
                        self.set_selection("")
                elif pygame.K_LCTRL in editor.keys and key == pygame.K_v:
                    if self._text_selection_start and self._text_selection_end:
                        self.set_selection(pyperclip.paste())
                    else:
                        self._text_selection_start = self._text_selection_end = self.cursor_location.copy()
                        self.set_selection(pyperclip.paste())
                elif key in [
                        pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_LCTRL, pygame.K_RCTRL,
                        pygame.K_CAPSLOCK, pygame.K_LALT,
                        pygame.K_RALT
                    ]: ...
                elif key in (pygame.K_TAB, "\t"):
                    tabs_to_add = TAB_SIZE - (self.cursor_location % TAB_SIZE)
                    self.set_selection("")
                    for i in range(tabs_to_add):
                        self._letters.insert(self.cursor_location, " ")
                        self.cursor_location += 1
                elif key == pygame.K_UP:
                    self.cursor_location = 0
                    if pygame.K_LSHIFT in editor.keys and self._text_selection_start:
                        self._text_selection_end = self.cursor_location
                        self.refresh_highlight()
                    elif not self._text_selection_start:
                        self._text_selection_start = self.cursor_location
                    else:
                        self._text_selection_start = self._text_selection_end = None
                elif key == pygame.K_LEFT:
                    self.cursor_location = max(self.cursor_location - 1, 0)
                    if pygame.K_LSHIFT in editor.keys and self._text_selection_start:
                        self._text_selection_end = self.cursor_location
                        self.refresh_highlight()
                    elif not self._text_selection_start:
                        self._text_selection_start = self.cursor_location
                    else:
                        self._text_selection_start = self._text_selection_end = None
                elif key == pygame.K_RIGHT:
                    self.cursor_location = min(self.cursor_location + 1, len(self._letters))
                    if pygame.K_LSHIFT in editor.keys and self._text_selection_start:
                        self._text_selection_end = self.cursor_location
                        self.refresh_highlight()
                    elif not self._text_selection_start:
                        self._text_selection_start = self.cursor_location
                    else:
                        self._text_selection_start = self._text_selection_end = None
                elif key == pygame.K_DOWN:
                    self.cursor_location = len(self._letters)
                    if pygame.K_LSHIFT in editor.keys and self._text_selection_start:
                        self._text_selection_end = self.cursor_location
                        self.refresh_highlight()
                    elif not self._text_selection_start:
                        self._text_selection_start = self.cursor_location
                    else:
                        self._text_selection_start = self._text_selection_end = None
                elif key in ["\b", pygame.K_BACKSPACE]:
                    if self._text_selection_start and self._text_selection_end:
                        self.set_selection("")
                        self._text_selection_start = self._text_selection_end = None
                    elif 0 < self.cursor_location <= len(self._letters):
                        self.cursor_location -= 1
                        self._letters.pop(self.cursor_location)
                elif key in (pygame.K_DELETE, pygame.KSCAN_DELETE):
                    if self._text_selection_start and self._text_selection_end:
                        self.set_selection("")
                        self._text_selection_start = self._text_selection_end = None
                    elif 0 <= self.cursor_location < len(self._letters):
                        self._letters.pop(self.cursor_location)
                elif key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_KP_ENTER, "\n", "\r"):
                    self.focused = False
                    self._cursor_visible = False
                    self.on_enter(self.get_content())
                    break
                else:
                    self._letters.insert(self.cursor_location, key)
                    self.cursor_location += 1
                #print(self.get_content())

            self._cursor_tick += 1
            if self._cursor_tick >= self._blink:
                self._cursor_tick = 0
                self._cursor_visible = not self._cursor_visible

            self.surface = self.font.render(self.get_content(), True, tuple(self.text_color))

    def _update(self, editor, X, Y):
        _x, _y = self.surface.get_size()
        if self.text_bg_color:
            if isinstance(self.text_bg_color, (Image, Animation)):
                self.text_bg_color.resize(_x+2, _y+2)._update(editor, X+self.x-1, Y+self.y-1)
            else:
                editor.screen.fill(self.text_bg_color, (X+self.x-1, Y+self.y-1, _x+2, _y+2))
        editor.screen.blit(self.surface, (X+self.x, Y+self.y))

        if self._cursor_visible:
            h = self.font.render(self.get_content()[0:self.cursor_location], True, (0, 0, 0)) # This is not shown on screen, only used to get width
            editor.screen.blit(self._cursor_surface, (X+self.x+h.get_width(), Y+self.y+2))

    def on_enter(self, text:str): ... # pylint: disable=unused-argument

class Selection:
    def __init__(self, text:str, start:int, end:int):
        self.text = text
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Selection [{self.start}:{self.end}]: '{self.text}'"

class Cursor:
    
    __slots__ = [
        "line",
        "col"
    ]
    
    def __init__(self, line, col):
        self.line = line
        self.col = col
    def copy(self):
        return Cursor(self.line, self.col)

    def __bool__(self):
        return True

    def __lt__(self, other):
        if isinstance(other, Cursor):
            if self.line == other.line: return self.col < other.col
            return self.line < other.line

    def __le__(self, other):
        if isinstance(other, Cursor):
            if self.line == other.line: return self.col <= other.col
            return self.line < other.line

    def __gt__(self, other):
        if isinstance(other, Cursor):
            if self.line == other.line: return self.col > other.col
            return self.line > other.line
    
    def __ge__(self, other):
        if isinstance(other, Cursor):
            if self.line == other.line: return self.col >= other.col
            return self.line > other.line

    def __eq__(self, other):
        if isinstance(other, Cursor):
            if self is other: return True
            return self.line == other.line and self.col == other.col

    def __repr__(self):
        return f"Cursor({self.line}, {self.col})"

class MultilineTextBox(UIElement):
    def __init__(self, x:int, y:int, min_width:int=1, min_height:int=1, content:str="", text_color:Color|tuple|int=TEXT_COLOR, text_bg_color:Color|Image|tuple|int=TEXT_BG_COLOR, text_size:int=TEXT_SIZE, cursor_color:Color|tuple|int=CURSOR_COLOR, single_line:bool=False):
        self.x = x
        self.y = y
        self.min_width = min_width
        self.min_height = min_height
        self._text_width = 0
        self._text_height = 0
        self.single_line = single_line
        self._lines = [[*line] for line in content.split("\n")]
        self.text_color = Color.color(text_color)
        self.text_bg_color = Color.color(text_bg_color)
        self.text_size = text_size
        self.font = pygame.font.Font(FONT, text_size)
        self.cursor_location = Cursor(0, 0)
        self._blink = CURSOR_BLINK_TIME
        self._cursor_tick = 0
        self._cursor_visible = False
        self._cursor_color = Color.color(cursor_color)
        self._cursor_surface = pygame.Surface((1, text_size))
        self._cursor_surface.fill(tuple(self._cursor_color))
        self.surfaces = []
        self.focused = False
        self.hovered = False
        self._text_selection_start = None
        self._text_selection_end = None
        self._highlight_offset = [0, 0]
        self._highlight = pygame.image.load(f"{PATH}/highlight.png")#pygame.Surface((1, 1), pygame.SRCALPHA, 32) # pylint: disable=no-member
        self.highlights = []
        self._save = self._default_save_event
        self.set_content(content)

    def on_save(self, function):
        """Decorator for a function
        
        This function is called whenever the text box detects the CTRL+S keybind
        
        passes:
            text_box (MultilineTextBox): The box that CTRL+S came from
            content (str): the entire text content of the text box
            selection (Selection | None): a Selection object containing the text box's selected text, and it's start and end text indices
            cursorPos (Cursor): the text box's current cursor position
        """
        self._save = function
        return function

    def _default_save_event(self, _, content:str, selection:Selection|None, cursorPos:Cursor):
        pass

    def refresh_highlight(self):
        self.highlights.clear()
        if (s := self._text_selection_start) and (e := self._text_selection_end):
            ll = min(s.line, e.line)
            gl = max(s.line, e.line)
            if gl == ll:
                lc = min(s.col, e.col)
                gc = max(s.col, e.col)
            elif s.line < e.line:
                lc = s.col
                gc = e.col
            else:
                lc = e.col
                gc = s.col
            

            letter = self.font.render("_", True, (0, 0, 0)) # This is not shown on screen, only used to get width
            w = letter.get_width()# - 1
            h = letter.get_height()

            if ll == gl:
                line = self.get_lines()[ll]
                pre = len(line[0:lc]) * w
                self._highlight_offset = [pre, (ll * h)]
                self.highlights.append(pygame.transform.scale(self._highlight, ((gc-lc)*w, h)))

            else:
                lines = self.get_lines()
                line = lines[ll]
                pre = len(line[0:lc]) * w
                self._highlight_offset = [pre, (ll * h) + 2]
                self.highlights.append(pygame.transform.scale(self._highlight, ((len(line[lc:])+1)*w, h)))
                for l in range(ll+1, gl):
                    line = lines[l]
                    self.highlights.append(pygame.transform.scale(self._highlight, ((len(line)+1)*w, h)))
                
                line = lines[gl]
                self.highlights.append(pygame.transform.scale(self._highlight, (len(line[0:gc])*w, h)))

    def get_selection(self):
        if (s := self._text_selection_start) and (e := self._text_selection_end):
            ll = min(s.line, e.line)
            gl = max(s.line, e.line)
            if s.line == e.line:
                lc = min(s.col, e.col)
                gc = max(s.col, e.col)
            elif s.line > e.line:
                lc = e.col
                gc = s.col
            else:
                lc = s.col
                gc = e.col

            lc = min(s.col, e.col)
            gc = max(s.col, e.col)

            lines = self.get_lines()[ll:gl+1]
            print(lines[-1], len(lines[-1]))
            lines[-1] = lines[-1][0:gc]
            lines[0] = lines[0][lc:]
            return "\n".join(lines)
        return None

    def set_selection(self, text:str):
        if (s := self._text_selection_start) is not None and (e := self._text_selection_end) is not None:
            ll = min(s.line, e.line)
            gl = max(s.line, e.line)
            lc = min(s.col, e.col)
            gc = max(s.col, e.col)
            
            mp = min(s, e).copy()

            lines = self.get_lines()
            pre = lines[0:ll+1]
            pre[-1] = pre[-1][0:lc]

            post = lines[gl:]
            post[0] = post[0][gc:]
            self.set_content("\n".join(pre) + text + "\n".join(post))
            self.cursor_location = mp
            self._text_selection_start = self._text_selection_end = None

    def get_index(self, cursor:Cursor):
        return sum(len(l) for l in self._lines[0:cursor.line]) + len(self._lines[cursor.line][0:cursor.col])

    def get_content(self):
        return "\n".join(["".join(line) for line in self._lines])

    def get_lines(self):
        return ["".join(line) for line in self._lines]

    def set_content(self, content:str):
        self._lines = [[*line] for line in content.split("\n")]
        self.cursor_location.line = min(self.cursor_location.line, len(self._lines)-1)
        if self._lines:
            self.cursor_location.col = min(self.cursor_location.col, len(self._lines[self.cursor_location.line])-1)
        self.refresh_surfaces()

    def refresh_surfaces(self):
        self.surfaces.clear()
        self._text_width = 0
        self._text_height = 0
        for line in self.get_lines():
            s = self.font.render(line or " ", True, tuple(self.text_color))
            self.surfaces.append(s)
            self._text_width = max(self._text_width, s.get_width())
            self._text_height += s.get_height()

    def _update(self, editor, X, Y):
        h = 0

        if self.text_bg_color:
            if isinstance(self.text_bg_color, (Image, Animation)):
                self.text_bg_color.x = self.x - 1
                self.text_bg_color.y = self.y - 1
                self.text_bg_color.width = max(self._text_width, self.min_width) + 2
                self.text_bg_color.height = max(self._text_height, self.min_height) + 2
                self.text_bg_color._update(editor, X, Y)
            else:
                editor.screen.fill(tuple(self.text_bg_color), (X+self.x-1, Y+self.y-1, max(self._text_width, self.min_width)+2, max(self._text_height, self.min_height)+2))

        l = 0
        for s in self.surfaces:
            s:pygame.Surface
            editor.screen.blit(s, (X+self.x, Y+self.y+h))
            if l == self.cursor_location.line and self._cursor_visible:
                _h = self.font.render(self.get_lines()[self.cursor_location.line][0:self.cursor_location.col], True, (0, 0, 0)) # This is not shown on screen, only used to get width
                editor.screen.blit(self._cursor_surface, (X+self.x+_h.get_width(), Y+self.y+h+2))
            h += s.get_height()
            l += 1

        if self._text_selection_start and self._text_selection_end and self.highlights:
            letter = self.font.render("_", True, (0, 0, 0)) # This is not shown on screen, only used to get width
            #w = letter.get_width()# - 1
            _h = letter.get_height()
            h = self.highlights[0]
            _x, _y = self._highlight_offset
            #print(f"highlight at: {X+self.x+_x}, {Y+self.y+_y}  mouse: {editor.mouse_pos} {h.get_size()}")
            editor.screen.blit(h, (X+self.x+_x, Y+self.y+_y))
            height = _h
            for h in self.highlights[1:]:
                editor.screen.blit(h, (X+self.x, Y+self.y+_y+height))
                height += _h

    def refresh_lines(self):
        self._lines = expand_text_lists(self._lines)

    def _event(self, editor, X, Y):
        w, h = max(self.min_width, self._text_width), max(self.min_height, self._text_height)
        _x, _y = editor.mouse_pos

        #if max(editor.X, X + self.x) <= _x <= min(X + self.x + w, editor.Width) and max(editor.Y, Y + self.y) <= _y <= min(Y + self.y + h, editor.Height):
        if editor.collides((_x, _y), (X+self.x, Y+self.y, w, h)):
            self.hovered = editor._hovered = True
        else:
            self.hovered = False

        
        if editor.left_mouse_down():
            if self.hovered:
                #if self.focused:
                letter = self.font.render("_", True, (0, 0, 0)) # This is not shown on screen, only used to get width
                w = letter.get_width()# - 1
                h = letter.get_height()
                dx = _x - (X + self.x)
                dy = _y - (Y + self.y)
                _old = self.cursor_location.copy()
                self.cursor_location.line = min(int(dy//h), len(self._lines)-1)
                self.cursor_location.col = max(min(int(round(dx/w)), len(self._lines[self.cursor_location.line])), 0)

                if pygame.K_LSHIFT in editor.keys:
                    if not self._text_selection_start:
                        self._text_selection_start = _old
                    self._text_selection_end = self.cursor_location.copy()
                else:
                    self._text_selection_start = self._text_selection_end = None

                self.focused = True
                self._cursor_visible = True
                self._cursor_tick = time.time()
                
            else:
                self.focused = False
                self._cursor_visible = False

        elif editor.mouse[0] and self.hovered:
            letter = self.font.render("_", True, (0, 0, 0))
            w = letter.get_width()# - 1
            h = letter.get_height()
            dx = _x - (X + self.x)
            dy = _y - (Y + self.y)
            _old = self.cursor_location.copy()
            self.cursor_location.line = min(int(dy//h), len(self._lines)-1)
            self.cursor_location.col = max(min(int(round(dx/w)), len(self._lines[self.cursor_location.line])), 0)

            if not self._text_selection_start:
                self._text_selection_start = _old
            self._text_selection_end = self.cursor_location.copy()
            self.refresh_highlight()

        if self.focused:
            for key in editor.typing:
                # print(f"{key!r}")
                if key == "$↑":
                    _old = self.cursor_location.copy()
                    if self.cursor_location.line == 0:
                        self.cursor_location.col = 0
                    else:
                        self.cursor_location.line -= 1
                        self.cursor_location.col = min(self.cursor_location.col, len(self._lines[self.cursor_location.line]))
                    if pygame.K_LSHIFT in editor.keys:
                        if not self._text_selection_start:
                            self._text_selection_start = _old
                        self._text_selection_end = self.cursor_location.copy()
                        self.refresh_highlight()
                    elif self._text_selection_start and self._text_selection_end:
                        self.cursor_location = min(self._text_selection_start, self._text_selection_end)
                        if self.cursor_location.line > 0:
                            self.cursor_location.line -= 1
                            self.cursor_location.col = min(self.cursor_location.col, len(self._lines[self.cursor_location.line]))
                        self._text_selection_start = self._text_selection_end = None
                elif key == "$↓":
                    _old = self.cursor_location.copy()
                    if self.cursor_location.line == len(self._lines)-1:
                        self.cursor_location.col = len(self._lines[self.cursor_location.line])
                    else:
                        self.cursor_location.line += 1
                        self.cursor_location.col = min(self.cursor_location.col, len(self._lines[self.cursor_location.line]))
                    if pygame.K_LSHIFT in editor.keys:
                        if not self._text_selection_start:
                            self._text_selection_start = _old
                        self._text_selection_end = self.cursor_location.copy()
                        self.refresh_highlight()
                    elif self._text_selection_start and self._text_selection_end:
                        self.cursor_location = max(self._text_selection_start, self._text_selection_end)
                        if self.cursor_location.line < len(self._lines)-1:
                            self.cursor_location.line += 1
                            self.cursor_location.col = min(self.cursor_location.col, len(self._lines[self.cursor_location.line]))
                        self._text_selection_start = self._text_selection_end = None
                elif key == "$→":
                    _old = self.cursor_location.copy()
                    if self.cursor_location.col == len(self._lines[self.cursor_location.line]):
                        if self.cursor_location.line < len(self._lines)-1:
                            self.cursor_location.line += 1
                            self.cursor_location.col = 0
                    else:
                        self.cursor_location.col += 1
                    if pygame.K_LSHIFT in editor.keys:
                        if not self._text_selection_start:
                            self._text_selection_start = _old
                        self._text_selection_end = self.cursor_location.copy()
                        self.refresh_highlight()
                    elif self._text_selection_start and self._text_selection_end:
                        self.cursor_location = max(self._text_selection_start, self._text_selection_end)
                        self._text_selection_start = self._text_selection_end = None
                elif key == "$←":
                    _old = self.cursor_location.copy()
                    if self.cursor_location.col == 0:
                        if self.cursor_location.line > 0:
                            self.cursor_location.line -= 1
                            self.cursor_location.col = len(self._lines[self.cursor_location.line])
                    else:
                        self.cursor_location.col -= 1
                    if pygame.K_LSHIFT in editor.keys:
                        if not self._text_selection_start:
                            self._text_selection_start = _old
                        self._text_selection_end = self.cursor_location.copy()
                        self.refresh_highlight()
                    elif self._text_selection_start and self._text_selection_end:
                        self.cursor_location = min(self._text_selection_start, self._text_selection_end)
                        self._text_selection_start = self._text_selection_end = None
                elif key in "\n\r":
                    if self.single_line:
                        continue
                    if (self._text_selection_start is not None) and (self._text_selection_end is not None):
                        self.cursor_location = self._text_selection_start.copy()
                        self.set_selection("")
                    txt = self._lines[self.cursor_location.line][self.cursor_location.col:]
                    self._lines[self.cursor_location.line] = self._lines[self.cursor_location.line][0:self.cursor_location.col]
                    self.cursor_location.line += 1
                    self.cursor_location.col = 0
                    self._lines.insert(self.cursor_location.line, txt)
                elif key == "\t":
                    pre = "".join(self._lines[self.cursor_location.line][0:self.cursor_location.col])
                    if pre.strip() == "":
                        add = " " * (4 - (len(pre) % 4))
                    else:
                        add = "    "
                    self._lines[self.cursor_location.line].insert(self.cursor_location.col, add)
                    self.refresh_lines()
                    self.cursor_location.col += len(add)
                elif key == "\b":
                    if self._text_selection_start and self._text_selection_end:
                        self.set_selection("")
                    else:
                        if self.cursor_location.col > 0:
                            txt = self._lines[self.cursor_location.line][0:self.cursor_location.col-1] + \
                                self._lines[self.cursor_location.line][self.cursor_location.col:]
                            self._lines[self.cursor_location.line] = txt
                            self.cursor_location.col -= 1
                        elif self.cursor_location.line > 0:
                            self.cursor_location.col = len(self._lines[self.cursor_location.line-1])
                            self._lines[self.cursor_location.line-1] += self._lines.pop(self.cursor_location.line)
                            self.cursor_location.line -= 1
                elif key == "\x7f": # delete
                    if self._text_selection_start and self._text_selection_end:
                        self.set_selection("")
                    else:
                        if self.cursor_location.col < len(self._lines[self.cursor_location.line]):
                            txt = self._lines[self.cursor_location.line][0:self.cursor_location.col] + \
                                self._lines[self.cursor_location.line][self.cursor_location.col+1:]
                            self._lines[self.cursor_location.line] = txt
                            # self.cursor_location.col -= 1
                        elif self.cursor_location.line < len(self._lines)-1:
                            # self.cursor_location.col = len(self._lines[self.cursor_location.line-1])
                            self._lines[self.cursor_location.line] += self._lines.pop(self.cursor_location.line+1)
                            # self.cursor_location.line -= 1
                elif key == "\x1a": # CTRL+Z
                    ...
                elif key == "\x18": # CTRL+X
                    if (self._text_selection_start is not None) and (self._text_selection_end is not None):
                        pyperclip.copy(self.get_selection())
                        self.set_selection("")
                elif key == "\x03": # CTRL+C
                    if (self._text_selection_start is not None) and (self._text_selection_end is not None):
                        pyperclip.copy(self.get_selection())
                elif key == "\x16": # CTRL+V
                    _l = pyperclip.paste()
                    if self.single_line:
                        noline = re.sub("\n+", " ", _l)
                        self._lines[self.cursor_location.line].insert(self.cursor_location.col, noline)
                        self.refresh_lines()
                        self.cursor_location.col += len(noline)
                        continue
                    l = _l.split("\n")
                    l0 = l[0]
                    self._lines[self.cursor_location.line].insert(self.cursor_location.col, l0)
                    
                    for _line in l[1:-1]:
                        self.cursor_location.line += 1
                        self._lines.insert(self.cursor_location.line, [c for c in re.split(r"", _line) if c])
                    
                    if len(l) > 1:
                        self.cursor_location.line += 1
                        if len(self._lines) <= self.cursor_location.line:
                            self._lines.append([c for c in re.split(r"", l[-1]) if c])
                        else:
                            self._lines.insert(self.cursor_location.line, [])
                            self._lines[self.cursor_location.line].insert(0, l[-1])
                    self.refresh_lines()
                    self.cursor_location.col += len(l[-1])
                elif key == "\x01": # CTRL+A
                    self._text_selection_start = Cursor(0, 0)
                    self._text_selection_end = Cursor(len(self._lines)-1, len(self._lines[-1]))
                    self.refresh_highlight()
                elif key == "\x13": # CTRL+S
                    content = self.get_content()
                    cursor = self.cursor_location.copy()
                    selection = None
                    if self._text_selection_start and self._text_selection_end:
                        selection = Selection(
                            self.get_selection(),
                            self.get_index(self._text_selection_start),
                            self.get_index(self._text_selection_end)
                        )
                    self._save(self, content, selection, cursor)
                else:
                    self._lines[self.cursor_location.line].insert(self.cursor_location.col, key)
                    self.cursor_location.col += 1
            if self._text_selection_start == self._text_selection_end and self._text_selection_start != None:
                self._text_selection_start = self._text_selection_end = None

            if (time.time() - self._cursor_tick) % 1 < 0.5:
                self._cursor_visible = True
            else:
                self._cursor_visible = False

            # self._cursor_tick += 1
            # if time.time() % 1 == 0:
            #     self._cursor_tick = 0
            #     self._cursor_visible = not self._cursor_visible


            # self.surface = self.font.render(self.get_content(), True, self.text_color)
            self.refresh_surfaces()

class Box(UIElement):

    def __init__(self, x, y, width, height, color:Color|Image|tuple|int=TEXT_COLOR):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = Color.color(color)
        self.children = []
        self.hovered = False

    def _update(self, editor, X, Y):
        if isinstance(self.color, (Image, Animation)):
            self.color._update(editor, X, Y)
            self.color.x = 0
            self.color.y = 0
            self.color.width = self.width
            self.color.height = self.height
        elif self.color:
            editor.screen.fill(tuple(self.color), (X + self.x, Y + self.y, self.width, self.height))
        for child in self.children:
            child._update(editor, X + self.x, Y + self.y)
    
    def _event(self, editor, X, Y):
        _c = self.children.copy()
        _c.reverse()
        _x, _y = editor.mouse_pos
        #if (max(editor.X, X + self.x) <= _x <= min(X + self.x + self.width, editor.Width) and max(editor.Y, Y + self.y) <= _y <= min(Y + self.y + self.height, editor.Height)):
        if editor.collides((_x, _y), (X+self.x, Y+self.y, self.width, self.height)):
            self.hovered = editor._hovered = True
        else:
            self.hovered = False

        for child in _c:
            child._event(editor, X + self.x, Y + self.y)

class LayeredObjects(UIElement):
    def __init__(self, layers:dict):
        self.layers = layers

    def _event(self, editor, X, Y):
        layers = [l for l in self.layers.keys()]
        layers.sort()
        layers.reverse()
        for l in layers:
            _l = self.layers[l]
            _l.reverse()
            for i in _l:
                i._event(editor, X, Y)

    def _update(self, editor, X, Y):
        layers = [l for l in self.layers.keys()]
        layers.sort()
        for l in layers:
            for i in self.layers[l]:
                i._update(editor, X, Y)

class Draggable(UIElement):
    def __init__(self, x, y, width, height, lock_horizontal=False, lock_vertical=False, children=[]):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.held = False
        self.hovered = False
        self.hx = 0
        self.hy = 0
        self.children = children
        self.lock_horizontal = lock_horizontal
        self.lock_vertical = lock_vertical
    
    def _event(self, editor, X, Y):

        _x, _y = editor.mouse_pos

        _c = self.children.copy()
        _c.reverse()
        for child in _c:
            child._event(editor, X + self.x, Y + self.y)

        #if max(editor.X, X + self.x) <= _x <= min(X + self.x + self.width, editor.Width) and max(editor.Y, Y + self.y) <= _y <= min(Y + self.y + self.height, editor.Height):
        if editor.collides((_x, _y), (X+self.x, Y+self.y, self.width, self.height)):
            self.hovered = editor._hovered = True
        else:
            self.hovered = False

        if editor.left_mouse_down():
            
            if self.hovered:
                if editor._focused_object is None:
                    editor._focused_object = self
                    editor.cancel_mouse_event()
                    self.held = True
                    self.hx = _x - (X + self.x)
                    self.hy = _y - (Y + self.y)
                    editor.previous_mouse = editor.mouse # set this so that only 1 object is picked up
                    
            else:
                self.held = False
                if editor._focused_object is self:
                    editor._focused_object = None
                
        elif editor.left_mouse_up():
            self.held = False
            if editor._focused_object is self:
                editor._focused_object = None

        #_x, _y = editor.mouse_pos
        if self.held:
            if not self.lock_horizontal: self.x = (_x - self.hx) - X
            if not self.lock_vertical: self.y = (_y - self.hy) - Y

    def _update(self, editor, X, Y):
        for child in self.children:
            child._update(editor, X + self.x, Y + self.y)

class Resizable(Draggable):
    def __init__(self, x:int, y:int, width:int, height:int, color:Color|Image|tuple|int=TEXT_BG_COLOR, min_width:int=1, min_height:int=1, max_width:int=..., max_height:int=..., can_drag:bool=True):
        
        assert 0 < min_width <= width, "width must be 1 or more"
        assert 0 < min_height <= height, "height must be 1 or more"

        super().__init__(x, y, width, height)
        self.min_width = min_width
        self.min_height = min_height
        self.max_width = max_width
        self.max_height = max_height
        self.color = Color.color(color)
        self.can_drag = can_drag
        self.hovered = False
        self.children = []

        self.right_resize = Draggable(self.width + 1, 0, 5, self.height, lock_vertical=True)
        self.down_resize = Draggable(0, self.height + 1, self.width, 5, lock_horizontal=True)
        self.corner_resize = Draggable(self.width+1, self.height+1, 5, 5)

        self.bg = Box(0, 0, self.width, self.height, self.color)

    def _event(self, editor, X, Y):
        _x, _y = editor.mouse_pos

        self.bg._event(editor, X + self.x, Y + self.y)
        self.corner_resize._event(editor, X + self.x, Y + self.y)
        self.down_resize._event(editor, X + self.x, Y + self.y)
        self.right_resize._event(editor, X + self.x, Y + self.y)

        for child in self.children:
            child._event(editor, X + self.x, Y + self.y)

        #if max(editor.X, X + self.x) <= _x <= min(X + self.x + self.width, editor.Width) and max(editor.Y, Y + self.y) <= _y <= min(Y + self.y + self.height, editor.Height):
        if editor.collides((_x, _y), (X+self.x, Y+self.y, self.width, self.height)):
            self.hovered = editor._hovered = True
        else:
            self.hovered = False

        if self.can_drag:
            if editor.left_mouse_down():
                
                if self.hovered:
                    if editor._focused_object is None:
                        editor._focused_object = self
                        editor.cancel_mouse_event()
                        self.held = True
                        self.hx = _x - (X + self.x)
                        self.hy = _y - (Y + self.y)
                        editor.previous_mouse = editor.mouse # set this so that only 1 object is picked up
                        
                else:
                    self.held = False
                    if editor._focused_object is self:
                        editor._focused_object = None
                    
            elif editor.left_mouse_up():
                self.held = False
                if editor._focused_object is self:
                    editor._focused_object = None

        #_x, _y = editor.mouse_pos
        if self.held: # this will never be True if self.can_drag is False.
            if not self.lock_horizontal: self.x = (_x - self.hx) - X
            if not self.lock_vertical: self.y = (_y - self.hy) - Y

        if self.right_resize.held:
            self.right_resize.x = self.corner_resize.x = max(self.min_width, self.right_resize.x)
        if self.down_resize.held:
            self.down_resize.y = self.corner_resize.y = max(self.min_height, self.down_resize.y)
        if self.corner_resize.held:
            self.right_resize.x = self.corner_resize.x = max(self.min_width, self.corner_resize.x)
            self.down_resize.y = self.corner_resize.y = max(self.min_height, self.corner_resize.y)
            
        self.width = self.bg.width = self.down_resize.width = self.right_resize.x
        self.height = self.bg.height = self.right_resize.height = self.down_resize.y

    def _update(self, editor, X, Y):
        _c = self.children.copy()
        _c.reverse()
        for child in _c:
            child._update(editor, X + self.x, Y + self.y)
        self.right_resize._update(editor, X + self.x, Y + self.y)
        self.down_resize._update(editor, X + self.x, Y + self.y)
        self.corner_resize._update(editor, X + self.x, Y + self.y)
        self.bg._update(editor, X + self.x, Y + self.y)

class Button(UIElement):

    class _overrider:
        def __init__(self, parent):
            self._parent = parent
            self.screen = parent.surface

    def __init__(self, x:int, y:int, width:int, height:int|None=None, text:str="", bg_color:Color|Image|tuple|int|None=TEXT_BG_COLOR, text_color:Color|tuple|int=TEXT_COLOR, text_size:int=TEXT_SIZE, hover_color:tuple|list|Color=TEXT_BG_COLOR, click_color:tuple|list|Color=TEXT_BG_COLOR):
        self.x = x
        self.y = y
        self.width = width
        self.height = height or text_size + 4
        self.text = text
        self.bg_color = self._bg_color = Color.color(bg_color)
        self.hover_color = Color.color(hover_color)
        self.click_color = Color.color(click_color)
        self.text_color = Color.color(text_color)
        self.lheld = False
        self.rheld = False
        self.hovered = False
        self._hovered = False
        self.children = []
        self._uoffx = 0
        self._uoffy = 0
        #self.held = False
        self.text_size = text_size
        self.font = pygame.font.Font(FONT, text_size)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32) # pylint: disable=no-member
        if self.bg_color:
            if isinstance(self.bg_color, (Image, Animation)):
                self.bg_color.partial_update()
                self.surface.blit(self.bg_color.surface, (0, 0))
            elif isinstance(self.bg_color, Color):
                self.bg_color = self.bg_color.with_alpha()
            else:
                if len(self.bg_color) == 3:
                    self.bg_color = Color(*self.bg_color, 255)
                self.surface.fill(self.bg_color)
        self.surface.blit(self.font.render(self.text, True, tuple(self.text_color)), (1, 1))
        self._override = self._overrider(self)
        self._mimic = EditorMimic(None, self._override)

    def _event(self, editor, X, Y):
        for child in self.children:
            child._event(editor, X+self.x+self._uoffx, Y+self.y+self._uoffy)
        _x, _y = editor.mouse_pos
        self._hovered = self.hovered
        self._mimic._editor = editor
        #if max(editor.X, X + self.x) <= _x <= min(X + self.x + self.width, editor.Width) and max(editor.Y, Y + self.y) <= _y <= min(Y + self.y + self.height, editor.Height):
        if self.bg_color:
            if isinstance(self.bg_color, (Image, Animation)):
                self.bg_color.x = 0
                self.bg_color.y = 0
                self.bg_color.width = self.width
                self.bg_color.height = self.height
                self.bg_color._event(self._mimic, X+self.x, Y+self.y)
        
        if editor.collides((_x, _y), (X+self.x, Y+self.y, self.width, self.height)):
            self.hovered = editor._hovered = True
            self.bg_color = self.hover_color
            if not self._hovered:
                self.on_hover(editor)
            if editor.left_mouse_down():
                self.bg_color = self.click_color
                self.on_left_click(editor)
                editor.cancel_mouse_event()
                self.lheld = True
            if editor.right_mouse_down():
                self.on_right_click(editor)
                editor.cancel_mouse_event()
                self.rheld = True
        else:
            self.hovered = False
            self.bg_color = self._bg_color
            if self._hovered is True:
                self.off_hover(editor)
        if editor.left_mouse_up():
            if self.lheld:
                self.off_left_click(editor)
            self.lheld = False
        if editor.right_mouse_up():
            if self.rheld:
                self.off_right_click(editor)
            self.rheld = False

        

        #self.update(editor, X, Y)

    def _update(self, editor, X, Y):
        for child in self.children:
            child._update(editor, X+self.x+self._uoffx, Y+self.y+self._uoffy)
            
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32) # pylint: disable=no-member
        self._override.screen = self.surface
        self._mimic._editor = editor
        if self.bg_color:
            if isinstance(self.bg_color, (Image, Animation)):
                self.bg_color.x = 0
                self.bg_color.y = 0
                self.bg_color.width = self.width
                self.bg_color.height = self.height
                self.bg_color.partial_update()
                self.bg_color._update(self._mimic, 0, 0)
                # self.surface.blit(self.bg_color.surface, (0, 0))
            else:
                self.surface.fill(tuple(self.bg_color))
        self.surface.blit(self.font.render(self.text, True, tuple(self.text_color)), (1, 1))

        self.pre_blit(editor, X, Y)

        editor.screen.blit(self.surface, (X+self.x, Y+self.y))
    
    def pre_blit(self, editor, X, Y): ... # pylint: disable=unused-argument
    def on_left_click(self, editor): ... # pylint: disable=unused-argument
    def off_left_click(self, editor): ... # pylint: disable=unused-argument
    def on_right_click(self, editor): ... # pylint: disable=unused-argument
    def off_right_click(self, editor): ... # pylint: disable=unused-argument
    def on_hover(self, editor): ... # pylint: disable=unused-argument
    def off_hover(self, editor): ... # pylint: disable=unused-argument

class Tabs(UIElement):
    class Style(Enum):
        TOP = auto()
        BOTTOM = auto()
        LEFT = auto()
        RIGHT = auto()
        MENU = auto()
        TOP_BOTTOM = auto()
        LEFT_RIGHT = auto()
        # BOTTOM_TOP = auto()
        # RIGHT_LEFT = auto()
        # TOP_BOTTOM_ALT = auto()
        # LEFT_RIGHT_ALT = auto()
        # BOTTOM_TOP_ALT = auto()
        # RIGHT_LEFT_ALT = auto()

    class _Tab(Button):
        def __init__(self, parent, x, y, width, height, location, text, tcu:tuple[int, int, int]|Image=TEXT_COLOR, tch:tuple[int, int, int]|Image=TEXT_COLOR, tcs:tuple[int, int, int]|Image=TEXT_COLOR, bgu:tuple[int, int, int]|Image=TEXT_BG_COLOR, bgh:tuple[int, int, int]|Image=TEXT_BG_COLOR, bgs:tuple[int, int, int]|Image=TEXT_BG_COLOR, text_size=TEXT_SIZE):
            super().__init__(x, y, width, height, text, bgu, tcu, text_size)
            self.tcu:tuple[int, int, int]|Image = tcu
            self.tch:tuple[int, int, int]|Image = tch
            self.tcs:tuple[int, int, int]|Image = tcs
            self.bgu:tuple[int, int, int]|Image = bgu
            self.bgh:tuple[int, int, int]|Image = bgh
            self.bgs:tuple[int, int, int]|Image = bgs
            self.location = location
            self.tabs_parent = parent

        def on_left_click(self, editor):
            self.bg_color = self.bgs
            self.text_color = self.tcs

            self.tabs_parent.active_tab = self.text
        
        def off_left_click(self, editor):
            if self.hovered:
                self.bg_color = self.bgh
                self.text_color = self.tch
            else:
                self.bg_color = self.bgu
                self.text_color = self.tcu
        
        def on_hover(self, editor):
            self.bg_color = self.bgh
            self.text_color = self.tch

        def off_hover(self, editor):
            self.bg_color = self.bgu
            self.text_color = self.tcu

        def pre_blit(self, editor, X, Y):
            if self.location == Tabs.Style.LEFT:
                self.surface = pygame.transform.rotate(self.surface, 90)
            elif self.location == Tabs.Style.RIGHT:
                self.surface = pygame.transform.rotate(self.surface, -90)

    def __init__(self, x:int, y:int, width:int, height:int, tab_style:Style=Style.TOP, tab_data:dict[str, list]=..., **options):
        """
        options:\n
        `tab_color_unselected`: Color|list|tuple[int, int, int]\n
        `tab_color_hovered`: Color|list|tuple[int, int, int]\n
        `tab_color_selected`: Color|list|tuple[int, int, int]\n

        `tab_color_empty`: Color|list|tuple[int, int, int]|None\n
        - default is None\n

        `content_bg_color`: Color|list|tuple[int, int, int]|None\n
        - default is None\n

        `text_color_unselected`: Color|list|tuple[int, int, int]\n
        `text_color_hovered`: Color|list|tuple[int, int, int]\n
        `text_color_selected`: Color|list|tuple[int, int, int]\n

        `tab_buffer`: int (how much space to pad the left (or top) of the tabs with)\n
        - top is padded in left/right modes, left in top/bottom modes\n

        `tab_height`: int (how high the tab is (or wide if on left/right))\n
        `tab_width`: int (default is 75 px)\n

        `scrollable_tabs`: bool (default is False)\n
        """
        if tab_data is ...: tab_data = {}
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tab_style = tab_style
        self.tab_data = tab_data
        # self.tx = 0
        # self.ty = 0
        if tab_data:
            self.active_tab = [*tab_data.keys()][0]
        else:
            self.active_tab = None
        
        self.tab_color_unselected  : Color|tuple[int, int, int]|Image      = Color.color(options.get("tab_color_unselected", (150, 150, 150)))
        self.tab_color_hovered     : Color|tuple[int, int, int]|Image      = Color.color(options.get("tab_color_hovered", (200, 200, 200)))
        self.tab_color_selected    : Color|tuple[int, int, int]|Image      = Color.color(options.get("tab_color_selected", (100, 100, 100)))

        self.tab_color_empty       : Color|tuple[int, int, int]|Image|None = Color.color(options.get("tab_color_empty", None))
        
        self.text_color_unselected : Color|tuple[int, int, int]|Image      = Color.color(options.get("text_color_unselected", TEXT_COLOR))
        self.text_color_hovered    : Color|tuple[int, int, int]|Image      = Color.color(options.get("text_color_hovered", TEXT_COLOR))
        self.text_color_selected   : Color|tuple[int, int, int]|Image      = Color.color(options.get("text_color_selected", TEXT_COLOR))
             
        self.content_bg_color      : Color|tuple[int, int, int]|Image|None = Color.color(options.get("content_bg_color", None))
        
        self.tab_buffer            : int                             = options.get("tab_buffer", 0)
        self.tab_height            : int                             = options.get("tab_height", TEXT_SIZE + 2)
        self.tab_width             : int                             = options.get("tab_width", 75)

        self.scrollable_tabs       : bool                            = options.get("scrollable_tabs", False)
        if self.scrollable_tabs:
            self._tabs_area = Scrollable(self.x, self.y, 1, 1, self.tab_color_empty, left_bound=0, top_bound=0)
        else:
            self._tab_objects = []
        self.load_tabs()

    def load_tabs(self):
        if self.scrollable_tabs:
            self._tabs_area.children.clear()
        else:
            self._tab_objects = []

        if self.tab_style == Tabs.Style.TOP:
            if self.scrollable_tabs:
                x = 0
                y = 0
                self._tabs_area.right_bound = 0
                self._tabs_area.bottom_bound = 0
                self._tabs_area.x = self.x + self.tab_buffer
                self._tabs_area.y = self.y - self.tab_height
                self._tabs_area.width = self.width - self.tab_buffer
                self._tabs_area.height = self.tab_height
            else:
                x = self.tab_buffer
                y = -self.tab_height
            for name in self.tab_data.keys():
                t = Tabs._Tab(self, x, y, self.tab_width, self.tab_height, Tabs.Style.TOP, name, self.text_color_unselected, self.text_color_hovered, self.text_color_selected, self.tab_color_unselected, self.tab_color_hovered, self.tab_color_selected)
                if self.scrollable_tabs:
                    t.width = t.font.render(t.text, True, (0, 0, 0)).get_width()
                    self._tabs_area.children.append(t)
                    x += t.width + 1
                else:
                    self._tab_objects.append(t)
                    x += self.tab_width + 1
            if self.scrollable_tabs:
                self._tabs_area.right_bound = -x
        
        elif self.tab_style == Tabs.Style.BOTTOM:
            if self.scrollable_tabs:
                x = 0
                y = 0
                self._tabs_area.right_bound = 0
                self._tabs_area.bottom_bound = 0
                self._tabs_area.x = self.x + self.tab_buffer
                self._tabs_area.y = self.y + self.height
                self._tabs_area.width = self.width - self.tab_buffer
                self._tabs_area.height = self.tab_height
            else:
                x = self.tab_buffer
                y = -self.tab_height
            for name in self.tab_data.keys():
                t = Tabs._Tab(self, x, y, self.tab_width, self.tab_height, Tabs.Style.TOP, name, self.text_color_unselected, self.text_color_hovered, self.text_color_selected, self.tab_color_unselected, self.tab_color_hovered, self.tab_color_selected)
                if self.scrollable_tabs:
                    t.width = t.font.render(t.text, True, (0, 0, 0)).get_width()
                    self._tabs_area.children.append(t)
                    x += t.width + 1
                else:
                    self._tab_objects.append(t)
                    x += self.tab_width + 1
            if self.scrollable_tabs:
                self._tabs_area.right_bound = -x

        elif self.tab_style == Tabs.Style.LEFT:
            if self.scrollable_tabs:
                x = 0
                y = 0
                self._tabs_area.right_bound = 0
                self._tabs_area.bottom_bound = 0
                self._tabs_area.x = self.x - self.tab_height
                self._tabs_area.y = self.y + self.tab_buffer
                self._tabs_area.width = self.tab_height
                self._tabs_area.height = self.height - self.tab_buffer
            else:
                x = -self.tab_height
                y = self.tab_buffer
            for name in self.tab_data.keys():
                t = Tabs._Tab(self, x, y, self.tab_width, self.tab_height, Tabs.Style.LEFT, name, self.text_color_unselected, self.text_color_hovered, self.text_color_selected, self.tab_color_unselected, self.tab_color_hovered, self.tab_color_selected)
                if self.scrollable_tabs:
                    t.width = t.font.render(t.text, True, (0, 0, 0)).get_width()
                    self._tabs_area.children.append(t)
                    y += t.width + 1
                else:
                    self._tab_objects.append(t)
                    y += self.tab_width + 1
            if self.scrollable_tabs:
                self._tabs_area.bottom_bound = -y

        elif self.tab_style == Tabs.Style.RIGHT:
            if self.scrollable_tabs:
                x = 0
                y = 0
                self._tabs_area.right_bound = 0
                self._tabs_area.bottom_bound = 0
                self._tabs_area.x = self.x + self.width
                self._tabs_area.y = self.y + self.tab_buffer
                self._tabs_area.width = self.tab_height
                self._tabs_area.height = self.height - self.tab_buffer
            else:
                x = -self.tab_height
                y = self.tab_buffer
            for name in self.tab_data.keys():
                t = Tabs._Tab(self, x, y, self.tab_width, self.tab_height, Tabs.Style.LEFT, name, self.text_color_unselected, self.text_color_hovered, self.text_color_selected, self.tab_color_unselected, self.tab_color_hovered, self.tab_color_selected)
                if self.scrollable_tabs:
                    t.width = t.font.render(t.text, True, (0, 0, 0)).get_width()
                    self._tabs_area.children.append(t)
                    y += t.width + 1
                else:
                    self._tab_objects.append(t)
                    y += self.tab_width + 1
            if self.scrollable_tabs:
                self._tabs_area.bottom_bound = -y

        elif self.tab_style == Tabs.Style.MENU:
            if self.scrollable_tabs:
                x = 0
                y = 0
                self._tabs_area.right_bound = 0
                self._tabs_area.bottom_bound = 0
                self._tabs_area.x = self.x - self.tab_width
                self._tabs_area.y = self.y + self.tab_buffer
                self._tabs_area.width = self.tab_width
                self._tabs_area.height = self.height - self.tab_buffer
                mw = 0
            else:
                x = -self.tab_width
                y = 0
            for name in self.tab_data.keys():
                t = Tabs._Tab(self, x, y, self.tab_width, self.tab_height, Tabs.Style.MENU, name, self.text_color_unselected, self.text_color_hovered, self.text_color_selected, self.tab_color_unselected, self.tab_color_hovered, self.tab_color_selected)
                if self.scrollable_tabs:
                    t.width = t.font.render(t.text, True, (0, 0, 0)).get_width()
                    mw = max(t.width, mw)
                    self._tabs_area.children.append(t)
                    #self._tabs_area.right_bound = min(self._tabs_area.right_bound, -t.width)
                    y += self.tab_height
                else:
                    self._tab_objects.append(t)
                    y += self.tab_height
            if self.scrollable_tabs:
                for tab in self._tabs_area.children:
                    tab.width = mw
                
                self._tabs_area.right_bound = -mw
                self._tabs_area.bottom_bound = -y

        else:
            raise Exception(f"{self.tab_style} is not implemented yet")

    def add_tab(self, tab_name:str, contents:list=...):
        if contents is ...: contents = []
        self.tab_data[tab_name] = contents
        self.load_tabs()

    def add_content(self, tab_name:str, contents:list|tuple):
        contents = list(contents)
        for c in contents:
            self.tab_data.get(tab_name).append(c)

    def remove_content(self, tab_name:str, item):
        if tab_name in self.tab_data.keys():
            if item in self.tab_data[tab_name]:
                self.tab_data[tab_name].remove(item)

    def rename_tab(self, old_name:str, new_name:str):
        if old_name in self.tab_data.keys():
            self.tab_data[new_name] = self.tab_data.pop(old_name)
            self.load_tabs()

    def remove_tab(self, tab_name:str):
        if tab_name in self.tab_data.keys():
            self.tab_data.pop(tab_name)
            self.load_tabs()

    def get_active_tab(self):
        return self.active_tab

    def _update(self, editor, X, Y):

        if self.tab_color_empty:
            if isinstance(self.tab_color_empty, (Image, Animation)):
                ...
            else:
                if self.tab_style == Tabs.Style.LEFT:
                    editor.screen.fill(self.tab_color_empty, (X+self.x-self.tab_height, Y+self.y+self.tab_buffer, self.tab_height, self.height-self.tab_buffer))
                elif self.tab_style == Tabs.Style.TOP:
                    editor.screen.fill(tuple(self.tab_color_empty), (X+self.x+self.tab_buffer, Y+self.y-self.tab_height, self.width-self.tab_buffer, self.tab_height))
                elif self.tab_style == Tabs.Style.RIGHT:
                    editor.screen.fill(self.tab_color_empty, (X+self.x+self.width, Y+self.y+self.tab_buffer, self.tab_height, self.height-self.tab_buffer))
                elif self.tab_style == Tabs.Style.BOTTOM:
                    editor.screen.fill(self.tab_color_empty, (X+self.x+self.tab_buffer, Y+self.y+self.height, self.width-self.tab_buffer, self.tab_height))
                elif self.tab_style == Tabs.Style.MENU:
                    editor.screen.fill(tuple(self.tab_color_empty), (X+self.x-self.tab_width, Y+self.y+self.tab_buffer, self.tab_width, self.height-self.tab_buffer))

        if self.content_bg_color:
            editor.screen.fill(tuple(self.content_bg_color), (X+self.x, Y+self.y, self.width, self.height))

        if self.scrollable_tabs:
            self._tabs_area._update(editor, X, Y)
        else:
            for tab in self._tab_objects:
                tab:Tabs._Tab
                tab._update(editor, X+self.x, Y+self.y)
        
        content = self.tab_data.get(self.active_tab, [])
        for c in content:
            c._update(editor, X, Y)

    def _event(self, editor, X, Y):
        content = self.tab_data.get(self.active_tab, [])
        
        content.reverse()
        for c in content:
            c._event(editor, X, Y)

        if self.scrollable_tabs:
            self._tabs_area._event(editor, X, Y)
        else:
            for tab in self._tab_objects:
                tab:Tabs._Tab
                tab._event(editor, X+self.x, Y+self.y)

class Scrollable:
    class _Scrollable(UIElement):
        def __init__(self, parent:UIElement, x:int, y:int, width:int, height:int, bg_color:Color|tuple|int|Image|Animation=TEXT_BG_COLOR, **options):
            self.parent = parent
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.bg_color = Color.color(bg_color)
            self.children = options.get("children", [])
            self.offsetX = 0
            self.offsetY = 0
            self.hovered = False
            self.left_bound = options.get("left_bound", None)
            self.top_bound = options.get("top_bound", None)
            self.right_bound = options.get("right_bound", None)
            self.bottom_bound = options.get("bottom_bound", None)
            if self.left_bound is not None and self.right_bound is not None:
                assert self.left_bound >= self.right_bound, "left bound must be larger than left bound (I know, it's wierd)"
            if self.top_bound is not None and self.bottom_bound is not None:
                assert self.top_bound >= self.bottom_bound, "top bound must be larger than bottom bound (I know, it's wierd)"
            self.mouse_pos = [0, 0]
            self.screen = pygame.Surface((width, height), pygame.SRCALPHA, 32) # pylint: disable=no-member 

        def set_editor(self, editor):
            self.parent._editor = editor
            self.mouse_pos = list(editor.mouse_pos)
            self.mouse_pos[0] -= self.x + self.offsetX
            self.mouse_pos[1] -= self.y + self.offsetY

        def collides(self, mouse, rect) -> bool:
            mx, my = mouse
            x, y, w, h = rect
            #print("Scrollable: v")
            if self.parent._fake_editor.collides((mx+self.x+self.offsetX, my+self.y+self.offsetY), (self.x, self.y, self.width, self.height)):
                #print(f"Scrollable: \033[38;2;20;200;20m{mouse} \033[38;2;200;200;20m{rect}\033[0m")
                if x <= mx <= x + w and y <= my <= y + h:
                    return True

            return False

        def _update(self, editor, X, Y):
            self.set_editor(editor)
            # self.mouse_pos[0] -= X
            # self.mouse_pos[1] -= Y

            self.screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32) # pylint: disable=no-member
            if self.bg_color:
                if isinstance(self.bg_color, (Image, Animation)):
                    self.bg_color._update(self.parent, X+self.offsetX, Y+self.offsetY)
                else:
                    self.screen.fill(tuple(self.bg_color))
            #self.update(editor, self.offsetX, self.offsetY)
            for child in self.children:
                child._update(self.parent, self.offsetX, self.offsetY)
            editor.screen.blit(self.screen, (X+self.x, Y+self.y))

        def clamp(self):
            if self.left_bound is not None:
                self.offsetX = min(self.offsetX, self.left_bound)
            if self.right_bound is not None:
                self.offsetX = max(self.offsetX, self.right_bound)
            if self.top_bound is not None:
                self.offsetY = min(self.offsetY, self.top_bound)
            if self.bottom_bound is not None:
                self.offsetY = max(self.offsetY, self.bottom_bound)

        def _event(self, editor, X, Y):
            _x, _y = editor.mouse_pos
            self.set_editor(editor)
            # self.mouse_pos[0] -= X
            # self.mouse_pos[1] -= Y

            _c = self.children.copy()
            _c.reverse()
            for child in _c:
                child._event(self.parent, 0, 0)

            #print(f"Scrollable: {_y-self.y=} {_y-self.y==self.mouse_pos[1]=}")

            if editor.collides((_x, _y), (self.x, self.y, self.width, self.height)):
                self.hovered = True
                if editor.scroll is not None:
                    if pygame.K_LSHIFT in editor.keys: # pylint: disable=no-member
                        self.offsetX += editor.scroll * SCROLL_MULTIPLIER
                        if self.left_bound is not None:
                            self.offsetX = min(self.offsetX, self.left_bound)
                        if self.right_bound is not None:
                            self.offsetX = max(self.offsetX, self.right_bound)
                    else:
                        self.offsetY += editor.scroll * SCROLL_MULTIPLIER
                        if self.top_bound is not None:
                            self.offsetY = min(self.offsetY, self.top_bound)
                        if self.bottom_bound is not None:
                            self.offsetY = max(self.offsetY, self.bottom_bound)
            else:
                self.hovered = False

            if self.hovered and editor.middle_mouse_down():
                self.offsetX = self.left_bound or 0
                self.offsetY = self.top_bound or 0
                editor.cancel_mouse_event()

    def __init__(self, x, y, width, height, bg_color=TEXT_BG_COLOR, **options):
        super().__setattr__("_fake_editor", None)
        super().__setattr__("_scrollable", Scrollable._Scrollable(self, x, y, width, height, bg_color, **options))
    def __getattribute__(self, __name: str):
        if __name == "_fake_editor":
            return super().__getattribute__("_fake_editor")
        elif __name == "_scrollable":
            return super().__getattribute__("_scrollable")
        elif __name == "Width":
            #co = getattr(super().__getattribute__("_scrollable"), "offsetX")
            cx = getattr(super().__getattribute__("_scrollable"), "x")# - getattr(super().__getattribute__("_scrollable"), "offsetX")
            cw = getattr(super().__getattribute__("_scrollable"), "width")# - getattr(super().__getattribute__("_scrollable"), "offsetX")
            if hasattr(super().__getattribute__("_fake_editor"), "x"):
                fx = getattr(super().__getattribute__("_fake_editor"), "x")
            else: fx = 0
            if hasattr(super().__getattribute__("_fake_editor"), "get_width"):
                fw = getattr(super().__getattribute__("_fake_editor"), "get_width")()
            else: fw = getattr(super().__getattribute__("_fake_editor"), "width")
            if fx + fw <= fx + cx + cw: return fw - cx
            return cw# - co
        elif __name == "Height":
            #co = getattr(super().__getattribute__("_scrollable"), "offsetY")
            cx = getattr(super().__getattribute__("_scrollable"), "y")# - getattr(super().__getattribute__("_scrollable"), "offsetY")
            cw = getattr(super().__getattribute__("_scrollable"), "height")# - getattr(super().__getattribute__("_scrollable"), "offsetY")
            if hasattr(super().__getattribute__("_fake_editor"), "y"):
                fx = getattr(super().__getattribute__("_fake_editor"), "y")
            else: fx = 0
            if hasattr(super().__getattribute__("_fake_editor"), "get_height"):
                fw = getattr(super().__getattribute__("_fake_editor"), "get_height")()
            else: fw = getattr(super().__getattribute__("_fake_editor"), "height")
            if fx + fw <= fx + cx + cw: return fw - cx
            return cw# - co
        elif __name == "X":
            return max(0, getattr(super().__getattribute__("_scrollable"), "x"))
        elif __name == "Y":
            return max(0, getattr(super().__getattribute__("_scrollable"), "y"))
        elif hasattr(super().__getattribute__("_scrollable"), __name):
            return getattr(super().__getattribute__("_scrollable"), __name)
        elif hasattr(super().__getattribute__("_fake_editor"), __name):
            return getattr(super().__getattribute__("_fake_editor"), __name)
        else:
            raise AttributeError
    def __setattr__(self, __name: str, __value) -> None:
        if __name == "_editor":
            super().__setattr__("_fake_editor", __value)
        elif hasattr(super().__getattribute__("_scrollable"), __name):
            setattr(super().__getattribute__("_scrollable"), __name, __value)
        elif hasattr(super().__getattribute__("_fake_editor"), __name):
            setattr(super().__getattribute__("_fake_editor"), __name, __value)
        else:
            setattr(super().__getattribute__("_scrollable"), __name, __value)

class Collapsable:
    class SplitType(Enum):
        VERTICAL_LEFT = auto()
        HORIZONTAL_TOP = auto()
        VERTICAL_RIGHT = auto()
        HORIZONTAL_BOTTOM = auto()

    class _Collapsable(UIElement):
        def __init__(self, parent:UIElement, x:int, y:int, width:int, height:int, main_content:list=[], side_content:list=[], **options): # pylint: disable=dangerous-default-value
            
            self.parent = parent
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.split_type = options.get("split_type", Collapsable.SplitType.VERTICAL_LEFT)

            if self.split_type in [Collapsable.SplitType.VERTICAL_LEFT, Collapsable.SplitType.VERTICAL_RIGHT]:
                self.split_size:int|float = options.get("split_size", width/2)
            elif self.split_type in [Collapsable.SplitType.HORIZONTAL_TOP, Collapsable.SplitType.HORIZONTAL_BOTTOM]:
                self.split_size:int|float = options.get("split_size", height/2)
            else:
                self.split_size:int|float = 1
                raise TypeError("split_type must be either SplitType.VERTICAL_LEFT, SplitType.VERTICAL_RIGHT, SplitType.HORIZONTAL_TOP, or SplitType.HORIZONTAL_BOTTOM")
            
            self._split_size = self.split_size
            self.split_min = options.get("split_min", 1)
            self.split_draggable = options.get("split_draggable", True)
            self.split_visible = options.get("split_visible", True)

            self.screen = pygame.Surface((self.width, self.height))
            self.mouse_pos = [0, 0]

            if self.split_type == Collapsable.SplitType.VERTICAL_LEFT:
                self.main_area = Scrollable(0, 0, width - self.split_size, height)
                self.main_area.children = main_content
                self.aside = Scrollable(width - self.split_size, 0, self.split_size, height)
                self.aside.children = side_content

                self.split = Draggable((width - self.split_size) - 2, 0, 4, height, lock_vertical=True)

                if not self.split_visible:
                    self.main_area.width = width
                    self.aside.width = 0
                    self.aside.x = width
                    self.split.x = width - 2
            
            elif self.split_type == Collapsable.SplitType.VERTICAL_RIGHT:
                self.main_area = Scrollable(self.split_size, 0, width - self.split_size, height)
                self.main_area.children = main_content
                self.aside = Scrollable(0, 0, self.split_size, height)
                self.aside.children = side_content

                self.split = Draggable(self.split_size - 2, 0, 4, height, lock_vertical=True)

                if not self.split_visible:
                    self.main_area.width = width
                    self.main_area.x = 0
                    self.aside.width = 0
                    self.split.x = -2

            elif self.split_type == Collapsable.SplitType.HORIZONTAL_TOP:
                self.main_area = Scrollable(0, 0, width, height - self.split_size)
                self.main_area.children = main_content
                self.aside = Scrollable(0, height - self.split_size, width, self.split_size)
                self.aside.children = side_content

                self.split = Draggable(0, (height - self.split_size) - 2, width, 4, lock_horizontal=True)

                if not self.split_visible:
                    self.main_area.height = height
                    self.aside.height = 0
                    self.aside.y = height
                    self.split.y = height - 2

            elif self.split_type == Collapsable.SplitType.HORIZONTAL_BOTTOM:
                self.main_area = Scrollable(0, self.split_size, width, height - self.split_size)
                self.main_area.children = main_content
                self.aside = Scrollable(0, 0, width, self.split_size)
                self.aside.children = side_content

                self.split = Draggable(0, self.split_size-2, width, 4, lock_horizontal=True)

                if not self.split_visible:
                    self.main_area.height = height
                    self.main_area.y = 0
                    self.aside.height = 0
                    self.split.y = -2

        def set_editor(self, editor):
            self.parent._editor = editor
            self.mouse_pos = list(editor.mouse_pos)
            self.mouse_pos[0] -= self.x
            self.mouse_pos[1] -= self.y

        def collides(self, mouse, rect) -> bool:
            mx, my = mouse
            x, y, w, h = rect

            #print("Collapsable: v")
            if self.parent._fake_editor.collides((mx+self.x, my+self.y), (self.x, self.y, self.width, self.height)):
                #print(f"Collapsable: \033[38;2;20;200;20m{mouse} \033[38;2;200;200;20m{rect}\033[0m")
                if x <= mx <= x + w and y <= my <= y + h:
                    return True
            return False

        def _event(self, editor, X, Y):
            self.set_editor(editor)

            if self.split_type == Collapsable.SplitType.VERTICAL_LEFT:
                if not self.split_draggable:
                    self.split.lock_horizontal = True
                    #self.split.lock_vertical = True
                else:
                    self.split.lock_horizontal = False

                self.main_area.width = (self.split.x + 2) # +2 to split so that it's based on the center of the split
                self.aside.x = (self.split.x + 2)
                self.aside.width = self.width - (self.split.x + 2)

                if (not self.split.held) and (self.width - (self.split.x + 2) < self.split_min):
                    self.main_area.width = self.width
                    self.split.x = self.width - 2
                    self.split_visible = False
                    self.aside.x = self.width
                    self.aside.width = 0
                if self.split_size > 0:
                    self.split_visible = True

            elif self.split_type == Collapsable.SplitType.VERTICAL_RIGHT:

                if not self.split_draggable:
                    self.split.lock_horizontal = True
                    #self.split.lock_vertical = True
                else:
                    self.split.lock_horizontal = False

                self.main_area.x = (self.split.x + 2)
                self.main_area.width = self.width - (self.split.x + 2)
                self.aside.width = (self.split.x + 2)

                if (not self.split.held) and ((self.split.x + 2) < self.split_min):
                    self.split.x = -2
                    self.aside.width = 0
                    self.main_area.x = 0
                    self.split_visible = False
                
                if self.split_size > 0:
                    self.split_visible = True

            elif self.split_type == Collapsable.SplitType.HORIZONTAL_TOP:
                if not self.split_draggable:
                    self.split.lock_vertical = True
                    #self.split.lock_vertical = True
                else:
                    self.split.lock_vertical = False
                
                self.main_area.height = (self.split.y + 2)
                self.aside.y = (self.split.y + 2)
                self.aside.height = self.height - (self.split.y + 2)

                if (not self.split.held) and (self.height - (self.split.y + 2) < self.split_min):
                    self.split.y = -2
                    self.split_visible = False
                    self.main_area.height = self.height
                    self.aside.y = self.height
                    self.aside.height = 0

                if self.split_size > 0:
                    self.split_visible = True

            elif self.split_type == Collapsable.SplitType.HORIZONTAL_BOTTOM:
                if not self.split_draggable:
                    self.split.lock_vertical = True
                    #self.split.lock_vertical = True
                else:
                    self.split.lock_vertical = False
                
                self.aside.height = (self.split.y + 2)
                self.main_area.y = (self.split.y + 2)
                self.main_area.height = self.height - (self.split.y + 2)

                if (not self.split.held) and ((self.split.y + 2) < self.split_min):
                    self.split.y = self.height - 2
                    self.main_area.height = self.height
                    self.aside.y = self.height
                    self.aside.height = 0
                    self.split_visible = False

                if self.split_size > 0:
                    self.split_visible = True

            self.split._event(self.parent, 0, 0)

            self.main_area._event(self.parent, 0, 0)

            if self.split_visible:
                self.aside._event(self.parent, 0, 0)

            self.split.x = min(max(-2, self.split.x), self.width-2)
            self.split.y = min(max(-2, self.split.y), self.height-2)

        def _update(self, editor, X, Y):
            self.set_editor(editor)
            self.screen = pygame.Surface((self.width, self.height))
            self.screen.fill((0, 0, 0))
            
            if self.split_visible:
                self.aside._update(self.parent, 0, 0)
            
            self.main_area._update(self.parent, 0, 0)
            
            self.split._update(self.parent, 0, 0)

            editor.screen.blit(self.screen, (X+self.x, Y+self.y))
            if self.split.hovered and self.split_draggable:
                editor.screen.fill((0, 0, 0), (X+self.x+self.split.x, Y+self.y+self.split.y, self.split.width, self.split.height))
            elif self.split_type in [Collapsable.SplitType.VERTICAL_LEFT, Collapsable.SplitType.VERTICAL_RIGHT]:
                editor.screen.fill((0, 0, 0), (X+self.x+self.split.x+2, Y+self.y+self.split.y, 1, self.split.height))
            elif self.split_type in [Collapsable.SplitType.HORIZONTAL_TOP, Collapsable.SplitType.HORIZONTAL_BOTTOM]:
                editor.screen.fill((0, 0, 0), (X+self.x+self.split.x, Y+self.y+self.split.y+2, self.split.width, 1))

    def __init__(self, x:int, y:int, width:int, height:int, main_content:list=[], side_content:list=[], **options): # pylint: disable=dangerous-default-value
        """
        options:\n
        `split_type`: SplitType\n
            default: SplitType.VERTICAL_LEFT (vertical/horizontal refers to orientation of split line, left/top/... referes to location of main content)\n
        `split_size`: int\n
            default: width/2 (or height/2)\n
            this is where the split starts, this split line is draggable unless disabled\n
        `split_min`: int\n
            default: 1\n
            if the user drags the split below this width/height, it will snap to 0 when the user lets go\n
        `split_draggable`: bool\n
            default: True\n
        `split_visible`: bool\n
            default: True\n
            if False, the main section will take the whole area, with the side section closed\n

        Attributes: (that you can access/modify)\n
        main_area: Scrollable\n
        aside: Scrollable\n
        x: int\n
        y: int\n
        width: int\n
        height: int\n
        """
        super().__setattr__("_fake_editor", None)
        super().__setattr__("_collapsable", Collapsable._Collapsable(self, x, y, width, height, main_content, side_content, **options))
    def __getattribute__(self, __name: str):
        if __name == "_fake_editor":
            return super().__getattribute__("_fake_editor")
        elif __name == "Width":
            cx = getattr(super().__getattribute__("_collapsable"), "x")
            cw = getattr(super().__getattribute__("_collapsable"), "width")
            if hasattr(super().__getattribute__("_fake_editor"), "x"):
                fx = getattr(super().__getattribute__("_fake_editor"), "x")
            else: fx = 0
            if hasattr(super().__getattribute__("_fake_editor"), "get_width"):
                fw = getattr(super().__getattribute__("_fake_editor"), "get_width")()
            else: fw = getattr(super().__getattribute__("_fake_editor"), "width")
            if fx + fw <= fx + cx + cw: return fw - cx
            return cw
        elif __name == "Height":
            cx = getattr(super().__getattribute__("_collapsable"), "y")
            cw = getattr(super().__getattribute__("_collapsable"), "height")
            if hasattr(super().__getattribute__("_fake_editor"), "y"):
                fx = getattr(super().__getattribute__("_fake_editor"), "y")
            else: fx = 0
            if hasattr(super().__getattribute__("_fake_editor"), "get_height"):
                fw = getattr(super().__getattribute__("_fake_editor"), "get_height")()
            else: fw = getattr(super().__getattribute__("_fake_editor"), "height")
            if fx + fw <= fx + cx + cw: return fw - cx
            return cw
        elif __name == "X":
            return max(0, getattr(super().__getattribute__("_collapsable"), "x"))
        elif __name == "Y":
            return max(0, getattr(super().__getattribute__("_collapsable"), "y"))
        elif __name == "_collapsable":
            return super().__getattribute__("_collapsable")
        elif hasattr(super().__getattribute__("_collapsable"), __name):
            return getattr(super().__getattribute__("_collapsable"), __name)
        elif hasattr(super().__getattribute__("_fake_editor"), __name):
            return getattr(super().__getattribute__("_fake_editor"), __name)
        else:
            raise AttributeError
    def __setattr__(self, __name: str, __value) -> None:
        if __name == "_editor":
            super().__setattr__("_fake_editor", __value)
        elif hasattr(super().__getattribute__("_collapsable"), __name):
            setattr(super().__getattribute__("_collapsable"), __name, __value)
        elif hasattr(super().__getattribute__("_fake_editor"), __name):
            setattr(super().__getattribute__("_fake_editor"), __name, __value)
        else:
            setattr(super().__getattribute__("_collapsable"), __name, __value)

class NumberedTextArea(UIElement):

    class Fold:
        def __init__(self, lines:list):
            self.lines = lines

    def __init__(self, x:int, y:int, width:int, height:int, text_color:Color|tuple|int=TEXT_COLOR, text_bg_color:Color|Image|Animation|tuple|int=TEXT_BG_COLOR):
        assert width >= 200, "width must be 200 or more (sorry)"
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text_color = Color.color(text_color)
        self.text_bg_color = Color.color(text_bg_color)
        self.lines = MultilineText(0, 0, 75, self.height, f"{'1': >9}", self.text_color, self.text_bg_color)
        self.editable = MultilineTextBox(5, 0, self.width-75, self.height, "", self.text_color, self.text_bg_color)

        self.collapsable = Collapsable(
            self.x, self.y,
            self.width, self.height,
            [
                self.editable
            ],
            [
                self.lines
            ],
            split_type=Collapsable.SplitType.VERTICAL_RIGHT,
            split_draggable=False,
            split_size=75
        )

        self.collapsable.main_area.left_bound = 0
        self.collapsable.main_area.top_bound = 0
        self.collapsable.aside.left_bound = 0
        self.collapsable.aside.top_bound = 0
        self.collapsable.aside.right_bound = 0

    def _update(self, editor, X, Y):
        self.collapsable._update(editor, X, Y)
        
    def _event(self, editor, X, Y):
        self.collapsable._event(editor, X, Y)

        if self.collapsable.main_area.hovered:
            self.collapsable.aside.offsetY = self.collapsable.main_area.offsetY
        if self.collapsable.aside.hovered:
            self.collapsable.main_area.offsetY = self.collapsable.aside.offsetY

        lines = len(self.collapsable.main_area.children[0].get_lines())

        txt = [f"{i+1: >9}" for i in range(lines)]
        self.collapsable.aside.children[0].set_content("\n".join(txt))

        # if lines == 0:
        #     raise Exception("Numbered Text Editor reached 0 lines, which is meant to be impossible!!")

        d = self.collapsable.main_area.children[0].surfaces[0].get_height()

        self.collapsable.main_area.bottom_bound = -d * (lines-1)
        self.collapsable.aside.bottom_bound = -d * (lines-1)

class Tie(UIElement):

    @classmethod
    def group(cls, ties):
        ret = []
        for g in ties:
            ret.append(cls(g[0], g[1], g[2] if len(g) == 3 else True))
        return ret

    def __init__(self, controller, child, size_only=True):
        self.controller = controller
        self.child = child
        self.size_only = size_only

    def _update(self, editor, X, Y): # pylint: disable=unused-argument
        ...
    def _event(self, editor, X, Y): # pylint: disable=unused-argument
        if not self.size_only:
            if hasattr(self.controller, "get_x"):
                self.child.x = self.controller.get_x()
            elif hasattr(self.controller, "x"):
                self.child.x = self.controller.x
            
            if hasattr(self.controller, "get_y"):
                self.child.y = self.controller.get_y()
            elif hasattr(self.controller, "y"):
                self.child.y = self.controller.y

        if hasattr(self.controller, "get_width"):
            self.child.width = self.controller.get_width()
        elif hasattr(self.controller, "width"):
            self.child.width = self.controller.width

        if hasattr(self.controller, "get_height"):
            self.child.height = self.controller.get_height()
        elif hasattr(self.controller, "height"):
            self.child.height = self.controller.height

class ContextTree(UIElement):
    
    class Line: pass
    
    @classmethod
    def new(cls, x, y, width, height, label, *args, **kwargs) -> Button:
        """
        See ContextTree.__init__() for args/kwargs
        """
        _m = cls(*args, **kwargs)
        m = Button(x, y, width, height, label, hover_color=(50, 50, 50), click_color=(50, 50, 50))
        m.on_left_click = _m
        _m.parent = m
        m.children.append(_m)
        return m
    
    def __init__(self, tree_fields, width, option_height, text_color=TEXT_COLOR, bg_color=TEXT_BG_COLOR, line_color=(70, 70, 70), text_size=TEXT_SIZE, hover_color=TEXT_BG_COLOR, click_color=TEXT_BG_COLOR):
        self.visible = False
        self.width = width
        self.option_height = option_height
        self.text_color = text_color
        self.bg_color = bg_color
        self.line_color = line_color
        self.text_size = text_size
        self.hover_color = hover_color
        self.click_color = click_color
        self.tree = {}
        
        self.parent = None
        
        h = 0
        for obj in tree_fields:
            if isinstance(obj, ContextTree.Line):
                self.tree.update({h: Box(0, h, self.width, 1, self.line_color)})
                h += 1/2
            elif isinstance(obj, dict):
                for key, val in obj.items():
                    if val is None:
                        continue
                    b = Button(0, h, self.width, self.option_height, key, self.bg_color, self.text_color, self.text_size, self.hover_color, self.click_color)
                    b.on_left_click = val
                    if isinstance(val, UIElement):
                        b.children.append(val)
                        if isinstance(val, ContextTree):
                            val.parent = b
                    self.tree.update({h: b})
                    h += self.option_height/2

    def set_visibility(self, val:bool):
        self.visible = val
        if not val:
            for t in self.tree.values():
                if isinstance(t, Button):
                    for c in t.children:
                        if isinstance(c, ContextTree):
                            c.set_visibility(False)

    def toggle_visibility(self):
        self.visible = not self.visible
        if not self.visible:
            self.set_visibility(False)
    
    def __call__(self, *_, **__):
        self.toggle_visibility()
    
    def _update(self, editor, X, Y):
        if self.visible:
            for h, t in self.tree.items():
                _x = self.parent.width if X + self.parent.width + self.width < editor.width else -t.width
                t._update(editor, X + _x, Y + h)
    
    def _event(self, editor, X, Y):
        if self.visible:
            for h, t in self.tree.items():
                _x = self.parent.width if X + self.parent.width + self.width < editor.width else -t.width
                t._event(editor, X + _x, Y + h)

class Editor:
    def __init__(self, width=1280, height=720) -> None:
        self.screen:pygame.Surface = None
        # self.window = Window.from_display_module()
        self.previous_mouse = [False, False, False]
        self.mouse = [False, False, False]
        self.mouse_pos = (0, 0)
        self.previous_keys = []
        # self.keys = []
        # self.new_keys = []
        # self.old_keys = []
        self.override_cursor = False
        self.running = True
        self._updates = []
        self.layers = {0: []}
        self.scroll = 0
        self.width = self.Width = width
        self.height = self.Height = height
        self.x = self.X = 0
        self.y = self.Y = 0
        self._fake_editor = self
        self._focused_object = None
        self._hovered = False

        self.unicodes = {
            pygame.K_UP: "$↑",
            pygame.K_DOWN: "$↓",
            pygame.K_RIGHT: "$→",
            pygame.K_LEFT: "$←"
        }
        self.unicode = {}
        self.keys = []
        self.typing = []

    # def set_window_location(self, x, y):
    #     if int(time.time() % 5) == 0:
    #         # window = Window.from_display_module()
    #         # window.position = (x, y)
    #         os.environ["SDL_VIDEO_WINDOW_POS"] = f"{x},{y}"
            
    #         pygame.display.set_mode((self.width+1, self.height))
    #         self.screen = pygame.display.set_mode((self.width, self.height))

    def set_window_location(self, new_x, new_y):
        # print("position?")
        hwnd = pygame.display.get_wm_info()['window']
        windll.user32.MoveWindow(hwnd, int(new_x), int(new_y), int(self.width), int(self.height), False)

    def left_mouse_down(self): return (self.previous_mouse[0] is False) and (self.mouse[0] is True)
    def left_mouse_up(self): return (self.previous_mouse[0] is True) and (self.mouse[0] is False)
    def middle_mouse_down(self): return (self.previous_mouse[1] is False) and (self.mouse[1] is True)
    def middle_mouse_up(self): return (self.previous_mouse[1] is True) and (self.mouse[1] is False)
    def right_mouse_down(self): return (self.previous_mouse[2] is False) and (self.mouse[2] is True)
    def right_mouse_up(self): return (self.previous_mouse[2] is True) and (self.mouse[2] is False)
    # def queue_update(self, obj): self._updates.append(obj)

    def collides(self, mouse, rect) -> bool:
        mx, my = mouse
        x, y, w, h = rect
        #print(f"Editor: \033[38;2;20;200;20m{mouse} \033[38;2;200;200;20m{rect}\033[0m")
        if x <= mx <= x + w and y <= my <= y + h:
            return True
        return False

    def cancel_mouse_event(self):
        self.previous_mouse = self.mouse.copy()

    def add_layer(self, layer:int, *content):
        if not layer in [*self.layers]:
            self.layers.update({layer: []})
        for c in content:
            self.layers[layer].append(c)

    def run(self):
        #pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE | pygame.NOFRAME) # pylint: disable=no-member

        while self.running:
            self.screen.fill((255, 255, 255))
            self.previous_keys = self.keys.copy()
            self.previous_mouse = self.mouse
            self._hovered = False
            self.mouse = list(pygame.mouse.get_pressed())
            self.mouse_pos = pygame.mouse.get_pos()
            # self.new_keys.clear()
            # self.old_keys.clear()
            self.width, self.height = self.Width, self.Height = self.screen.get_size()

            self.typing.clear()

            self.scroll = 0
            for event in pygame.event.get():
                if event.type == pygame.MOUSEWHEEL: # pylint: disable=no-member
                    self.scroll = event.y
                elif event.type == pygame.KEYDOWN: # pylint: disable=no-member
                    if event.key not in self.keys:
                        self.keys.append(event.key)
                    un = self.unicodes.get(event.key, event.unicode)
                    if un:
                        self.unicode.update({un: time.time()})
                        self.typing.append(un)
                    # self.new_keys.append(event.unicode or event.key)
                    # self.keys.append(event.key)
                elif event.type == pygame.KEYUP: # pylint: disable=no-member
                    if event.key in self.keys:
                        self.keys.remove(event.key)
                    un = self.unicodes.get(event.key, event.unicode)
                    if un and un in self.unicode.keys():
                        self.unicode.pop(un)
                elif event.type == pygame.QUIT: # pylint: disable=no-member
                    pygame.quit() # pylint: disable=no-member
                    self.running = False
                    return

            nt = time.time()
            for key, t in self.unicode.items():
                if (nt - t) > 0.8:
                    if int(((nt - t) * 1000) % 10) == 0:
                        self.typing.append(key)

            layers = [*self.layers.keys()]
            layers.sort()

            for l in layers:
                for i in self.layers[l]:
                    i._update(self, 0, 0)

            _layers = layers.copy()
            _layers.reverse()
            for l in _layers:
                _l = self.layers[l].copy()
                _l.reverse()
                for i in _l:
                    i._event(self, 0, 0)

            #self.screen.fill((255, 0, 0), (self.mouse_pos[0]-1, self.mouse_pos[1]-1, 3, 3))

            pygame.display.update()

class CodeEditor(UIElement):
    
    def __init__(self, width, height):
        self.resolution = [width, height]
        self.children = []
        self.hover_color = (50, 50, 50)
        self.click_button = (70, 70, 70)
        self.ctx_tree_opts = (20, TEXT_COLOR, TEXT_BG_COLOR, (70, 70, 70), TEXT_SIZE, (50, 50, 50), (50, 50, 50))
        
        self._recent_window_pos = (int((1920 - (1920*2/4))/2), int((1080 - (1080*2/4))/2))
        # print(self._recent_window_pos)
        self._recent_window_size = (1920*2/4, 1080*2/4)
        
        # Apps:
        # The Game
        # Text Editor
        
        # Console
        
        
        self.active_app = ""
        
        self.window_drag_offset = None
        self.selected_drag = ""
        self.drag_offset = 0
        
        self.top_bar = Box(0, 0, width, 20, Color(24, 24, 24))
        self.children.append(self.top_bar)
        
        
        self.top_bar_icon = Image(f"{PATH}/dungeon_game_icon.png", 2, 2, 16, 16)
        self.children.append(self.top_bar_icon)
        
        self.top_bar_file = ContextTree.new(
            20, 0, 40, 20, "File", [
                {
                    "New File...": self.top_bar_file_new_file
                },
                ContextTree.Line(),
                {
                    "Open File...": self.top_bar_file_open_file,
                    "Open Folder...": self.top_bar_file_open_folder
                },
                ContextTree.Line(),
                {
                    "Save": self.top_bar_file_save,
                    "Save All": self.top_bar_file_save_all
                },
                ContextTree.Line(),
                {
                    "Exit": self.top_bar_file_exit
                }
            ], 115, *self.ctx_tree_opts
        )
        self.top_bar_file._uoffx = -self.top_bar_file.width
        self.top_bar_file._uoffy = self.top_bar_file.height
        self.children.append(self.top_bar_file)

        self.top_bar_edit = ContextTree.new(
            60, 0, 40, 20, "Edit", [
                {
                    "Undo": self.top_bar_edit_undo,
                    "Redo": self.top_bar_edit_redo
                },
                ContextTree.Line(),
                {
                    "Cut": self.top_bar_edit_cut,
                    "Copy": self.top_bar_edit_copy,
                    "Paste": self.top_bar_edit_paste
                },
                ContextTree.Line(),
                {
                    "Find": self.top_bar_edit_find,
                    "Replace": self.top_bar_edit_replace
                }
            ], 60, *self.ctx_tree_opts
        )
        self.top_bar_edit._uoffx = -self.top_bar_edit.width
        self.top_bar_edit._uoffy = self.top_bar_edit.height
        self.children.append(self.top_bar_edit)

        ctx_file_onclick = self.top_bar_file.on_left_click
        def ctx_file(*_, **__):
            self.top_bar_edit.children[0].set_visibility(False)
            ctx_file_onclick(*_, **__)
        self.top_bar_file.on_left_click = ctx_file

        ctx_edit_onclick = self.top_bar_edit.on_left_click
        def ctx_edit(*_, **__):
            self.top_bar_file.children[0].set_visibility(False)
            ctx_edit_onclick(*_, **__)
        self.top_bar_edit.on_left_click = ctx_edit

        self.minimize_button = Button(width-(26*3), 0, 26, 20, " ─ ", (24, 24, 24), hover_color=(70, 70, 70))
        self.minimize_button.on_left_click = self.minimize
        self.children.append(self.minimize_button)

        self._is_fullscreen = False
        self._fullscreen = Image(f"{PATH}/full_screen.png", 0, 0, 26, 20)
        self._fullscreen_hovered = Image(f"{PATH}/full_screen_hovered.png", 0, 0, 26, 20)
        self._shrinkscreen = Image(f"{PATH}/shrink_window.png", 0, 0, 26, 20)
        self._shrinkscreen_hovered = Image(f"{PATH}/shrink_window_hovered.png", 0, 0, 26, 20)

        self.fullscreen_toggle = Button(width-(26*2), 0, 26, 20, "", self._fullscreen, hover_color=self._fullscreen_hovered)
        self.fullscreen_toggle.on_left_click = self.toggle_fullscreen
        self.children.append(self.fullscreen_toggle)
        self._close = Image(f"{PATH}/close_button.png", 0, 0, 26, 20)
        self._close_hovered = Image(f"{PATH}/close_button_hovered.png", 0, 0, 26, 20)
        self.close_button = Button(width-26, 0, 26, 20, "", self._close, hover_color=self._close_hovered)
        self.close_button.on_left_click = self.close_window
        self.children.append(self.close_button)

        self.bottom_drag = Box(5, height-5, width-10, 5, (24, 24, 24))
        self.children.append(self.bottom_drag)

        self.bottom_right_drag = Box(width-5, height-5, 5, 5, (24, 24, 24))
        self.children.append(self.bottom_right_drag)
        
        self.bottom_left_drag = Box(0, height-5, 5, 5, (24, 24, 24))
        self.children.append(self.bottom_left_drag)
        
        self.left_drag = Box(0, 20, 5, height-25, (24, 24, 24))
        self.children.append(self.left_drag)
        
        self.right_drag = Box(width-5, 20, 5, height-25, (24, 24, 24))
        self.children.append(self.right_drag)

        self.top_bar_line = Box(0, 20, width, 1, (70, 70, 70))
        self.children.append(self.top_bar_line)
        
        self.bottom_bar = Box(5, height-20, width-10, 15, (24, 24, 24))
        self.children.append(self.bottom_bar)
        
        self.bottom_bar_line = Box(0, height-21, width, 1, (70, 70, 70))
        self.children.append(self.bottom_bar_line)

        self.app_bar = Box(5, 21, 45, height-42, (24, 24, 24))
        self.children.append(self.app_bar)




    def minimize(self, *_, **__):
        pygame.display.iconify()

    def get_screen_pos(self, editor):
        mx, my = mouse.get_position()
        rx, ry = editor.mouse_pos
        # print(f"mouse: ({mx}, {my}) -> ({rx}, {ry})  ({mx-rx}, {my-ry})")
        return mx-rx, my-ry

    def set_fullscreen(self, editor):
        monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
        work_area = monitor_info.get("Work")
        editor.width, editor.height = work_area[2:4]
        editor.set_window_location(0, 0)
        
        self._update_layout(editor)

    def toggle_fullscreen(self, editor):
        if self._is_fullscreen:
            self.fullscreen_toggle.bg_color = self.fullscreen_toggle._bg_color = self._fullscreen
            self.fullscreen_toggle.hover_color = self._fullscreen_hovered
            editor.width, editor.height = self._recent_window_size
            self.top_bar.hovered = False
            self.window_drag_offset = None
            # editor.mouse[0] = editor.previous_mouse[0] = False
            # editor.set_window_location(-1920, -1080)
            editor.set_window_location(*self._recent_window_pos)
            
            # print(self._recent_window_pos)
            self._update_layout(editor)
        else:
            self.fullscreen_toggle.bg_color = self.fullscreen_toggle._bg_color = self._shrinkscreen
            self.fullscreen_toggle.hover_color = self._shrinkscreen_hovered
            self.top_bar.hovered = False
            self.window_drag_offset = None
            self._recent_window_pos = self.get_screen_pos(editor)
            self._recent_window_size = (editor.width, editor.height)
            self.set_fullscreen(editor)
            # editor.mouse[0] = False
            # editor.previous_mouse[0] = False
        self._is_fullscreen = not self._is_fullscreen

    def close_window(self, editor):
        editor.running = False
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def top_bar_file_new_file(self, *_, **__):
        ...
    def top_bar_file_open_file(self, *_, **__):
        ...
    def top_bar_file_open_folder(self, *_, **__):
        ...
    def top_bar_file_save(self, *_, **__):
        ...
    def top_bar_file_save_all(self, *_, **__):
        ...
    def top_bar_file_exit(self, *_, **__):
        ...
    def top_bar_edit_undo(self, *_, **__):
        ...
    def top_bar_edit_redo(self, *_, **__):
        ...
    def top_bar_edit_cut(self, *_, **__):
        ...
    def top_bar_edit_copy(self, *_, **__):
        ...
    def top_bar_edit_paste(self, *_, **__):
        ...
    def top_bar_edit_find(self, *_, **__):
        ...
    def top_bar_edit_replace(self, *_, **__):
        ...

    def _update(self, editor, X, Y):
        for child in self.children:
            child._update(editor, X, Y)

    def _update_layout(self, editor):
        
        pygame.display.set_mode((editor.width, editor.height), pygame.RESIZABLE | pygame.NOFRAME)
        
        self.top_bar.width = editor.width
        self.bottom_drag.width = editor.width-10
        self.bottom_drag.y = self.bottom_left_drag.y = self.bottom_right_drag.y = editor.height-5
        self.bottom_right_drag.x = self.right_drag.x = editor.width-5
        self.right_drag.height = self.left_drag.height = editor.height - 25
        self.bottom_bar_line.y = editor.height-21
        self.bottom_bar_line.width = self.top_bar_line.width = editor.width
        self.bottom_bar.width = editor.width-10
        self.bottom_bar.y = editor.height-20
        
        self.app_bar.height = editor.height - 42
        
        self.minimize_button.x = editor.width - (26*3)
        self.fullscreen_toggle.x = editor.width - (26*2)
        self.close_button.x = editor.width - 26

    def _event(self, editor:Editor, X, Y):
        if (self.top_bar.hovered and editor.mouse[0] and (not editor.previous_mouse[0])):
            self.window_drag_offset = editor.mouse_pos
        elif (editor.mouse[0] and self.window_drag_offset):
            x, y = mouse.get_position()
            x -= self.window_drag_offset[0]
            y -= self.window_drag_offset[1]
            editor.set_window_location(x, y)
        elif (not editor.mouse[0]) and editor.previous_mouse[0]:
            x, y = mouse.get_position()
            
            if y == 0:
                self._is_fullscreen = True
                self._recent_window_size = (editor.width, editor.height)
                self._recent_window_pos = self.get_screen_pos(editor)
                
                self.set_fullscreen(editor)
            
            self.window_drag_offset = None

        rmx, rmy = mouse.get_position()
        rsx, rsy = self.get_screen_pos(editor)

        if self.bottom_drag.hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)
            
            if editor.mouse[0] and (not editor.previous_mouse[0]):
                self.selected_drag = "bottom_drag"
            
        elif self.left_drag.hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
            
            if editor.mouse[0] and (not editor.previous_mouse[0]):
                self.selected_drag = "left_drag"
                self.drag_offset = (rsx + editor.width, rsy)
                
        elif self.right_drag.hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
            
            if editor.mouse[0] and (not editor.previous_mouse[0]):
                self.selected_drag = "right_drag"
            
        elif self.bottom_left_drag.hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENESW)
            if editor.mouse[0] and (not editor.previous_mouse[0]):
                self.selected_drag = "bottom_left_drag"
                self.drag_offset = (rsx + editor.width, rsy)
        elif self.bottom_right_drag.hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENWSE)
            if editor.mouse[0] and (not editor.previous_mouse[0]):
                self.selected_drag = "bottom_right_drag"
        elif not editor.override_cursor:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if self.selected_drag in ["bottom_drag", "bottom_right_drag", "bottom_left_drag"]:
            # print(rmy, rsy, rmy-rsy)
            editor.height = max(100, rmy - rsy)
            self._update_layout(editor)
        if self.selected_drag in ["left_drag", "bottom_left_drag"]:
            editor.set_window_location(min (rmx, self.drag_offset[0]-100), self.drag_offset[1])
            editor.width = max(100, self.drag_offset[0] - rmx)
            self._update_layout(editor)
        if self.selected_drag in ["right_drag", "bottom_right_drag"]:
            editor.width = max(100, rmx - rsx)
            self._update_layout(editor)


        if (not editor.mouse[0]) and editor.previous_mouse[0]:
            self.selected_drag = ""

        for child in self.children:
            child._event(editor, X, Y)

if __name__ == "__main__":
    from threading import Thread
    import traceback

    editor = Editor()
    
    def inp_thread():
        while not editor.running: pass
        while editor.running:
            inp = input("> ")
            if inp:
                try:
                    exec(inp)
                except Exception as e:
                    print("\n".join(traceback.format_exception(e)))
    i = Thread(target=inp_thread)
    i.start()
    
    c = CodeEditor(editor.width, editor.height)

    # drag_box = Draggable(20, 20, 50, 50)
    # drag_box.children.append(
    #     Box(0, 0, 50, 50, (0, 127, 200))
    # )
    # editor.layers[0].append(drag_box)

    # class Console(TextBox):
    #     def on_enter(self, text:str):
    #         try:
    #             exec(text)
    #         except Exception as e:
    #             print("\n".join(traceback.format_exception(e)))
    #         self.set_content()
    #         self.focused = True

    # c = NumberedTextArea(20, 20, 400, 400)

    # c.editable.set_content("This is a test, using a long\npiece of text\nbecause yeah\n:D")

    # b = Resizable(20, 20, 40, 40, (127, 200, 200), 40, 40)

    # def pre_print(*args, **kwargs):
    #     def idk(*_, **__):
    #         print(*args, **kwargs)
    #     return idk

    # ctx_tree_opts = (100, 20, TEXT_COLOR, TEXT_BG_COLOR, (70, 70, 70), TEXT_SIZE, (50, 50, 50), (50, 50, 50))

    # m = ContextTree.new(50, 50, 100, 20, [
    #     {
    #         "option 1": pre_print("Hello"),
    #         "option 2": pre_print("World!")
    #     },
    #     ContextTree.Line(),
    #     {
    #         "option 3": ContextTree([
    #             {
    #                 "sub opt 3.1": pre_print("owo"),
    #                 "sub opt 3.2": pre_print("idk")
    #             }
    #         ], *ctx_tree_opts)
    #     }
    # ], *ctx_tree_opts)


    # # a = Animation(50, 50, sprite_sheet=f"{PATH}/gray_scale.png", sprite_width=1, sprite_height=1, fps=5, resize=(20, 20))

    # t = Tabs(
    #     0, 20, 800, 400,
    #     tab_data={
    #         "Text Editor": [c],
    #         "Test": [b],
    #         "context menu": [m]
    #     },
    #     tab_color_unselected=(20, 20, 20),
    #     tab_color_hovered=(26, 26, 26),
    #     tab_color_selected=(31, 31, 31),
    #     tab_color_empty=(18, 18, 18),
    #     tab_height=20,
    #     content_bg_color=(31, 31, 31),
    #     scrollable_tabs=True
    # )

    editor.layers[0] += [
        #MultilineText(0, 0, 400, 200, "h\nh\nh\nh\nh"),
        c#t,#c,
        #Console(2, 2, 200, "\"console\"")
    ]

    # # editor.add_layer(2, a)

    # #editor.add_layer(10, Console(2, 2, 400))

    editor.run()

