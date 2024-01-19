# pylint: disable=W,R,C,import-error

import re

class MarkdownRenderer:

    def __init__(self, file:str):
        self.file = file
        self.content = ""
        self.components = []
    
    def render(self):
        self.components.clear()

        with open(self.file, "r+", encoding="utf-8") as f:
            self.content = f.read()

        lines = [l.strip() for l in re.split(r"(?:(?:\n|  )\n+)", self.content)]


        for line in lines:
            ...


    def _event(self, editor, X, Y):
        ...
    
    def _update(self, editor, X, Y):
        ...



