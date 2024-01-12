# pylint: disable=W,R,C,no-member

from UIElement import UIElement
from RenderPrimitives import Color, Image, Animation
from Options import TEXT_COLOR, TEXT_BG_COLOR, SCROLL_MULTIPLIER
from MultilineText import MultilineText
from FunctionalElements import Collapsable
from MultilineTextBox import MultilineTextBox

class NumberedTextArea(UIElement):

    class Fold:
        __slots__ = ["lines"]
        def __init__(self, lines:list):
            self.lines = lines

    def __init__(self, x:int, y:int, width:int, height:int, text_color:Color|tuple|int=TEXT_COLOR, text_bg_color:Color|Image|Animation|tuple|int=TEXT_BG_COLOR, scroll_speed=SCROLL_MULTIPLIER, split_color=None):
        assert width >= 200, "width must be 200 or more (sorry)"
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text_color = Color.color(text_color)
        self.text_bg_color = Color.color(text_bg_color)
        self.lines = MultilineText(0, 0, 75, self.height, f"{'1': >9}", self.text_color, self.text_bg_color)
        self.editable = MultilineTextBox(2, 0, self.width-75, self.height, "", self.text_color, self.text_bg_color)

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
            split_size=75,
            scroll_speed = scroll_speed,
            
        )

        self.collapsable.main_area.left_bound = 0
        self.collapsable.main_area.top_bound = 0
        self.collapsable.aside.left_bound = 0
        self.collapsable.aside.top_bound = 0
        self.collapsable.aside.right_bound = 0

    def _update_layout(self):
        # print(f"Numbered text area _update_layout!")
        self.lines.min_height = self.editable.min_height = self.height
        self.collapsable.height = self.collapsable.main_area.height = self.collapsable.aside.height = self.height-20
        self.collapsable.width = self.width-5
        self.editable.min_width = self.width-75


    def set_content(self, content:str):
        self.editable.set_content(content)

    def _update(self, editor, X, Y):
        self.collapsable._update(editor, X, Y)
        
    def _event(self, editor, X, Y):
        
        # self._update_layout(editor)
        
        self.collapsable._event(editor, X, Y)

        if self.collapsable.main_area.hovered:
            self.collapsable.aside.offsetY = self.collapsable.main_area.offsetY
        if self.collapsable.aside.hovered:
            self.collapsable.main_area.offsetY = self.collapsable.aside.offsetY

        lines = len(self.collapsable.main_area.children[0].get_lines())

        # print(f"Numbered Text Area lines: {lines}")

        txt = [f"{i+1: >9}" for i in range(lines)]

        # print(self.collapsable.aside.children[0])
        self.collapsable.aside.children[0].set_colored_content("\n".join(txt))

        # if lines == 0:
        #     raise Exception("Numbered Text Editor reached 0 lines, which is meant to be impossible!!")

        d = self.collapsable.main_area.children[0].surfaces[0].get_height()

        self.collapsable.main_area.bottom_bound = -d * (lines-1)
        self.collapsable.aside.bottom_bound = -d * (lines-1)
