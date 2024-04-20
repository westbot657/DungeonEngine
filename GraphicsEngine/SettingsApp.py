# pylint: disable=W,R,C,import-error

from UIElement import UIElement


class SettingsApp(UIElement):
    def __init__(self, code_editor, editor):
        self.code_editor = code_editor
        self.children = []
        
    def _event(self, editor, X, Y):
        ...
        
    def _update(self, editor, X, Y):
        ...