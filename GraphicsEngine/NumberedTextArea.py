# pylint: disable=W,R,C,no-member,import-error

from UIElement import UIElement
from RenderPrimitives import Color, Image, Animation
from Options import TEXT_COLOR, TEXT_BG_COLOR, SCROLL_MULTIPLIER, TEXT_SIZE, TEXT_BG2_COLOR, TEXT_BG3_COLOR
from MultilineText import MultilineText
from FunctionalElements import Collapsable
from MultilineTextBox import MultilineTextBox
from Util import PopoutElement
from Geometry import Box

@PopoutElement()
class NumberedTextArea(UIElement):

    class FakeHover:
        def __init__(self):
            self._hovered = True

    fake_hover = FakeHover()

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
        self.lines = MultilineText(0, 0, 70, self.height, f"{'1': >{(70 // TEXT_SIZE)+2}}", self.text_color, self.text_bg_color)
        self._fill = Box(0, 0, 7, self.height, self.text_bg_color)
        self.editable = MultilineTextBox(7, 0, self.width-80, self.height, "", self.text_color, self.text_bg_color)
        
        self.show_scrollbar = False
        self.scroll_bg = TEXT_BG2_COLOR
        self.scroll_bar_color = (100, 100, 100)
        self.scroll_bar_hover_color = (120, 120, 120)
        self.scroll_bar_click_color = (140, 140, 140)
        self.scroll_bar_height = 0
        self.scroll_bar_y = 0
        self.scroll_click_offset = 0
        self.scroll_target = 0
        self.scroll_clicked = False
        self.scroll_bar_width = 20 # this is the width of the full area where the scroll bar is, the bar itself will visibly be 2px thinner on each side (but will collide 1px thinner)
        self.scroll_visibility_inset = 2
        self.scroll_collision_inset = 1
        self.scroll_dragging = False
        self.scroll_hovered = False

        self.collapsable = Collapsable(
            self.x, self.y,
            self.width, self.height,
            [
                self._fill,
                self.editable
            ],
            [
                self.lines
            ],
            split_type=Collapsable.SplitType.VERTICAL_RIGHT,
            split_draggable=False,
            split_size=70,
            scroll_speed = scroll_speed,
        )

        self.collapsable.main_area.left_bound = 0
        self.collapsable.main_area.top_bound = 0
        self.collapsable.aside.left_bound = 0
        self.collapsable.aside.top_bound = 0
        self.collapsable.aside.right_bound = 0

    def _update_layout(self):
        self.lines.min_height = self.editable.min_height = self.height
        self.collapsable.height = self.collapsable.main_area.height = self.collapsable.aside.height = self.height
        self._fill.height = self.editable.min_height = self.editable._text_height + self.height
        self.collapsable.width = self.width-28
        self.editable.min_width = self.width-80

    def get_content(self):
        return self.editable.get_content()

    def set_content(self, content:str):
        self.editable.set_content(content)

    def _update(self, editor, X, Y):
        
        self.collapsable._update(editor, X, Y)
        
        if self.show_scrollbar:
            editor.screen.fill(self.scroll_bg, ((self.x+self.width)-self.scroll_bar_width+self.scroll_collision_inset-4, self.y, self.scroll_bar_width-(2*self.scroll_collision_inset), self.height))
            editor.screen.fill((self.scroll_bar_click_color if self.scroll_dragging else (self.scroll_bar_hover_color if self.scroll_hovered else self.scroll_bar_color)), ((self.x+self.width)-self.scroll_bar_width+self.scroll_visibility_inset-4, self.y+self.scroll_bar_y, self.scroll_bar_width-(2*self.scroll_visibility_inset), self.scroll_bar_height))
            
    def _event(self, editor, X, Y):
        
        self._update_layout()
        
        self.show_scrollbar = self.editable._text_height - self.editable._height >= 0
        

        if self.show_scrollbar:
            self.scroll_hovered = False
            self.scroll_bar_height = (self.height**2)/(self.editable._text_height + self.height - self.editable._height)
            print(self.scroll_bar_height)
            
            if editor.collides(editor.mouse_pos, ((self.x+self.width)-self.scroll_bar_width+self.scroll_collision_inset-4, self.y+self.scroll_bar_y, self.scroll_bar_width-(2*self.scroll_collision_inset), self.scroll_bar_height)):
                if editor._hovering is None:
                    editor._hovering = self.fake_hover
                    editor._hovered = self.fake_hover._hovered = True
                self.scroll_hovered = True
                if editor.left_mouse_down():
                    self.scroll_dragging = True
                    self.scroll_click_offset = editor.mouse_pos[1]-self.scroll_bar_y

            elif editor.collides(editor.mouse_pos, ((self.x+self.width)-self.scroll_bar_width+self.scroll_collision_inset-4, self.y, self.scroll_bar_width-(2*self.scroll_collision_inset), self.height)):
                if editor._hovering is None:
                    editor._hovering = self.fake_hover
                    editor._hovered = self.fake_hover._hovered = True
                if editor.left_mouse_down():
                    self.scroll_dragging = True
                    self.scroll_bar_y = min(max(0, editor.mouse_pos[1]-self.y-(self.scroll_bar_height/2)), self.height-self.scroll_bar_height)
                    self.scroll_click_offset = editor.mouse_pos[1]-self.scroll_bar_y

            if not editor.mouse[0]:
                self.scroll_dragging = False
        
        else:
            self.scroll_dragging = False
            
        
        if self.scroll_dragging:
            self.scroll_bar_y = min(max(0, editor.mouse_pos[1]-self.scroll_click_offset), self.height-self.scroll_bar_height)
            
            ratio = self.scroll_bar_y / ((self.height-self.scroll_bar_height))
            self.collapsable.main_area.offsetY = self.collapsable.aside.offsetY = -((self.editable._text_height - self.editable._height)*ratio)
        else:
            ratio = -self.collapsable.main_area.offsetY / (self.editable._text_height - self.editable._height) #
            self.scroll_bar_y = (self.height-self.scroll_bar_height) * ratio
        
        self.collapsable._event(editor, X, Y)

        if self.collapsable.main_area.hovered:
            self.collapsable.aside.offsetY = self.collapsable.main_area.offsetY
        if self.collapsable.aside.hovered:
            self.collapsable.main_area.offsetY = self.collapsable.aside.offsetY

        lines = len(self.collapsable.main_area.children[1].get_lines())

        # print(f"Numbered Text Area lines: {lines}")

        txt = [f"{i+1: >{(70 // TEXT_SIZE)+2}}" for i in range(lines)]

        # print(self.collapsable.aside.children[0])
        self.collapsable.aside.children[0].set_colored_content("\n".join(txt))

        # if lines == 0:
        #     raise Exception("Numbered Text Editor reached 0 lines, which is meant to be impossible!!")

        d = self.collapsable.main_area.children[1].surfaces[0].get_height()

        self.collapsable.main_area.bottom_bound = -d * (lines-1)
        self.collapsable.aside.bottom_bound = -d * (lines-1)
