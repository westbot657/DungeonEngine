# pylint: disable=[W,R,C,no-member]

try:
    from GraphicsEngine.PlatformDependencies import gw, macOSfocusWindow, macOSgetWindowPos, macOSsetWindow
    from GraphicsEngine.Options import PATH, TEXT_BG3_COLOR
    from GraphicsEngine.Popup import Popup
    from GraphicsEngine.ContextTree import ContextTree
    from GraphicsEngine.SnapNode import SnapNode
    from GraphicsEngine.MultilineText import MultilineText
    from GraphicsEngine.MultilineTextBox import MultilineTextBox
    from GraphicsEngine.TextBox import TextBox
    from GraphicsEngine.FunctionalElements import Button
    from GraphicsEngine.Text import Text
except ImportError:
    from PlatformDependencies import gw, macOSfocusWindow, macOSgetWindowPos, macOSsetWindow
    from Options import PATH, TEXT_BG3_COLOR
    from Popup import Popup
    from ContextTree import ContextTree
    from SnapNode import SnapNode
    from MultilineText import MultilineText
    from MultilineTextBox import MultilineTextBox
    from TextBox import TextBox
    from FunctionalElements import Button
    from Text import Text


import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pygame.time import Clock

import platform
import time
from array import array

pygame.init()

class Editor:

    def __init__(self, engine, io_hook, width=1280, height=720) -> None:
        self.screen:pygame.Surface = None
        self.engine = engine
        self.io_hook = io_hook
        
        self.ctx = None
        self.quad_buffer = None
        
        self.game_app = None
        self.previous_mouse = [False, False, False]
        self.mouse = [False, False, False]
        self.mouse_pos = (0, 0)
        self.previous_keys = []
        self.override_cursor = False
        self.running = True
        self._updates = []
        self.layers = {0: []}
        self.scroll = 0
        self.width = self.Width = width
        self.height = self.Height = height
        self.held = None
        self.x = self.X = 0
        self.y = self.Y = 0
        self._fake_editor = self
        self._focused_object = None
        self._hovered = False
        self._hovering = None
        self._hovering_last = None
        self._hover_time = 0
        self._hovering_ctx_tree = False
        self._listeners = {}
        self._caption = "Insert Dungeon Name Here"
        self._alt = None
        self._alt_border = None
        self._alt_pos = (0, 0)
        self._frame = 0
        self.unicodes = {
            pygame.K_UP: "$↑",
            pygame.K_DOWN: "$↓",
            pygame.K_RIGHT: "$→",
            pygame.K_LEFT: "$←"
        }
        self.unicode = {}
        self.keys = []
        self.typing = []
        self._do_layout_update = False

    def add_event_listener(self, event, listener):
        # print(f"ADDING EVENT: {event} :: {listener}")
        if event not in self._listeners:
            self._listeners.update({event: []})
        
        self._listeners[event].append(listener)

    def set_window_location(self, new_x, new_y): # This function also causes a window size change
        self._do_layout_update = True
        if platform.system() in ["Windows", "Linux"]:
            window = gw.getWindowsWithTitle(self._caption)[0]
            if window is not None:
                window.moveTo(int(new_x), int(new_y))
                window.resizeTo(self.width, self.height)
        elif platform.system() == "Darwin":
            macOSsetWindow(self._caption, int(new_x), int(new_y), self.width, self.height)

    def left_mouse_down(self): return (self.previous_mouse[0] is False) and (self.mouse[0] is True)

    def left_mouse_up(self): return (self.previous_mouse[0] is True) and (self.mouse[0] is False)

    def middle_mouse_down(self): return (self.previous_mouse[1] is False) and (self.mouse[1] is True)

    def middle_mouse_up(self): return (self.previous_mouse[1] is True) and (self.mouse[1] is False)

    def right_mouse_down(self): return (self.previous_mouse[2] is False) and (self.mouse[2] is True)

    def right_mouse_up(self): return (self.previous_mouse[2] is True) and (self.mouse[2] is False)

    def collides(self, mouse, rect) -> bool:
        mx, my = mouse
        x, y, w, h = rect

        if x <= mx < x + w and y <= my < y + h:
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
        # print(f"making window of size: ({self.width}, {self.height})")
        
        
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE | pygame.NOFRAME) # pylint: disable=no-member
        
        
        pygame.display.set_icon(pygame.image.load(f"{PATH}/dungeon_game_icon.png"))
        pygame.display.set_caption(self._caption)
        self.clock = Clock()

        # _fps = time.time()
        # fps = _fps
        
        if platform.system() in ["Windows", "Linux"]:
            window = gw.getWindowsWithTitle(self._caption)[0]
            if window is not None:
                window.alwaysOnTop(True)
                window.alwaysOnTop(False)
        elif platform.system() == "Darwin":
            macOSfocusWindow(self._caption)
        
        # fps_display = Text(0, 0, 1, f"{fps}", text_size=10)

        while self.running:
            self.clock.tick(120)
            self.screen.fill((24, 24, 24))
            self.previous_keys = self.keys.copy()
            self.previous_mouse = self.mouse
            self._hovered = False
            # self._hovering_last = self._hovering
            self._hovering = None
            self._hovering_ctx_tree = False
            self.mouse = list(pygame.mouse.get_pressed()) #[mouse.is_pressed(mouse.LEFT), mouse.is_pressed(mouse.MIDDLE), mouse.is_pressed(mouse.RIGHT)]#list(a and b for a, b in zip(pygame.mouse.get_pressed(), ))
            self.mouse_pos = pygame.mouse.get_pos()
            self.width, self.height = self.Width, self.Height = self.screen.get_size()
            self.typing.clear()
            self.scroll = 0
            # self._frame += 1
            # if self._frame >= 100:
            #     self._frame = 1

            # _fps = fps
            # fps = time.time()

            for event in pygame.event.get():

                if event.type == pygame.MOUSEWHEEL: # pylint: disable=no-member
                    self.scroll = event.y
                    
                if event.type == pygame.MOUSEMOTION:
                    self._alt = None

                elif event.type == pygame.KEYDOWN: # pylint: disable=no-member

                    if event.key not in self.keys:
                        self.keys.append(event.key)

                    un = self.unicodes.get(event.key, event.unicode)

                    if un:
                        self.unicode.update({un: time.time()})
                        self.typing.append(un)
                        
                elif event.type == pygame.KEYUP: # pylint: disable=no-member

                    if event.key in self.keys:
                        self.keys.remove(event.key)

                    un = self.unicodes.get(event.key, event.unicode)

                    if un and un in self.unicode.keys():
                        self.unicode.pop(un)

                elif event.type == pygame.QUIT: # pylint: disable=no-member
                    if "WINDOW_CLOSED" in self._listeners:
                        for listener in self._listeners.get("WINDOW_CLOSED", []):
                            listener()
                    else:
                        pygame.quit() # pylint: disable=no-member
                        self.running = False
                        return

            nt = time.time()

            for key, t in self.unicode.items():

                if (nt - t) > 0.8:

                    if int(((nt - t) * 1000) % 5) == 0:
                        self.typing.append(key)

            layers = [*self.layers.keys()]
            layers.sort()


            if Popup._popup:
                Popup._popup._update_layout(self)
                Popup._popup._event(self, 0, 0)

            ContextTree.event(self, 0, 0)

            for l in layers[::-1]:
                for i in self.layers[l][::-1]:
                    i._event(self, 0, 0)

            SnapNode.reset()

            lmd = self.left_mouse_down()
            rmd = self.right_mouse_down()
            if self._hovering is not None:
                # print(f"Hovering: {self._hovering}  alt: {getattr(self._hovering, "_alt_text", "")}")

                if self._hovering != self._hovering_last:
                    self._alt = None
                    self._hover_time = time.time()
                
                elif self._hover_time + 1.5 < time.time() < self._hover_time + 2.5 and (self._alt is None):
                    if alt := getattr(self._hovering, "_alt_text", None):
                        self._hover_time = 0 # this will make the alt text not follow the mouse between t=1.5 and t=2.5
                        self._alt = MultilineText(0, 0, 1, 14*(alt.count("\n")+1), alt)
                        self._alt_border = pygame.Surface((self._alt._text_width+4, self._alt._text_height+4))
                        self._alt_border.fill(TEXT_BG3_COLOR)
                        self._alt_pos = (self.mouse_pos[0], self.mouse_pos[1]-self._alt._text_height)

                if rmd:
                    if hasattr(self._hovering, "on_right_click") and not isinstance(self._hovering, Button):

                        try:
                            self._hovering.on_right_click(self, self._hovering)

                        except Exception as e:
                            print("\n".join(e.args))
            
                if isinstance(self._hovering, (TextBox, MultilineTextBox)):
                    self.override_cursor = True
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
                
                else:
                    self.override_cursor = False
            elif self.override_cursor:
                self.override_cursor = False
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
            self._hovering_last = self._hovering

            if (rmd or lmd):
                self._alt = None
                if not self._hovering_ctx_tree:
                    ContextTree.closeAll()

            for l in layers:

                for i in self.layers[l]:
                    i._update(self, 0, 0)

            ContextTree.update(self, 0, 0)

            if Popup._popup:
                Popup._popup._update(self, 0, 0)
            
            if self._alt:
                self.screen.blit(self._alt_border, (min(max(0, self._alt_pos[0]), self.width-self._alt_border.get_width())-2, min(max(0, self._alt_pos[1]), self.height-self._alt_border.get_height())-2))
                self._alt._update(self, min(max(0, self._alt_pos[0]), self.width-self._alt_border.get_width()), min(max(0, self._alt_pos[1]), self.height-self._alt_border.get_height()))

            # fps_display.set_text(f"{fps-_fps}")
            # fps_display._event(self, 5, self.height-10)
            # fps_display._update(self, 5, self.height-10)

            pygame.display.flip()


