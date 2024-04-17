# pylint: disable=[W,R,C, import-error]

from Util import PopoutElement
from UIElement import UIElement
from RenderPrimitives import Image
from Options import PATH
from FunctionalElements import Button, Scrollable
from Text import Text
    
@PopoutElement()
class DirectoryTree(UIElement):
    folds = {
        "open": Image(f"{PATH}/folder_open.png", 0, 0, 14, 14),
        "closed": Image(f"{PATH}/folder_closed.png", 0, 0, 14, 14)
    }
    file_icons = {
        "default": Image(f"{PATH}/default_file_icon.png", 0, 0, 14, 14),
        "dungeon_script": Image(f"{PATH}/ds_file_icon.png", 0, 0, 14, 14),
        "combat": Image(f"{PATH}/combat_file_icon.png", 0, 0, 14, 14),
        "json": Image(f"{PATH}/json_file_icon.png", 0, 0, 14, 14)
    }
    file_icons["ds"] = file_icons["dungeon_script"]
    
    __slots__ = [
        "x", "y", "name", "expanded", "width", "children",
        "_height", "height", "components", "surface", "folder"
    ]
    
    class Folder(UIElement):
        __slots__ = [
            "parent", "name", "width", "components", "collapsed", "height", "_height",
            "hitbox", "fold_arrow", "label"
        ]
        
        def __init__(self, name, width, components, parent, collapsed:bool=True):
            self.parent = parent
            self.name = name
            self.width = width
            self.components = components
            self.collapsed = collapsed
            self.height = 15
            self._height = 15
            self.hitbox = Button(0, 0, width, 15)
            self.fold_arrow = DirectoryTree.folds["closed" if collapsed else "open"]
            self.label = Text(14, -1, width-14, name, text_size=12, text_bg_color=None)
            self.hitbox.on_left_click = self._toggle
            
        def get_expanded(self) -> dict:
            if self.collapsed: return {}

            d = {}
            for f in self.components:
                if isinstance(f, DirectoryTree.Folder):
                    d.update(f.get_expanded())

            return {self.name: d}
        
        def expand_tree(self, tree):

            if self.collapsed:
                self._toggle(None)
                
            for f in self.components:
                if isinstance(f, DirectoryTree.Folder) and (f.name in tree.keys()):
                    f.expand_tree(tree[f.name])

        def _toggle(self, editor): # "editor" is an argument as it is passed by the button this function is bound to
            self.collapsed = not self.collapsed
            self.fold_arrow = DirectoryTree.folds["closed" if self.collapsed else "open"]
        
        def _update(self, editor, X, Y, x_offset=0):
            self.fold_arrow._update(editor, X+x_offset, Y)
            self.label._update(editor, X+x_offset, Y)

            if self.collapsed:
                self.height = self._height

            else:
                self.height = self._height
                for component in self.components:
                    component: DirectoryTree.Folder | DirectoryTree.File
                    component._update(editor, X, Y+self.height, x_offset+10)
                    self.height += component.height
        
        def _event(self, editor, X, Y, x_offset=0):
            self.hitbox._event(editor, X, Y)
            
            if self.collapsed:
                self.height = self._height

            else:
                self.height = self._height
                for component in self.components:
                    component: DirectoryTree.Folder | DirectoryTree.File
                    component._event(editor, X, Y+self.height, x_offset+10)
                    self.height += component.height

    class File(UIElement):
        __slots__ = [
            "parent", "name", "width", "on_click", "icon", "height",
            "hitbox", "label"#, "rct"
        ]
        
        def __init__(self, name, on_click, icon, width, parent, on_right_click=None):
            self.parent = parent
            self.name = name
            self.width = width
            self.on_click = on_click
            self.icon = DirectoryTree.file_icons[icon]
            self.height = 15
            self.hitbox = Button(0, 0, width, 15, "", (255, 0, 0))
            self.label = Text(14, -1, width-14, name, text_size=12, text_bg_color=None)
            self.hitbox.on_left_click = on_click
            if on_right_click:
                self.hitbox.on_right_click = on_right_click

        def _update(self, editor, X, Y, x_offset=0):
            self.icon._update(editor, X+x_offset, Y)
            self.label._update(editor, X+x_offset, Y)
        
        def _event(self, editor, X, Y, x_offset=0):
            self.hitbox._event(editor, X, Y)

    def _get_icon_for_file(self, file_name):
        if file_name.endswith((".ds", ".dungeon_script")):
            return "ds"
        
        elif file_name.endswith(".combat"):
            return "combat"
        
        elif file_name.endswith(".json"):
            return "json"
        
        return "default"

    def parse_components(self, name, tree, parent):
        if isinstance(tree, dict):
            comps = []
            for k, v in tree.items():
                comps.append(self.parse_components(k, v, parent))

            return DirectoryTree.Folder(name, self.width, comps, parent)
        
        else:
            if hasattr(tree, "rmb_click"):
                return DirectoryTree.File(name, tree, self._get_icon_for_file(name), self.width, parent, tree.rmb_click)

            else:
                return DirectoryTree.File(name, tree, self._get_icon_for_file(name), self.width, parent)

    def __init__(self, x, y, name, components:dict, width, editor):
        self.x = x
        self.y = y
        self.name = name
        self.expanded = False
        self.width = width
        self.children = []
        self._height = 0
        self.height = 0
        self.components = []
        
        for name, comp in components.items():
            self.components.append(self.parse_components(name, comp, self))
        
        self.surface = Scrollable(self.x, self.y, 225, editor.height-42, (24, 24, 24), left_bound=0, top_bound = 0)
        self.children.append(self.surface)
        self.folder = DirectoryTree.Folder(self.name, width, self.components, self, False)
        self.surface.children.append(self.folder)

    def get_expanded(self):
        return self.folder.get_expanded()

    def expand_tree(self, tree):
        self.folder.expand_tree(tree["DUNGEONS"])

    def _update_layout(self, editor):
        self.surface.height = editor.height-42

    def _update(self, editor, X, Y):
        for child in self.children:
            child._update(editor, X, Y)
    
    def _event(self, editor, X, Y):

        for child in self.children[::-1]:
            child._event(editor, X, Y)

