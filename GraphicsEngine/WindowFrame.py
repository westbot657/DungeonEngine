# pylint: disable=[W,R,C, no-member]
try:
    from GraphicsEngine.UIElement import UIElement
    from GraphicsEngine.Geometry import Box
    from GraphicsEngine.RenderPrimitives import Color, Image
    from GraphicsEngine.Options import PATH
    from GraphicsEngine.Text import Text
    from GraphicsEngine.FunctionalElements import Button
    from GraphicsEngine.PlatformDependencies import gw, macOSfocusWindow, macOSgetWindowPos, macOSsetWindow, get_monitors
except ImportError:
    from UIElement import UIElement
    from Geometry import Box
    from RenderPrimitives import Color, Image
    from Options import PATH
    from Text import Text
    from FunctionalElements import Button
    from PlatformDependencies import gw, macOSfocusWindow, macOSgetWindowPos, macOSsetWindow, get_monitors


import platform
import sys
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from pynput.mouse import Controller

mouse = Controller()

class WindowFrame(UIElement):
    def __init__(self, width, height, editor, window_limits:list[int,int,int,int]=..., title=""):
        if window_limits is ...:
            window_limits = [800, 425, 1920, 1080]
        self.window_limits = window_limits
        self.resolution = [width, height]
        self.children = []
        self.editor = editor
        self.hover_color = (50, 50, 50)
        self.click_button = (70, 70, 70)
        self.window_drag_offset = None
        self.selected_drag = ""
        self.drag_offset = 0
        self._recent_window_pos = (int((1920 - (1920*2/4))/2), int((1080 - (1080*2/4))/2))
        self._recent_window_size = (1920*2/4, 1080*2/4)
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
        self.top_bar = Box(0, 0, width, 20, Color(24, 24, 24))
        self.children.append(self.top_bar)
        self.top_bar_icon = Image(f"{PATH}/dungeon_game_icon.png", 2, 2, 16, 16)
        self.children.append(self.top_bar_icon)
        
        # print(f"TITLE: {title}")
        self.title = Text(20, 2, content=title, text_size=13)
        self.children.append(self.title)
        
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

    def minimize(self, *_, **__):
        # RPC.update(details="Made the window smol 4 some reason", state="¯\_(ツ)_/¯")
        pygame.display.iconify()

    def get_screen_pos(self, editor):
        if platform.system() in ["Windows", "Linux"]:
            window = gw.getWindowsWithTitle(self.editor._caption)[0]
            if window is not None:
                return window.left, window.top
            return self._recent_window_pos
        elif platform.system() == "Darwin":
            return macOSgetWindowPos(self.editor._caption)

    def set_fullscreen(self, editor):
        screen = get_monitors()[0]
        editor.width, editor.height = screen.width, screen.height
        editor.set_window_location(0, 0)
        self._update_layout(editor)
        editor._do_layout_update = True

    def toggle_fullscreen(self, editor):

        if self._is_fullscreen:
            self.fullscreen_toggle.bg_color = self.fullscreen_toggle._bg_color = self._fullscreen
            self.fullscreen_toggle.hover_color = self._fullscreen_hovered
            editor.width, editor.height = self._recent_window_size
            self.top_bar.hovered = False
            self.window_drag_offset = None
            editor.set_window_location(*self._recent_window_pos)
            self._update_layout(editor)

        else:
            self.fullscreen_toggle.bg_color = self.fullscreen_toggle._bg_color = self._shrinkscreen
            self.fullscreen_toggle.hover_color = self._shrinkscreen_hovered
            self.top_bar.hovered = False
            self.window_drag_offset = None
            self._recent_window_pos = self.get_screen_pos(editor)
            self._recent_window_size = (editor.width, editor.height)
            self.set_fullscreen(editor)

        self._is_fullscreen = not self._is_fullscreen
        editor._do_layout_update = True

    def close_window(self, editor):
        
        if "WINDOW_CLOSED" in editor._listeners:
            for listener in editor._listeners["WINDOW_CLOSED"]:
                listener()
        else:
            editor.running = False
            if editor.engine:
                editor.engine.stop()
            pygame.display.quit()
            pygame.quit()
            sys.exit()

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
        self.minimize_button.x = editor.width - (26*3)
        self.fullscreen_toggle.x = editor.width - (26*2)
        self.close_button.x = editor.width - 26

    def _event(self, editor, X, Y):

        for child in self.children[::-1]:
            child._event(editor, X, Y)

        if (self.top_bar.hovered and editor.mouse[0] and (not editor.previous_mouse[0])):
            self.window_drag_offset = editor.mouse_pos

        elif (editor.mouse[0] and self.window_drag_offset):
            x, y = mouse.position#.get_position()
            x -= self.window_drag_offset[0]
            y -= self.window_drag_offset[1]
            editor.set_window_location(x, y)

        elif (not editor.mouse[0]) and editor.previous_mouse[0]:
            x, y = mouse.position#.get_position()
            
            if y == 0:
                self._is_fullscreen = False
                self.toggle_fullscreen(editor)
            
            self.window_drag_offset = None

        rmx, rmy = mouse.position#.get_position()
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
            editor.height = min(max(self.window_limits[1], rmy - rsy), self.window_limits[3])
            self._update_layout(editor)

        if self.selected_drag in ["left_drag", "bottom_left_drag"]:
            editor.set_window_location(min(rmx, self.drag_offset[0]-100), self.drag_offset[1])
            editor.width = min(max(self.window_limits[0], self.drag_offset[0] - rmx), self.window_limits[2])
            self._update_layout(editor)

        if self.selected_drag in ["right_drag", "bottom_right_drag"]:
            editor.width = min(max(self.window_limits[0], rmx - rsx), self.window_limits[2])
            self._update_layout(editor)

        if (not editor.mouse[0]) and editor.previous_mouse[0]:
            self.selected_drag = ""  
