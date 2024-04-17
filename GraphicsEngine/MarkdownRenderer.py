# pylint: disable=W,R,C,import-error

import re
import webbrowser

from Geometry import Box
from RenderPrimitives import Color, Image
from Text import Text
from Organizers import Link

# webbrowser.open(url)

class MarkdownRenderer:

    def __init__(self, container, file:str):
        self.container = container
        self.file = file
        self.content = ""
        self.components = []
        self.links = []
        self.render_mode = "normal"

    def render(self):
        self.components.clear()

        with open(self.file, "r+", encoding="utf-8") as f:
            self.content = f.read()

        lines = [l.replace("\n", " ").strip() for l in re.split(r"(?:(?:\n|  )\n+)", self.content)]

        content_height = 0
        content_left = 0
        content_right = 0

        for line in lines:
            if m := re.match(r"\<\!\-\- \#\!(?P<mode>[^ ]+) \-\-\>", line):
                self.render_mode = m.groupdict()["mode"]

            # page seperator line
            if line.strip() == "---":
                ...

            if self.render_mode == "credits":
                # align content to center
                # create badges
                ...

                # H1
                # H2
                # H3
                # H4?
                # text
                # badges
                # social links

            elif self.render_mode == "normal":
                # left align
                # 
                ...

                # H1
                # H2
                # H3
                # H4?
                # text
                # bullet points
                # code blocks
                # links


    def _event(self, editor, X, Y):
        ...

    def _update(self, editor, X, Y):
        ...

