# pylint: disable=W,R,C,no-member
# (C) Weston Day 2024
# pygame UI Library

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pygame.time import Clock

# useful utils
# from enum import Enum, auto
from mergedeep import merge
import time
import json
import re
import sys
import random
import Stockings
import socket
# import ast
# import webbrowser
import platform

from subprocess import Popen, PIPE, STDOUT
from threading import Thread

# 3D rendering
from shapely.geometry.polygon import Polygon as Poly

# used to import the game engine with code
# import importlib
from importlib.machinery import SourceFileLoader


# Things needed to move and resize pygame window
# import mouse
from pynput.mouse import Controller

from typing import Any

mouse = Controller()

# from pygame._sdl2.video import Window, Texture # pylint: disable=no-name-in-module

# import components
try:
    from GraphicsEngine.Options import client_id, DO_RICH_PRESENCE, PATH, \
        FONT, SETTINGS, TEXT_SIZE, TEXT_COLOR, TEXT_BG_COLOR, \
        TEXT_HIGHLIGHT, TAB_SIZE, POPOUTS, TEXT_BG2_COLOR, TEXT_BG3_COLOR
    from GraphicsEngine.Util import expand_text_lists, \
        rotate, rotate3D, rotate3DV, \
        quad_to_tris, invert_tris, \
        angle_between, warp, safe_eval, \
        Selection, Cursor, PopoutElement
    from GraphicsEngine.UIElement import UIElement
    from GraphicsEngine.RenderPrimitives import Color, Image, Animation
    from GraphicsEngine.EditorMimic import EditorMimic
    from GraphicsEngine.Text import Text
    from GraphicsEngine.MultilineText import MultilineText
    from GraphicsEngine.TextBox import TextBox
    from GraphicsEngine.MultilineTextBox import MultilineTextBox
    from GraphicsEngine.Geometry import Box, Polygon, Poly3D
    from GraphicsEngine.Organizers import LayeredObjects, Draggable, Resizable, Tie, Link
    from GraphicsEngine.FunctionalElements import Button, BorderedButton, Tabs, Scrollable, Collapsable, ProgressBar
    from GraphicsEngine.NumberedTextArea import NumberedTextArea
    from GraphicsEngine.PopoutInterface import PopoutInterface
    from GraphicsEngine.SnapNode import SnapNode
    from GraphicsEngine.DiscordPresence import RPC, RPCD
    from GraphicsEngine.ContextTree import ContextTree
    from GraphicsEngine.DirectoryTree import DirectoryTree
    from GraphicsEngine.Popup import Popup
    from GraphicsEngine.Editor import Editor
    from GraphicsEngine.GameApp import GameApp
    from GraphicsEngine.PlatformDependencies import gw, macOSfocusWindow, macOSgetWindowPos, macOSsetWindow, get_monitors
    from GraphicsEngine.FileEditor import FileEditor
    from GraphicsEngine.AttributePanel import AttributePanel
    from GraphicsEngine.ConstructionCanvas import ConstructionCanvas
    from GraphicsEngine.AdvancedEditorSubApp import AdvancedEditorSubApp
    from GraphicsEngine.FileEditorSubApp import FileEditorSubApp
    from GraphicsEngine.PopoutWindow import PopoutWindow
    from GraphicsEngine.EditorApp import EditorApp
except ImportError:
    from Options import client_id, DO_RICH_PRESENCE, PATH, \
        FONT, SETTINGS, TEXT_SIZE, TEXT_COLOR, TEXT_BG_COLOR, \
        TEXT_HIGHLIGHT, TAB_SIZE, POPOUTS, TEXT_BG2_COLOR, TEXT_BG3_COLOR
    from Util import expand_text_lists, \
        rotate, rotate3D, rotate3DV, \
        quad_to_tris, invert_tris, \
        angle_between, warp, safe_eval, \
        Selection, Cursor, PopoutElement
    from UIElement import UIElement
    from RenderPrimitives import Color, Image, Animation
    from EditorMimic import EditorMimic
    from Text import Text
    from MultilineText import MultilineText
    from TextBox import TextBox
    from MultilineTextBox import MultilineTextBox
    from Geometry import Box, Polygon, Poly3D
    from Organizers import LayeredObjects, Draggable, Resizable, Tie, Link
    from FunctionalElements import Button, BorderedButton, Tabs, Scrollable, Collapsable, ProgressBar
    from NumberedTextArea import NumberedTextArea
    from PopoutInterface import PopoutInterface
    from SnapNode import SnapNode
    from DiscordPresence import RPC, RPCD
    from ContextTree import ContextTree
    from DirectoryTree import DirectoryTree
    from Popup import Popup
    from Editor import Editor
    from GameApp import GameApp
    from PlatformDependencies import gw, macOSfocusWindow, macOSgetWindowPos, macOSsetWindow, get_monitors
    from FileEditor import FileEditor
    from AttributePanel import AttributePanel
    from ConstructionCanvas import ConstructionCanvas
    from AdvancedEditorSubApp import AdvancedEditorSubApp
    from FileEditorSubApp import FileEditorSubApp
    from PopoutWindow import PopoutWindow
    from EditorApp import EditorApp


pygame.init() # pylint: disable=no-member
pygame.font.init()

class CodeEditor(UIElement):
    
    def __init__(self, width, height, editor):
        self.resolution = [width, height]
        self.children = []
        self.editor = editor
        self.hover_color = (50, 50, 50)
        self.click_button = (70, 70, 70)
        self.ctx_tree_opts = (20, TEXT_COLOR, TEXT_BG_COLOR, (70, 70, 70), TEXT_SIZE, (50, 50, 50), (50, 50, 50))
        self._recent_window_pos = (int((1920 - (1920*2/4))/2), int((1080 - (1080*2/4))/2))
        self._recent_window_size = (1920*2/4, 1080*2/4)
        self.active_app = ""
        self.window_drag_offset = None
        self.selected_drag = ""
        self.drag_offset = 0
        self.app_bar = Box(5, 21, 45, height-42, (24, 24, 24))
        self.children.append(self.app_bar)
        self.app_line = Box(50, 21, 1, height-42, (70, 70, 70))
        self.children.append(self.app_line)
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
        self._error_message = MultilineText(25, 25, 1, 1, "", text_color=(255, 200, 200), text_bg_color=None)
        self._error_popup = Popup(400, 30).add_children(self._error_message)
        self._error_popup._update_layout = self._error_message_update_layout
        self._app_game_icon = Image(f"{PATH}/dungeon_game_app_icon.png", 0, 0, 50, 50)
        self._app_game_icon_hovered = Image(f"{PATH}/dungeon_game_app_icon_hovered.png", 0, 0, 50, 50)
        self._app_game_icon_selected = Image(f"{PATH}/dungeon_game_app_icon_selected.png", 0, 0, 50, 50)
        self.app_game_selector = Button(0, 22, 50, 50, "", self._app_game_icon, hover_color=self._app_game_icon_hovered, click_color=self._app_game_icon_selected)
        self.app_game_selector.on_left_click = self.select_game_app
        self.app_game_selector._alt_text = "IDNH Game Menu"
        self.children.append(self.app_game_selector)
        self._app_editor_icon = Image(f"{PATH}/dungeon_editor_app_icon.png", 0, 0, 50, 50)
        self._app_editor_icon_hovered = Image(f"{PATH}/dungeon_editor_app_icon_hovered.png", 0, 0, 50, 50)
        self._app_editor_icon_selected = Image(f"{PATH}/dungeon_editor_app_icon_selected.png", 0, 0, 50, 50)
        self.app_editor_selector = Button(0, 22+50, 50, 50, "", self._app_editor_icon, hover_color=self._app_editor_icon_hovered, click_color=self._app_editor_icon_selected)
        self.app_editor_selector.on_left_click = self.select_editor_app
        self.app_editor_selector._alt_text = "IDNH Dungeon Editor"
        self.children.append(self.app_editor_selector)
        self.top_bar = Box(0, 0, width, 20, Color(24, 24, 24))
        self.children.append(self.top_bar)
        self.top_bar_icon = Image(f"{PATH}/dungeon_game_icon.png", 2, 2, 16, 16)
        self.children.append(self.top_bar_icon)
        self.new_file_display = Text(25, 5, 1, "Enter new file path/name:", text_size=13)
        self.new_file_input_box = MultilineTextBox(25, 25, 350, 16, "", text_bg_color=(31, 31, 31))
        self.new_file_input_box.single_line = True
        self.new_file_input_box.on_enter(self.create_new_file)
        self.new_file_popup = Popup(400, 50).add_children(
            self.new_file_display,
            self.new_file_input_box
        )
        self.delete_file_display = Text(25, 5, 1, "Delete File:", text_size=13)
        self.delete_file_input_box = MultilineTextBox(25, 25, 350, 16, "", text_bg_color=(31, 31, 31))
        self.delete_file_confirm_display = Text(25, 45, 1, "Re-enter file name to delete:", text_size=13)
        self.delete_file_confirm_input_box = MultilineTextBox(25, 65, 350, 16, "", text_bg_color=(31, 31, 31))
        self.delete_file_err = MultilineText(25, 80, 350, 32, "", text_color=(255, 180, 180), text_bg_color=None, text_size=13)
        self.delete_file_input_box.single_line = True
        self.delete_file_input_box.on_enter(self.delete_focus_confirm_file)
        self.delete_file_confirm_input_box.single_line = True
        self.delete_file_confirm_input_box.on_enter(self.delete_file)
        self.delete_file_popup = Popup(400, 120).add_children(
            self.delete_file_display,
            self.delete_file_input_box,
            self.delete_file_confirm_display,
            self.delete_file_confirm_input_box,
            self.delete_file_err
        )
        self.top_bar_file = ContextTree.new(
            25, 0, 40, 20, "File", [
                {
                    "New File...": self.top_bar_file_new_file,
                    "Delete File...": self.top_bar_file_delete_file
                },
                # ContextTree.Line(),
                # {
                #     "Open File...": self.top_bar_file_open_file,
                #     "Open Folder...": self.top_bar_file_open_folder
                # },
                # ContextTree.Line(),
                # {
                #     "Save": self.top_bar_file_save,
                #     "Save All": self.top_bar_file_save_all
                # },
                # ContextTree.Line(),
                # {
                #     "Exit": self.top_bar_file_exit
                # }
            ], 115, *self.ctx_tree_opts,
            group="main-ctx"
        )
        self.top_bar_file._uoffx = -self.top_bar_file.width
        self.top_bar_file._uoffy = self.top_bar_file.height
        self.children.append(self.top_bar_file)
        self.top_bar_edit = ContextTree.new(
            70, 0, 40, 20, "Edit", [
                {
                    "Undo": self.top_bar_edit_undo,
                    "Redo": self.top_bar_edit_redo
                },
                ContextTree.Line(),
                {
                    "Cut": self.top_bar_edit_cut,
                    "Copy": self.top_bar_edit_copy,
                    "Paste": self.top_bar_edit_paste
                }
            ], 60, *self.ctx_tree_opts,
            group="main-ctx"
        )
        self.top_bar_edit._uoffx = -self.top_bar_edit.width
        self.top_bar_edit._uoffy = self.top_bar_edit.height
        self.children.append(self.top_bar_edit)
        # ctx_file_onclick = self.top_bar_file.on_left_click
        # def ctx_file(*_, **__):
        #     self.top_bar_edit.children[0].set_visibility(False)
        #     ctx_file_onclick(*_, **__)

        # self.top_bar_file.on_left_click = ctx_file
        # ctx_edit_onclick = self.top_bar_edit.on_left_click
        # def ctx_edit(*_, **__):
        #     self.top_bar_file.children[0].set_visibility(False)
        #     ctx_edit_onclick(*_, **__)

        # self.top_bar_edit.on_left_click = ctx_edit
        self.minimize_button = Button(width-(26*3), 0, 26, 20, " ─ ", (24, 24, 24), hover_color=(70, 70, 70))
        self.minimize_button.on_left_click = self.minimize
        self.children.append(self.minimize_button)
        self.game_app = GameApp(self, editor)
        self.editor_app = EditorApp(self, editor)
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

    def _error_message_update_layout(self, editor):
        self._error_popup.width = self._error_popup.bg.width = self._error_message._text_width + 50
        self._error_popup.height = self._error_popup.bg.height = self._error_message._text_height + 50
        self._error_popup.x = (editor.width-self._error_popup.width)/2
        self._error_popup.y = (editor.height-self._error_popup.height)/2
        self._error_popup.mask.width = editor.width
        self._error_popup.mask.height = editor.height

    def popupError(self, message):
        self._error_message.set_colored_content(message)
        self._error_popup.popup()

    def reset_app_selectors(self):
        self.app_game_selector.bg_color = self.app_game_selector._bg_color = self._app_game_icon
        self.app_game_selector.hover_color = self._app_game_icon_hovered
        self.app_editor_selector.bg_color = self.app_editor_selector._bg_color = self._app_editor_icon
        self.app_editor_selector.hover_color = self._app_editor_icon_hovered
        
    def select_game_app(self, editor):
        self.reset_app_selectors()

        if self.active_app != "game":
            self.active_app = "game"
            RPCD["details"] = "Playing <Insert Dungeon Name Here>"
            RPC.update(**RPCD)
            self.app_game_selector.bg_color = self.app_game_selector._bg_color = self.app_game_selector.hover_color = self._app_game_icon_selected

        else:
            RPCD["details"] = "Just staring at a blank screen..."
            RPC.update(**RPCD)
            self.active_app = ""
    
    def select_editor_app(self, editor):
        self.reset_app_selectors()

        if self.active_app != "editor":
            self.active_app = "editor"
            RPCD["details"] = "Editing a Dungeon"
            RPC.update(**RPCD)
            self.app_editor_selector.bg_color = self.app_editor_selector._bg_color = self.app_editor_selector.hover_color = self._app_editor_icon_selected
            
        else:
            RPCD["details"] = "Just staring at a blank screen..."
            RPC.update(**RPCD)
            self.active_app = ""

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
        editor._do_layout_update = True
        self._update_layout(editor)
        

    def toggle_fullscreen(self, editor):
        editor._do_layout_update = True
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

    def close_window(self, editor):
        editor.running = False
        editor.engine.stop()
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def create_new_file(self, text_box):
        c = text_box.get_content()
        text_box.set_colored_content("")
        comps = c.strip().replace("\\", "/").split("/")
        file_name = comps.pop(-1)

        if comps[0] == "Dungeons":
            comps.pop(0)

        path = "./Dungeons/"
        a = {"DUNGEONS": {}}
        b = a["DUNGEONS"]

        while comps:
            b.update({comps[0]: {}})
            b = b[comps[0]]
            path += comps.pop(0) + "/"

            try:
                os.mkdir(path)

            except:
                pass

        if os.path.exists(path+file_name):
            err = "Error: file already exists:"
            w = max(len(path+file_name), len(err))
            self.popupError(f"{err: ^{w}}\n{path+file_name: ^{w}}")
            return
        
        else:
            open(path+file_name, "w+", encoding="utf-8").close()

        self.editor_app.sub_app_file_editor.open_folder("./Dungeons", self.editor_app.sub_app_file_editor.file_opener_getter, self.editor)
        self.editor_app.sub_app_file_editor.file_opener_getter(path+file_name, self.editor)()
        self.editor_app.sub_app_file_editor.dir_tree.expand_tree(a)

    def delete_focus_confirm_file(self, text_box):
        text_box.focused = False
        text_box._cursor_visible = False
        self.delete_file_confirm_input_box.focused = True
        self.delete_file_confirm_input_box.cursor_location.col = len(self.delete_file_confirm_input_box.get_content())
    
    def delete_file(self, text_box):
        txt = self.delete_file_input_box.get_content().strip()
        txt2 = text_box.get_content().strip()
        
        if txt == txt2 and txt:
            self.delete_file_input_box.set_content("")
            text_box.set_content("")

            try:
                os.remove(f"./Dungeons/{txt}")
                self.editor_app.sub_app_file_editor.open_folder("./Dungeons", self.editor_app.sub_app_file_editor.file_opener_getter, self.editor)

            except Exception as e:
                self.popupError("Error: " + "\n".join(str(a) for a in e.args))

        else:

            if txt and (not txt2):
                self.delete_file_err.set_colored_content("Please re-enter file name in second text box")

            elif txt2 and (not txt):
                self.delete_file_err.set_colored_content("Please enter file name in first text box")

            elif txt and txt2:
                self.delete_file_err.set_colored_content("File names do not match")

            else:
                self.delete_file_err.set_colored_content("Please enter name of file to delete")
                
    def top_bar_file_new_file(self, *_, **__):
        self.top_bar_file.children[0].toggle_visibility()
        self.new_file_popup.popup()

    def top_bar_file_delete_file(self, *_, **__):
        self.top_bar_file.children[0].toggle_visibility()
        self.delete_file_popup.popup()
        
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

        if self.active_app == "game":
            self.game_app._update(editor, X, Y)

        elif self.active_app == "editor":
            self.editor_app._update(editor, X, Y)
            
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
        self.app_bar.height = self.app_line.height = editor.height - 42
        self.minimize_button.x = editor.width - (26*3)
        self.fullscreen_toggle.x = editor.width - (26*2)
        self.close_button.x = editor.width - 26

    def _event(self, editor:Editor, X, Y):

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
            editor.height = max(425, rmy - rsy)
            self._update_layout(editor)

        if self.selected_drag in ["left_drag", "bottom_left_drag"]:
            editor.set_window_location(min (rmx, self.drag_offset[0]-100), self.drag_offset[1])
            editor.width = max(800, self.drag_offset[0] - rmx)
            self._update_layout(editor)

        if self.selected_drag in ["right_drag", "bottom_right_drag"]:
            editor.width = max(800, rmx - rsx)
            self._update_layout(editor)

        if (not editor.mouse[0]) and editor.previous_mouse[0]:
            self.selected_drag = ""

        for child in self.children[::-1]:
            child._event(editor, X, Y)
            
        if self.active_app == "game":
            self.game_app._event(editor, X, Y)

        elif self.active_app == "editor":
            self.editor_app._event(editor, X, Y)


class IOHook:

    def __init__(self):
        self.engine = None
        self.player_data = None
        self.game_app: GameApp = None

    def init(self, engine):
        self.engine = engine

    def color_text(self, text:str) -> str:

        def repl(match:re.Match):
            t = match.group()
            if (m := re.match(r"(\"(?:\\.|[^\"\\])*\"|\'(?:\\.|[^\'\\])*\')", t)): # "..."
                t = re.sub(r"(\\.|`[^`]*`)", "\033[38;2;215;186;125m\\1\033[38;2;206;145;120m", m.group())
                return f"\033[38;2;206;145;120m{t}\033[0m"
            
            elif (m := re.match(r"\+(?:\d+|\[(?:\d+\-\d+|(?:\d+\%\:\d+ *)+)\])(?:dmg|def)\b", t)):
                return f"\033[38;2;100;250;100m{m.group()}\033[0m"
            
            elif (m := re.match(r"\-(?:\d+|\[(?:\d+\-\d+|(?:\d+\%\:\d+ *)+)\])(?:dmg|def)\b", t)):
                return f"\033[38;2;250;100;100m{m.group()}\033[0m"
            
            elif (m := re.match(r"\[(?: INFINITE |EQUIPPED|WEARING)\]", t)):
                return f"\033[38;2;255;255;255m[\033[38;2;25;180;40m{m.group().replace('[', '').replace(']', '')}\033[38;2;255;255;255m]\033[0m"
            
            elif (m := re.match(r"\[(=*)(-*)\](?: *(\d+)/(\d+))?", t)):
                g = m.groups()

                if g[2] is None:
                    return f"\033[38;2;255;255;255m[\033[38;2;100;250;100m{g[0]}\033[38;2;250;100;100m{g[1]}\033[38;2;255;255;255m]\033[0m"
                
                else:
                    a = int(g[2])
                    b = int(g[3])
                    d = int(a/b*10)
                    c1 = (255/10) * d
                    c2 = 255 - c1

                    return f"\033[38;2;255;255;255m[\033[38;2;100;250;100m{g[0]}\033[38;2;250;100;100m{g[1]}\033[38;2;255;255;255m] \033[38;2;{int(c2)};{int(c1)};0m{a}\033[38;2;255;255;255m/\033[38;2;255;255;255m{b}\033[0m"
                
            elif (m := re.match(r"```(?P<lang>json|md|ds|dungeon_script|ascii|less)?(?:\\.|[^`])*```", t)):
                d = m.groupdict()
                lang = d["lang"]
                text = t[3+len(lang or ""):-3]

                if lang == "json":
                    return FileEditor.json_colors(text)
                
                elif lang == "md":
                    return FileEditor.md_colors(text)
                
                elif lang in ["ds", "dungeon_script"]:
                    return FileEditor.ds_colors(text)
                
                elif lang == "less":
                    return self.color_text(text)
                
                else:
                    return self.ascii_colors(text)
                
            elif (m := re.match(r"`[^`\n]*`", t)):
                return f"\033[38;2;95;240;255m{m.group().replace('`', '')}\033[0m"
            
            elif (m := re.match(r"\*[^\*\n]*\*", t)):
                return f"\033[38;2;30;200;80m{m.group().replace('*', '')}\033[0m"
            
            elif (m := re.match(r"_[^_\n]*_", t)):
                return f"\033[38;2;220;90;145m{m.group().replace('_', '')}\033[0m"
            
            else:
                return t

        return re.sub(r"(```(?:\\.|[^`])*```|\"(?:\\.|[^\"\\\n])*\"|\[(?:| INFINITE |EQUIPPED|WEARING)\]|\[=*-*\](?: *\d+/\d+)?|(?:\+|\-)(?:\d+|\[(?:\d+\-\d+|(?:\d+\%\:\d+ *)+)\])(?:dmg|def)\b|\d+ft\b|`[^`\n]*`|\*[^\*\n]*\*|_[^_\n]*_|\d+\/\d+)", repl, text)

    def ascii_colors(self, text:str) -> str:
        return re.sub(r"([│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌]+)", "\033[38;2;100;100;100m\\1\033[0m", text)

    def sendOutput(self, target, text):

        if target in ["log", 0, 1, 5, 6, 7, 8]:
            cl = self.game_app.log_output.colored_content.split("\n")
            cl.append("[" + str({
                0: "engine",
                1: "sound"
            }.get(target, target)) + "]: " + text)

            if len(cl) > 200:
                cl = cl[-200:]

            self.game_app.log_output.set_colored_content("\n".join(cl))
            self.game_app.log_scrollable.offsetY = -(self.game_app.log_output._text_height - (self.game_app.log_output.min_height - 20))

        elif target == 2:
            self.game_app.updateInventory(text)
        
        elif target == 3:
            self.game_app.updateCombat(text)

        elif target == 4:
            self.game_app.updatePlayer(text)

            if text is not None:
                self.game_app.updateInventory(text.inventory)

        elif target == 9:

            if text == "update-combat-ui":
                self.game_app.updateCombat()

            elif text == "update-inventory-ui":
                self.game_app.updateInventory()

        else:
            cl = self.game_app.main_output.colored_content.split("\n")
            cl.append("\n" + text)

            if len(cl) > 200:
                cl = cl[-200:]

            self.game_app.main_output.set_colored_content(self.color_text("\n".join(cl)))
            self.game_app.main_out_scrollable.offsetY = -(self.game_app.main_output._text_height - (self.game_app.main_output.min_height - 20))

    def start(self):
        pass

    def stop(self):
        pass

    def sendInput(self, player_id, text):
        if self.engine is None: return

        cl = self.game_app.log_output.colored_content.split("\n")
        cl.append(f"\033[38;2;100;250;100m[{player_id}]: \033[38;2;255;255;255m" + text + "\033[0m")

        if len(cl) > 200:
            cl = cl[-200:]

        self.game_app.log_output.set_colored_content("\n".join(cl))
        self.game_app.log_scrollable.offsetY = -(self.game_app.log_output._text_height - (self.game_app.log_output.min_height - 20))
        self.engine.handleInput(player_id, text)

if __name__ == "__main__":
    argv = sys.argv[1:]
    if argv:
        if argv[0] == "popout":
            PopoutWindow(content={"PORT": int(argv[1])})
            exit()
        elif argv[0] == "thumbnail" and not getattr(sys, "frozen", False):
            # print("thumbnail")
            border1 = Box(0, 0, 1282, 642, (255, 0, 0))
            border2 = Box(1, 1, 1280, 640, TEXT_BG_COLOR)
            title_t = Text(0, 0, 1, "<Insert Dungeon Name Here>", text_size=65, text_bg_color=None)
            description_t = Text(0, 0, 1, "A text-adventure game engine", text_size=50, text_bg_color=None)
            icon_img = Image(f"{PATH}/dungeon_builder_iconx512.png", 0, 0, 512, 512)
            copyright_t = Text(0, 0, 1, f"© Weston Day 2023-{time.localtime().tm_year}", text_size=35, text_bg_color=None)
            socials_t = Text(0, 0, 1, "  Westbot657", text_size=25, text_bg_color=None)
            socials_img = Image(f"{PATH}/credits/github-mark-white.png", 0, 0, 230/8, 225/8)
            title = Draggable(50, 50, title_t.width, title_t.height, children=[title_t])
            description = Draggable(200, 70, description_t.width, description_t.height, children=[description_t])
            icon = Draggable(100, 100, icon_img.width, icon_img.height, children=[icon_img])
            copy = Draggable(100, 200, copyright_t.width, copyright_t.height, children=[copyright_t])
            socials = Draggable(100, 200, socials_t.width, socials_t.height, children=[socials_t, socials_img])
            title.ignore_child_hovering = True
            description.ignore_child_hovering = True
            copy.ignore_child_hovering = True
            socials.ignore_child_hovering = True
            
            editor = Editor(None, None, 1282, 642)
            editor.add_layer(-1,
                border1, border2
            )
            editor.layers[0] += [
                icon, title, description, copy, socials
            ]
            editor.run()

        exit()
    # if platform.system() == "Windows":
    #     if windows := gw.getWindowsWithTitle("Insert Dungeon Name Here"):
    #         window = windows[0]
    #         window.alwaysOnTop(True)
    #         window.alwaysOnTop(False)
    #         exit()
    # elif platform.system() == "Darwin":
    #     macOSfocusWindow("Insert Dungeon Name Here")
    try:
        from Engine import Engine
    except ImportError:
        sys.path.append("./Engine")
        _Engine = SourceFileLoader("Engine", "./Engine/Engine.py").load_module() # pylint: disable=no-value-for-parameter
        Engine = _Engine.Engine
    io_hook = IOHook()
    engine = Engine(io_hook, is_ui=True)
    editor = Editor(engine, io_hook)
    c = CodeEditor(editor.width, editor.height, editor)
    editor.layers[0] += [
        c
    ]
    editor.run()

"""
# │┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌

Ideas:


Combat Sequence Editor:
╔════════════════════════════════════════════════╦════════════╗ 
║ <combat_id>                                    ║ Enemy list ║ <- List of individual enemies used in combat
╠════════════════════════════════════════════════╣            ║ may also contain randomizable elements (somehow, idk)
║ Event 1 (usually spawn enemies + dialoug)      ║            ║ 
╠════════════╦════════════╦══════════════════════╣            ║ 
║ Trigger 2A ║ Trigger 2B ║ Trigger 2C           ║            ║ <- Tabs: Triggers A, B, or C may be triggered, Each leads to a
║            ╙────────────╨──────────────────────╢            ║ unique chain of events. These branches may join back into a
╟────────────────────────────────────────────────╢            ║ comman sequence at a later time, or continue seperate for the
║ Event 2A-3                                     ║            ║ remainder of the combat sequence
╟────────────────────────────────────────────────╢            ║ 
║ Trigger 2A-4                                   ║            ║ 
╟────────────────────────────────────────────────╢            ║ 
║ Event 2A-5                                     ║            ║ 
╟────────────────────────────────────────────────╢            ║ 
║ ...                                            ║            ║ 
╠════════════════════════════════════════════════╣            ║ <- end of sub-sequence 2A/2B/2C 
║ ...                                            ║            ║ 
╚════════════════════════════════════════════════╩════════════╝ <- end of combat sequence


Map Saving:

rect: [center X, center Y, width, height, rotation]
image: [center X, center Y, width, height, rotation], src: <file location>




"""
