# pylint: disable=[W,R,C, import-error]

from UIElement import UIElement
from Geometry import Box
from RenderPrimitives import Image
from Options import PATH
from FunctionalElements import Button
from FileEditorSubApp import FileEditorSubApp
from AdvancedEditorSubApp import AdvancedEditorSubApp


class EditorApp(UIElement):
    
    def __init__(self, code_editor, editor):
        self.code_editor = code_editor
        self.children = []
        self.sub_apps = []
        self.sub_app_bar = Box(51, 21, 50, editor.height-42, (24, 24, 24))
        self.children.append(self.sub_app_bar)
        self.sub_app_bar_line = Box(101, 21, 1, editor.height-42, (70, 70, 70))
        self.children.append(self.sub_app_bar_line)
        self.file_editor_icons = [
            Image(f"{PATH}/file_editor_sub_app.png", 0, 0, 50, 50),
            Image(f"{PATH}/file_editor_sub_app_hovered.png", 0, 0, 50, 50),
            Image(f"{PATH}/file_editor_sub_app_selected.png", 0, 0, 50, 50)
        ]
        
        self.file_editor_sub_app_button = Button(51, 71, 50, 50, "", self.file_editor_icons[0], hover_color=self.file_editor_icons[1], click_color=self.file_editor_icons[2])
        self.file_editor_sub_app_button.on_left_click = self.click_file_editor
        self.file_editor_sub_app_button._alt_text = "Basic File Editor"
        self.children.append(self.file_editor_sub_app_button)
        self.sub_app_file_editor = FileEditorSubApp(code_editor, editor)
        self.sub_apps.append((self.file_editor_sub_app_button, self.file_editor_icons))
        
        
        self.advanced_editor_icons = [
            Image(f"{PATH}/advanced_editor_sub_app.png", 0, 0, 50, 50),
            Image(f"{PATH}/advanced_editor_sub_app_hovered.png", 0, 0, 50, 50),
            Image(f"{PATH}/advanced_editor_sub_app_selected.png", 0, 0, 50, 50)
        ]
        
        self.advanced_editor_sub_app_button = Button(51, 21, 50, 50, "", self.advanced_editor_icons[0], hover_color=self.advanced_editor_icons[1], click_color=self.advanced_editor_icons[2])
        self.advanced_editor_sub_app_button.on_left_click = self.click_advanced_editor
        self.advanced_editor_sub_app_button._alt_text = "Advanced Editor"
        self.children.append(self.advanced_editor_sub_app_button)
        self.sub_app_advanced_editor = AdvancedEditorSubApp(code_editor, editor)
        self.sub_apps.append((self.advanced_editor_sub_app_button, self.advanced_editor_icons))
        
        self.active_app = None #self.sub_app_file_editor
    
    def click_file_editor(self, *_, **__):

        if self.active_app != self.sub_app_file_editor:
            self._reset_sub_apps()
            self.active_app = self.sub_app_file_editor
            self.file_editor_sub_app_button._bg_color = self.file_editor_sub_app_button.bg_color = self.file_editor_sub_app_button.hover_color = self.file_editor_icons[2]

        else:
            self._reset_sub_apps()
    
    def click_advanced_editor(self, *_, **__):
        if self.active_app != self.sub_app_advanced_editor:
            self._reset_sub_apps()
            self.active_app = self.sub_app_advanced_editor
            self.advanced_editor_sub_app_button._bg_color = self.advanced_editor_sub_app_button.bg_color = self.advanced_editor_sub_app_button.hover_color = self.advanced_editor_icons[2]
        
        else:
            self._reset_sub_apps()
    
    def _reset_sub_apps(self):
        self.active_app = None

        for button, icons in self.sub_apps:
            button._bg_color = button.bg_color = icons[0]
            button.hover_color = icons[1]

    def _update_layout(self, editor):
        self.sub_app_bar.height = self.sub_app_bar_line.height = editor.height - 42
        if self.active_app:
            self.active_app._update_layout(editor)
        

    def _event(self, editor, X, Y):
        if editor._do_layout_update:
            self._update_layout(editor)
        
        if self.active_app:
            self.active_app._event(editor, X, Y)
        
        for child in self.children[::-1]:
            child._event(editor, X, Y)
    
    def _update(self, editor, X, Y):
        
        if self.active_app:
            self.active_app._update(editor, X, Y)
        
        for child in self.children:
            child._update(editor, X, Y)

