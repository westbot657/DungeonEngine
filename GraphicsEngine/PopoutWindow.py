# pylint: disable=[W,R,C,no-member, import-error]

from UIElement import UIElement
from NumberedTextArea import NumberedTextArea
from FileEditor import FileEditor
from Text import Text
from FunctionalElements import BorderedButton
from Popup import Popup
from Editor import Editor
from WindowFrame import WindowFrame
from Util import PopoutElement, safe_eval
from Organizers import Link
from PlatformDependencies import gw, macOSfocusWindow, macOSgetWindowPos, macOSsetWindow, get_monitors

from mergedeep import merge
from subprocess import Popen
from threading import Thread
import socket
import Stockings
import json
import sys
import platform
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import time
import pygame

pygame.init()

class PopoutBehaviorPreset(UIElement):
    def __init__(self, preset:str, data, editor, popout):
        self.preset = preset
        self.children = []
        
        match preset:
            case "file-editor":
                w = 350
                h = 75
                popout.frame.window_limits = [400, 300, 1920, 1080]
                self.file_path = data["file_path"]
                self.text_editor = NumberedTextArea(5, 21, 240, 208)
                self.children.append(self.text_editor)
                
                match self.file_path.rsplit(".", 1)[-1]:
                    case "json"|"piskel":
                        self.text_editor.editable.color_text = FileEditor.json_colors
                    case "ds"|"dungeon_script"|"dse":
                        self.text_editor.editable.color_text = FileEditor.ds_colors
                    case "md":
                        self.text_editor.editable.color_text = FileEditor.md_colors
                
                self._popup_save_label = Text(0, 15, content="You have unsaved changes!")
                self._popup_save_label.x = (w/2) - (self._popup_save_label.width/2)
                
                self._popup_cancel = BorderedButton(0, 45, -1, text=" Cancel ", text_size=13)
                self._popup_save = BorderedButton(100, 45, -1, text=" Save & Close ", text_size=13)
                self._popup_exit = BorderedButton(200, 45, -1, text=" Close anyways ", text_size=13)
                
                overall_width = self._popup_cancel.width + 10 + self._popup_save.width + 10 + self._popup_exit.width
                self._popup_cancel.x = (w/2) - (overall_width/2)
                self._popup_save.x = self._popup_cancel.x + self._popup_cancel.width + 10
                self._popup_exit.x = self._popup_save.x + self._popup_save.width + 10
                
                self.popup = Popup(w, h, [
                    self._popup_save_label,
                    self._popup_cancel,
                    self._popup_save,
                    self._popup_exit
                ])

                
                with open(self.file_path, "r+", encoding="utf-8") as f:
                    self.text_editor.set_content(f.read())

                def _update_layout(*_, **__):
                    self.text_editor.width = editor.width = min(max(300, editor.width), 1920)
                    self.text_editor.height = editor.height = min(max(250, editor.height), 1080)
                    self.text_editor._update_layout()
                
                def on_save(_, content, __, ___):
                    with open(self.file_path, "w+", encoding="utf-8") as f:
                        f.write(content)
                    popout.send(json.dumps({"event": "save"}))

                def on_close():
                    with open(self.file_path, "r+", encoding="utf-8") as f:
                        if self.text_editor.editable.get_content() == f.read():
                            popout.send(json.dumps({"event": "close"}))
                            # popout.close()
                            exit()
                        else:
                            self.popup.popup()
                
                editor.add_event_listener("WINDOW_CLOSED", on_close)
                
                def on_cancel(*_, **__):
                    self.popup.close()
                
                def on_save_exit(*_, **__):
                    with open(self.file_path, "w+", encoding="utf-8") as f:
                        f.write(self.text_editor.editable.get_content())
                    popout.send(json.dumps({"event": "close"}))
                    popout.close()
                    exit()
                    
                def on_exit(*_, **__):
                    popout.send(json.dumps({"event": "close"}))
                    popout.close()
                    exit()


                self._update_layout = _update_layout
                self.text_editor.editable.on_save(on_save)
                self._popup_cancel.on_left_click = on_cancel
                self._popup_save.on_left_click = on_save_exit
                self._popup_exit.on_left_click = on_exit

            case "":
                ...


    # def _update_layout(self, editor): # pylint: disable=method-hidden
    #     pass

    def _event(self, editor, X, Y):
        self._update_layout(editor)

        for child in self.children[::-1]:
            child._event(editor, X, Y)
        

    def _update(self, editor, X, Y):
        for child in self.children:
            child._update(editor, X, Y)


    def file_editor_window_close_event(self):
        ...

class PopoutWindow(UIElement):
    _windows = []
    _port = 10001
    _init = False
    _server = None
    
    @classmethod
    def init(cls):
        if not cls._init:
            cls._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cls._server.bind(("127.0.0.1", cls._port))
            cls._server.listen(5)
        return cls._server
    
    def check_closed(self):
        if hasattr(self.conn, "CLOSED"):
            self.closed = True
    
    def __init__(self, size:tuple[int, int]=..., content:dict[str, dict|list]=..., window_title=""):
        self.children = []
        self.closed = False
        self.ready = False
        if (size != ...) and (content != ...):
            # This branch is run from the main process
            # launch sub-process, set up communication
            # self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            PopoutWindow.init()
            self.ctx = "parent"
            
            PopoutWindow._windows.append(self)
            
            data: dict[str, dict|list] = {
                "size": size,
                "content": merge({"window_title": window_title}, content)
            }
            
            # data["content"].update({"PORT": PopoutWindow._port})
            
            # self.socket.bind(("127.0.0.1", PopoutWindow._port))

            if getattr(sys, "frozen", False):
                Popen(f"\"{sys.executable}\" popout {PopoutWindow._port}")
            else:
                Popen(f"py -3.12 ./GraphicsEngine/ui_library.py popout {PopoutWindow._port}")
            # self.socket.listen(1)
            self.connection, self.conn_addr = PopoutWindow._server.accept()
            # self.socket.setblocking(False)
            self.conn = Stockings.Stocking(self.connection)
            
            # PopoutWindow._port += 1
            # if PopoutWindow._port > 25565:
            #     PopoutWindow._port = 12345
            
            def break_off():
                while not self.conn.handshakeComplete: pass
                self.ready = True
                self.conn.write(json.dumps(data))
                
            t = Thread(target=break_off)
            t.daemon = True
            t.start()

        else:
            # This branch is run in the sub-process
            
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # print(f"client connecting with port: {content["PORT"]}")
            self.socket.connect(("127.0.0.1", content["PORT"]))
            
            self.conn = Stockings.Stocking(self.socket)
            
            while not self.conn.handshakeComplete: pass
            
            self.ctx = "child"
            # content.pop("PORT")
            
            while not (r := self.conn.read()):
                pass
            data = json.loads(r)
            
            content = data["content"]
            size = data["size"]
            
            # print(f"{size=}")
            self.editor = Editor(None, None, *size)
            self.window_title = content.get("window_title", "")
            self.editor._caption = self.window_title
            self.frame = WindowFrame(*size, self.editor, content.get("window_limits", ...), title=self.window_title)
            comps = {
                "editor": self.editor,
                "frame": self.frame
            }

            self.editor.add_layer(5, self.frame)
            if "behavior" in content:
                # print(f"Using behavior preset! ({content})")
                self.preset = PopoutBehaviorPreset(content["behavior"], content["data"], self.editor, self)
                self.children.append(self.preset)
                
                self.editor.add_layer(0, self)
            else:
                for name, comp in content["components"].items():
                    if comp["type"] in PopoutElement._elements:
                        comps.update({name: PopoutElement._elements[comp["type"]](*comp.get("args", []), **comp.get("kwargs", {}))})
                
                for link in content["links"]:
                    link: dict
                    # print(f"creating link: {link}")
                    if "link_handler" in link:
                        e = link.pop("link_handler")
                        # ctx = {
                        #     "parent": comps[link["parent"]]
                        #     "child": comps[link["child"]]
                        # }
                        l = lambda a: safe_eval(e, {"a": a})
                    else:
                        l = lambda a: a
                    self.children.append(
                        Link(
                            comps[link.pop("parent")],
                            comps[link.pop("child")],
                            **link,
                            link_handler = l
                        )
                    )
                    
                self.components = comps

                self.editor.add_layer(0, self)
                
                for layer, objs in content["editor_layers"].items():
                    self.editor.add_layer(int(layer), *[comps[name] for name in objs])
            
            self.editor.run()

    def _event(self, editor, X, Y):
        self.check_closed()
        if (self.ctx == "parent") and (not self.ready): return
        if self.closed: return
        if self.ctx == "child":
            for c in self.children[::-1]:
                c._event(editor, X, Y)
        try:
            if io := self.conn.read():
                if self.ctx == "parent":
                    ...
                else:
                    if io == "%close%":
                        self.conn.close()
                        pygame.quit()
                        exit()
                    elif io == "%focus%":
                        if platform.system() == "Windows":
                            try:
                                window = gw.getWindowsWithTitle(self.window_title)[0]
                                # window.activate()
                                window.alwaysOnTop(True)
                                window.alwaysOnTop(False)
                            except: pass
                        elif platform.system() == "Darwin":
                            macOSfocusWindow(self.window_title)
                    
                    elif io.startswith("{"):
                        data = json.loads(io)
                        
                        if data.get("event", None) == "close":
                            self.closed = True
                        # print(f"recieved data: {data}")
                        # for key, val in data.items():
                        #     if key == "interface-cmd":
                        #         PopoutInterface.execute(val, self.components, self)
        except BrokenPipeError:
            if self.ctx == "parent":
                self.closed = True
            else:
                pygame.quit()
                exit()

    def _update(self, editor, X, Y):
        if self.ctx == "child":
            for child in self.children:
                child._update(editor, X, Y)
    
    def send(self, data):
        self.check_closed()
        
        if not self.closed:
            try:
                self.conn.write(data)
            except BrokenPipeError:
                self.closed = True

    def await_read(self, timeout=-1) -> str|None:
        self.check_closed()
        t = time.time()
        while True:
            if time.time() - t > timeout > 0:
                return None
            try:
                r = self.conn.read()
                if r:
                    return r
            except BrokenPipeError:
                self.closed = True
                return None
    
    def read(self):
        self.check_closed()
        try:
            return self.conn.read()
        except BrokenPipeError:
            self.closed = True
            return None

    def close(self): # This method can only be called from the main process
        self.conn.write("%close%")
        self.closed = True
        try:
            while self.conn.writeDataQueued(): pass
        except OSError:
            pass
        try:
            self.conn.close()
        except OSError:
            pass

