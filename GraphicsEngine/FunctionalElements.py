# pylint: disable=W,R,C,no-member

from UIElement import UIElement
from RenderPrimitives import Color, Image, Animation
from Options import TEXT_COLOR, TEXT_BG_COLOR, TEXT_SIZE, \
    FONT, SCROLL_MULTIPLIER
from EditorMimic import EditorMimic
from Organizers import Draggable
from enum import Enum, auto
import pygame

class Button(UIElement):

    __slots__ = [
        "x", "y", "width", "height", "text", "bg_color", "hover_color", "click_color",
        "text_color", "lheld", "rheld", "hovered", "_hovered", "children", "_uoffx",
        "_uoffy", "text_size", "font", "surface", "_override", "_mimic"
    ]

    class _overrider:
        
        __slots__ = [
            "_parent", "screen"
        ]
        
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
        
        r = self.font.render(self.text, True, tuple(self.text_color))
        if self.width == -1:
            self.width = r.get_width()
        
        self.surface = pygame.Surface((min(1, self.width), self.height), pygame.SRCALPHA, 32) # pylint: disable=no-member
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
        self.surface.blit(r, (1, 1))
        
        self._override = self._overrider(self)
        self._mimic = EditorMimic(None, self._override)

    def _event(self, editor, X, Y):
        for child in self.children[::-1]:
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
            if editor._hovering is None:
                self.hovered = editor._hovered = True
                editor._hovering = self
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
        
        for child in self.children:
            child._update(editor, X+self.x+self._uoffx, Y+self.y+self._uoffy)
    
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
        
        __slots__ = [
            "tcu", "tch", "tcs",
            "bgu", "bgh", "bgs",
            "location", "tabs_parent"
        ]
        
        def __init__(self, parent, x, y, width, height, location, text, tcu:tuple[int, int, int]|Image=TEXT_COLOR, tch:tuple[int, int, int]|Image=TEXT_COLOR, tcs:tuple[int, int, int]|Image=TEXT_COLOR, bgu:tuple[int, int, int]|Image=TEXT_BG_COLOR, bgh:tuple[int, int, int]|Image=TEXT_BG_COLOR, bgs:tuple[int, int, int]|Image=TEXT_BG_COLOR, text_size=TEXT_SIZE):
            super().__init__(x, y, width, height, text, bgu, tcu, text_size, bgh, bgs)
            self.tcu:tuple[int, int, int]|Image = tcu
            self.tch:tuple[int, int, int]|Image = tch
            self.tcs:tuple[int, int, int]|Image = tcs
            self.bgu:tuple[int, int, int]|Image = bgu
            self.bgh:tuple[int, int, int]|Image = bgh
            self.bgs:tuple[int, int, int]|Image = bgs
            self.location = location
            self.tabs_parent = parent
            self.children = []
            
            # print(self.children, id(self.children))

        def on_left_click(self, editor):
            self.tabs_parent.active_tab = self.text
            self.tabs_parent.reset_tab_colors()
        
        # def off_left_click(self, editor):
        #     self.bg_color = self._bg_color = self.bgu
        #     self.hover_color = self.bgh
        #     self.text_color = self.tch
        
        # def on_hover(self, editor):
        #     self.bg_color = self.bgh
        #     self.text_color = self.tch

        # def off_hover(self, editor):
        #     self.bg_color = self.bgu
        #     self.text_color = self.tcu

        def pre_blit(self, editor, X, Y):
            if self.location == Tabs.Style.LEFT:
                self.surface = pygame.transform.rotate(self.surface, 90)
            elif self.location == Tabs.Style.RIGHT:
                self.surface = pygame.transform.rotate(self.surface, -90)

        def _event(self, editor, X, Y):
            return super()._event(editor, X, Y)
        
        def _update(self, editor, X, Y):
            return super()._update(editor, X, Y)

    __slots__ = [
        "x", "y", "width", "height", "tab_style",
        "tab_data", "tab_children", "active_tab",
        "tab_color_unselected", "tab_color_hovered",
        "tab_color_selected", "tab_color_empty",
        "text_color_unselected", "text_color_hovered",
        "text_color_selected", "content_bg_color",
        "tab_buffer", "tab_height", "tab_width",
        "scrollable_tabs", "tab_padding",
        "_tabs_area", "_tab_objects"
    ]

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
        
        `tab_padding`: int how much space to put between tabs
        """
        if tab_data is ...: tab_data = {}
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tab_style = tab_style
        self.tab_data = tab_data
        self.tab_children = options.get("tab_children", None) or {}
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
        
        self.tab_buffer            : int  = options.get("tab_buffer", 0)
        self.tab_height            : int  = options.get("tab_height", TEXT_SIZE + 2)
        self.tab_width             : int  = options.get("tab_width", 75)

        self.scrollable_tabs       : bool = options.get("scrollable_tabs", False)
        
        self.tab_padding           : int  = options.get("tab_padding", 0)
        
        if self.scrollable_tabs:
            self._tabs_area = Scrollable(self.x, self.y, 1, 1, self.tab_color_empty, left_bound=0, top_bound=0, scroll_speed=40)
        else:
            self._tab_objects = []
        self.load_tabs()

    def reset_tab_colors(self):
        if self.scrollable_tabs:
            l = self._tabs_area.children
        else:
            l = self._tab_objects

        for tab in l:
            tab:Tabs._Tab
            if tab.text == self.active_tab:
                tab.bg_color = tab._bg_color = tab.hover_color = tab.bgs
            else:
                tab.bg_color = tab._bg_color = tab.bgu
                tab.hover_color = tab.bgh

    def get_tab(self, label):
        if self.scrollable_tabs:
            for c in self._tabs_area.children:
                if c.text == label:
                    return c
        else:
            for c in self._tab_objects:
                if c.text == label:
                    return c

    def load_tabs(self):
        if self.scrollable_tabs:
            self._tabs_area.children.clear()
        else:
            self._tab_objects.clear()

        if self.tab_style == Tabs.Style.TOP:
            self._tabs_area.swap_scroll = True
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
                t = Tabs._Tab(
                    self, x, y, self.tab_width, self.tab_height,
                    Tabs.Style.TOP, name,
                    self.text_color_unselected, self.text_color_hovered, self.text_color_selected,
                    self.tab_color_unselected, self.tab_color_hovered, self.tab_color_selected
                )
                t.children = self.tab_children.get(name, list())
                # print("CHILDREN: ", t.children)
                if self.active_tab == name:
                    t.on_left_click(None)
                
                if self.scrollable_tabs:
                    t.width = t.font.render(t.text, True, (0, 0, 0)).get_width()
                    self._tabs_area.children.append(t)
                    x += t.width + 1 + self.tab_padding
                else:
                    self._tab_objects.append(t)
                    x += self.tab_width + 1 + self.tab_padding
            if self.scrollable_tabs:
                self._tabs_area.right_bound = -x
        
        elif self.tab_style == Tabs.Style.BOTTOM:
            self._tabs_area.swap_scroll = True
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
                t.children = self.tab_children.get(name, list())
                # print("CHILDREN: ", t.children)
                if self.scrollable_tabs:
                    t.width = t.font.render(t.text, True, (0, 0, 0)).get_width()
                    self._tabs_area.children.append(t)
                    x += t.width + 1 + self.tab_padding
                else:
                    self._tab_objects.append(t)
                    x += self.tab_width + 1 + self.tab_padding
            if self.scrollable_tabs:
                self._tabs_area.right_bound = -x

        elif self.tab_style == Tabs.Style.LEFT:
            self._tabs_area.swap_scroll = False
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
                t.children = self.tab_children.get(name, list())
                # print("CHILDREN: ", t.children)
                if self.scrollable_tabs:
                    t.width = t.font.render(t.text, True, (0, 0, 0)).get_width()
                    self._tabs_area.children.append(t)
                    y += t.width + 1 + self.tab_padding
                else:
                    self._tab_objects.append(t)
                    y += self.tab_width + 1 + self.tab_padding
            if self.scrollable_tabs:
                self._tabs_area.bottom_bound = -y

        elif self.tab_style == Tabs.Style.RIGHT:
            self._tabs_area.swap_scroll = False
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
                t.children = self.tab_children.get(name, list())
                # print("CHILDREN: ", t.children)
                if self.scrollable_tabs:
                    t.width = t.font.render(t.text, True, (0, 0, 0)).get_width()
                    self._tabs_area.children.append(t)
                    y += t.width + 1 + self.tab_padding
                else:
                    self._tab_objects.append(t)
                    y += self.tab_width + 1 + self.tab_padding
            if self.scrollable_tabs:
                self._tabs_area.bottom_bound = -y

        elif self.tab_style == Tabs.Style.MENU:
            self._tabs_area.swap_scroll = False
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
                t.children = self.tab_children.get(name, list())
                # print("CHILDREN: ", t.children)
                if self.scrollable_tabs:
                    t.width = t.font.render(t.text, True, (0, 0, 0)).get_width()
                    mw = max(t.width, mw)
                    self._tabs_area.children.append(t)
                    #self._tabs_area.right_bound = min(self._tabs_area.right_bound, -t.width)
                    y += self.tab_height + self.tab_padding
                else:
                    self._tab_objects.append(t)
                    y += self.tab_height + self.tab_padding
            if self.scrollable_tabs:
                for tab in self._tabs_area.children:
                    tab.width = mw
                
                self._tabs_area.right_bound = -mw
                self._tabs_area.bottom_bound = -y

        else:
            raise Exception(f"{self.tab_style} is not implemented yet")
        
        self.reset_tab_colors()

    def add_tab(self, tab_name:str, contents:list=..., children:list=None):
        if contents is ...: contents = []
        self.tab_data[tab_name] = contents
        self.tab_children[tab_name] = children or []
        self.load_tabs()

    def add_content(self, tab_name:str, contents:list|tuple):
        if tab_name in self.tab_data:
            for c in contents:
                self.tab_data.get(tab_name).append(c)

    def add_tab_children(self, tab_name:str, children:list|tuple):
        # print(f"ADD CHILDREN: '{tab_name}' <- {children}")
        if tab_name in self.tab_data.keys():
            if tab_name not in self.tab_children.keys():
                self.tab_children.update({tab_name: []})
            for c in children:
                self.tab_children[tab_name].append(c)
        # print(f"ALL CHILDREN of '{tab_name}': {self.get_tab(tab_name).children}")

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
            self.active_tab = None
            self.load_tabs()

        if tab_name in self.tab_children.keys():
            self.tab_children.pop(tab_name)

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
            # for child in self._tabs_area.children:
            #     if _c := self.tab_children.get(child.text, None):
            #         for c in _c:
            #             # print(f"child update: {c} @ ({X+self.x+child.x}, {Y+self.y+child.y-self.tab_height})")
            #             c._update(editor, X+self.x+child.x, Y+self.y+child.y-self.tab_height)
        else:
            for tab in self._tab_objects:
                tab:Tabs._Tab
                tab._update(editor, X+self.x, Y+self.y)
                # if _c := self.tab_children.get(tab.text, None):
                #     for c in _c:
                #         c._update(editor, X+self.x+tab.x, Y+self.x+tab.y)
        
        content = self.tab_data.get(self.active_tab, [])
        for c in content:
            c._update(editor, X, Y)

    def _event(self, editor, X, Y):
        content = self.tab_data.get(self.active_tab, [])
        
        for c in content:
            c._event(editor, X, Y)

        if self.scrollable_tabs:
            # print(f"tab children: {self.tab_children}")
            # for child in self._tabs_area.children:
            #     print(child.text)
            #     if (_c := self.tab_children.get(child.text, None)) is not None:
            #         for c in _c:
            #             # print(f"child event: {c} @ ({X+self.x+child.x}, {Y+self.y+child.y-self.tab_height})")
            #             c._event(editor, X+self.x+child.x, Y+self.y+child.y-self.tab_height)
            self._tabs_area._event(editor, X, Y)
        else:
            for tab in self._tab_objects:
                tab:Tabs._Tab
                # if _c := self.tab_children.get(tab.text, None):
                #     for c in _c:
                #         c._event(editor, X+self.x+tab.x, Y+self.x+tab.y)
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
            self.scroll_speed = options.get("scroll_speed", SCROLL_MULTIPLIER)
            self.hovered = False
            self.left_bound = options.get("left_bound", None)
            self.top_bound = options.get("top_bound", None)
            self.right_bound = options.get("right_bound", None)
            self.bottom_bound = options.get("bottom_bound", None)
            self.swap_scroll = options.get("swap_scroll", False)
            if self.left_bound is not None and self.right_bound is not None:
                assert self.left_bound >= self.right_bound, "left bound must be larger than right bound (I know, it's wierd)"
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
            for child in self.children[::-1]:
                child._event(self.parent, 0, 0)

            #print(f"Scrollable: {_y-self.y=} {_y-self.y==self.mouse_pos[1]=}")

            if editor.collides((_x, _y), (self.x, self.y, self.width, self.height)):
                if editor._hovering is None:
                    editor._hovering = self
                if editor._hovering or any([child.hovered for child in self.children if hasattr(child, "hovered")]):
                    self.hovered = True
                    if editor.scroll is not None:
                        if (pygame.K_LSHIFT in editor.keys and not self.swap_scroll) or (self.swap_scroll): # pylint: disable=no-member
                            self.offsetX += editor.scroll * self.scroll_speed
                            if self.left_bound is not None:
                                self.offsetX = min(self.offsetX, self.left_bound)
                            if self.right_bound is not None:
                                self.offsetX = max(self.offsetX, self.right_bound)
                        elif (pygame.K_LSHIFT in editor.keys and self.swap_scroll) or (not self.swap_scroll):
                            self.offsetY += editor.scroll * self.scroll_speed
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
        def __init__(self, parent:UIElement, x:int, y:int, width:int, height:int, main_content:list=None, side_content:list=None, **options): # pylint: disable=dangerous-default-value
            
            main_content = main_content or []
            side_content = side_content or []
            
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
            self.scroll_speed = options.get("scroll_speed", SCROLL_MULTIPLIER)
            self.split_color = options.get("split_color", None) or (70, 70, 70)

            self.screen = pygame.Surface((self.width, self.height))
            self.mouse_pos = [0, 0]

            if self.split_type == Collapsable.SplitType.VERTICAL_LEFT:
                self.main_area = Scrollable(0, 0, width - self.split_size, height, scroll_speed=self.scroll_speed)
                self.main_area.children = main_content
                self.aside = Scrollable(width - self.split_size, 0, self.split_size, height, scroll_speed=self.scroll_speed)
                self.aside.children = side_content

                self.split = Draggable((width - self.split_size) - 2, 0, 4, height, lock_vertical=True)

                if not self.split_visible:
                    self.main_area.width = width
                    self.aside.width = 0
                    self.aside.x = width
                    self.split.x = width - 2
            
            elif self.split_type == Collapsable.SplitType.VERTICAL_RIGHT:
                self.main_area = Scrollable(self.split_size, 0, width - self.split_size, height, scroll_speed=self.scroll_speed)
                self.main_area.children = main_content
                self.aside = Scrollable(0, 0, self.split_size, height, scroll_speed=self.scroll_speed)
                self.aside.children = side_content

                self.split = Draggable(self.split_size - 2, 0, 4, height, lock_vertical=True)

                if not self.split_visible:
                    self.main_area.width = width
                    self.main_area.x = 0
                    self.aside.width = 0
                    self.split.x = -2

            elif self.split_type == Collapsable.SplitType.HORIZONTAL_TOP:
                self.main_area = Scrollable(0, 0, width, height - self.split_size, scroll_speed=self.scroll_speed)
                self.main_area.children = main_content
                self.aside = Scrollable(0, height - self.split_size, width, self.split_size, scroll_speed=self.scroll_speed)
                self.aside.children = side_content

                self.split = Draggable(0, (height - self.split_size) - 2, width, 4, lock_horizontal=True)

                if not self.split_visible:
                    self.main_area.height = height
                    self.aside.height = 0
                    self.aside.y = height
                    self.split.y = height - 2

            elif self.split_type == Collapsable.SplitType.HORIZONTAL_BOTTOM:
                self.main_area = Scrollable(0, self.split_size, width, height - self.split_size, scroll_speed=self.scroll_speed)
                self.main_area.children = main_content
                self.aside = Scrollable(0, 0, width, self.split_size, scroll_speed=self.scroll_speed)
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
                self.split.height = self.height

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
                self.split.height = self.height

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
                self.split.width = self.width

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
                self.split.width = self.width

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
                editor.screen.fill(self.split_color, (X+self.x+self.split.x, Y+self.y+self.split.y, self.split.width, self.split.height))
            elif self.split_type in [Collapsable.SplitType.VERTICAL_LEFT, Collapsable.SplitType.VERTICAL_RIGHT]:
                editor.screen.fill(self.split_color, (X+self.x+self.split.x+2, Y+self.y+self.split.y, 1, self.split.height))
            elif self.split_type in [Collapsable.SplitType.HORIZONTAL_TOP, Collapsable.SplitType.HORIZONTAL_BOTTOM]:
                editor.screen.fill(self.split_color, (X+self.x+self.split.x, Y+self.y+self.split.y+2, self.split.width, 1))

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

