# pylint: disable=W,R,C,import-error

from LoadingBar import LoadingBar
from Toasts import Toasts
from FunctionalElements import Button
from RenderPrimitives import Image
from Options import PATH

import math
import time
import json
import glob
import os

class VisualConfig:
    
    
    @classmethod
    def analyze_project_structure(cls, root:str, dungeon_id:str) -> list[str]|str:
        """
        returns the list of files returned from glob.glob  \n
        if there are errors with the file structure, returns a string instead
        """
        to_load = []
        
        # issues = []
        
        if not os.path.exists(f"{root}/{dungeon_id}.json"):
            return "Folder does not resemble expected dungeon structure"
        to_load.append(f"{root}/{dungeon_id}.json")
        
        return to_load
    
    @staticmethod
    def blank(*_, **__): pass
    
    @classmethod
    def error(cls, msg:str, loading_bar:LoadingBar, load_toast:Toasts.Toast, toasts:Toasts):
        loading_bar.fill_color = (255, 30, 30)
        loading_bar.set_max_progress(1)
        loading_bar.set_progress(1)
        # loading_bar.width -= 25
        
        ctb_frames = [
            Image(f"{PATH}/advanced_editor/close_button.png", 0, 0, 20, 20),
            Image(f"{PATH}/advanced_editor/close_button_hovered.png", 0, 0, 20, 20)
        ]
        
        close_toast_button = Button(loading_bar.x+loading_bar.width-20, loading_bar.y-25, 20, 20, "", ctb_frames[0], hover_color=ctb_frames[1], click_color=ctb_frames[1])
        toast2 = toasts.toast(msg, 0.1, (255, 30, 30))
        toast2.keep_showing = True
        
        def on_click_button(*_, **__):
            load_toast.remove()
            toast2.keep_showing = False
            close_toast_button.on_left_click = cls.blank
        close_toast_button.on_left_click = on_click_button
        load_toast.children.append(close_toast_button)
    
    
    @classmethod
    def load(cls, root:str, loading_bar:LoadingBar, load_toast:Toasts.Toast, toasts:Toasts):
        root = root.replace("\\", "/")
        
        dungeon_id = root.rsplit("/", 1)[-1]
        
        result = {
            "name": dungeon_id,
            "weapons": [],
            "ammo": [],
            "armor": [],
            "tools": [],
            "items": [],
            "combats": [],
            "enemies": [],
            "rooms": [],
            "roads": [],
            "scripts": [],
            "error": None
        }
        
        result = cls.analyze_project_structure(root, dungeon_id)
        
        if isinstance(result, list):
            ...
        else:
            cls.error(result, loading_bar, load_toast, toasts)
            

