# pylint: disable=[W,R,C]

try:
    from GraphicsEngine.ContextTree import ContextTree
    from GraphicsEngine.Options import TEXT_COLOR, TEXT_BG_COLOR, TEXT_SIZE
    from GraphicsEngine.FileEditor import FileEditor
    from GraphicsEngine.Organizers import LayeredObjects
    from GraphicsEngine.DirectoryTree import DirectoryTree
    from GraphicsEngine.FunctionalElements import Button, Tabs
    from GraphicsEngine.PopoutWindow import PopoutWindow
    from GraphicsEngine.UIElement import UIElement
    from GraphicsEngine.Geometry import Box
except ImportError:
    from ContextTree import ContextTree
    from Options import TEXT_COLOR, TEXT_BG_COLOR, TEXT_SIZE
    from FileEditor import FileEditor
    from Organizers import LayeredObjects
    from DirectoryTree import DirectoryTree
    from FunctionalElements import Button, Tabs
    from PopoutWindow import PopoutWindow
    from UIElement import UIElement
    from Geometry import Box

import os

class Opener:

    def __init__(self, sub_app, file_path, editor):
        self.sub_app = sub_app
        self.file_path = file_path
        self.editor = editor
        self.ctx_tree = ContextTree([
            {
                "Open in popout": self.open_popout
            }
        ], 200, 20, TEXT_COLOR, TEXT_BG_COLOR, (70, 70, 70), TEXT_SIZE, (50, 50, 50), (50, 50, 50), group="main-ctx")

    def __call__(s, *_, **__): # pylint: disable=no-self-argument
        self = s.sub_app
        editor = s.editor
        file_path = s.file_path
        
        n = "  " + file_path.replace("./Dungeons/", "") + "   " #"  " + file_path.rsplit("/", 1)[-1] + "   "

        if n in self.popouts.keys():
            self.popouts[n].send("%close%")
            content = self.popouts[n].await_read()
            self.popouts[n].close()
            self.popouts.pop(n)

        if file_path not in self.open_files.keys():
            new = {file_path: FileEditor(329, 41, editor.width-329, editor.height-62, file_path, file_path.rsplit("/", 1)[-1], editor)}
            self.open_files.update(new)
            self.file_tabs.add_tab(n, [new[file_path]])
            tab = self.file_tabs.get_tab(n)
            self.tabs.append(n)
            ico = LayeredObjects({"0": [
                DirectoryTree.file_icons[DirectoryTree._get_icon_for_file(None, file_path)]
            ]}, 2, 4)
            close_button = Button(tab.width - 15, 1, 14, 14, "X", None, text_size=12)
            close_button.on_left_click = self.tab_remover_getter(n)
            self.file_tabs.add_tab_children(n, (
                ico,
                close_button
            ))

        self.file_tabs.active_tab = n
        self.file_tabs.reset_tab_colors()
        self.focused_file = file_path

    def rmb_click(self, *_, **__):
        self.ctx_tree.openAtMouse(self.editor)

    def open_popout(self, *_, **__):
        self.ctx_tree.close()

        n = "  " + self.file_path.replace("./Dungeons/", "") + "   "

        if n in self.sub_app.popouts:
            self.sub_app.popouts[n].check_closed()
            if self.sub_app.popouts[n].closed:
                self.sub_app.popouts.pop(n)
            else:
                self.sub_app.popouts[n].send("%focus%")
                return

        elif n in self.sub_app.tabs:
            if self.file_path in self.sub_app.open_files:
                self.sub_app.open_files.pop(self.file_path)
            self.sub_app.file_tabs.remove_tab(n)
            self.sub_app.tabs.remove(n)

        p = PopoutWindow((400, 300), {"behavior": "file-editor", "data": {"file_path": self.file_path}}, window_title=n.strip())
        self.sub_app.popouts.update({n: p})

class FileEditorSubApp(UIElement):
    
    def open_folder(self, folder_path, file_opener_getter, editor):
        folder_name = folder_path.replace("\\", "/").rsplit("/", 1)[1]
        tree = list(os.walk(folder_path))
        dir_tree = {
            folder_name: {}
        }

        for path, sub_folders, files in tree:
            path = path.replace("./", "").replace("\\", "/").split("/")
            curr = dir_tree

            for p in path:
                curr = curr[p]
            
            for sub in sub_folders:
                curr.update({sub: {}})
            
            for f in files:
                curr.update({f: file_opener_getter(f"./{'/'.join(path)}/{f}", editor)})
        
        self.dir_tree = DirectoryTree(103, 21, folder_name.replace("./", "").rsplit("/", 1)[-1].upper(), dir_tree[folder_name], 225, editor)

        for c in self.children.copy():

            if isinstance(c, DirectoryTree) and (c is not self.dir_tree):
                i = self.children.index(c)
                self.children.remove(c)
                tree = c.get_expanded()
                self.children.insert(i, self.dir_tree)
                self.dir_tree.expand_tree(tree)
            
    def tab_remover_getter(self, tab_name):
        
        def remove_tab(*_, **__):
            # print(f"{tab_name} - {self.open_files}")
            keys = list(self.open_files.keys())
            self.file_tabs.remove_tab(tab_name)
            i = 0
            for k, c in self.open_files.copy().items():
                
                if k.strip().endswith(tab_name.strip()):
                    self.open_files.pop(k)
                    break
                i += 1

            if self.focused_file == tab_name:
                self.focused_file = None
        
        return remove_tab
        
    def file_opener_getter(self, file_path, editor):
        return Opener(self, file_path, editor)
    
    def __init__(self, code_editor, editor):
        self.code_editor = code_editor
        self.editor = editor
        self.children = []
        self.dir_tree = None
        self.open_files = {}
        self.popouts = {}
        self.tabs = []
        self.focused_file = None
        self.open_folder("./Dungeons", self.file_opener_getter, editor)
        self.children.append(self.dir_tree)
        self.explorer_bar = Box(328, 21, 1, editor.height-42, (70, 70, 70))
        self.children.append(self.explorer_bar)
        self.file_tabs = Tabs(
            329, 41, editor.width-329, 15,
            tab_color_unselected=(24, 24, 24), tab_color_hovered=(31, 31, 31),
            tab_color_selected=(31, 31, 31), tab_color_empty=(24, 24, 24),
            tab_width=100, tab_height=20, scrollable_tabs=True,
            tab_padding=0
        )
        self.children.append(self.file_tabs)
        
    def _update_layout(self, editor):
        self.explorer_bar.height = editor.height-42
        self.file_tabs.width = editor.width-329
        self.dir_tree._update_layout(editor)
        
        if file_editor := self.file_tabs.tab_data.get(self.file_tabs.active_tab, [None])[0]:
            file_editor.width = editor.width-329
            file_editor.height = editor.height-42
            file_editor._update_layout(editor)
        
    def _update(self, editor, X, Y):
        
        for child in self.children:
            child._update(editor, X, Y)
        
    def _event(self, editor, X, Y):

        for child in self.children[::-1]:
            child._event(editor, X, Y)
