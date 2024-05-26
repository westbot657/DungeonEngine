# pylint: disable=W,R,C,import-error

from LoadingBar import LoadingBar
from Toasts import Toasts
from FunctionalElements import Button
from RenderPrimitives import Image
from Options import PATH

from typing import Any

import math
import time
import json
import glob
import os
import re

class VisualLoader:
    
    _engine_loaded = False
    _engine_editable = False
    
    class ObjectReference:
        def __init__(self, ref_id:str):
            self.ref_id = ref_id
            self.broken_reference = False
        
        def get_ref(self):
            return VisualLoader._refernce_map[self.ref_id.split(":", 1)[0]][self.ref_id]
    
        def get(self, data_name:str):
            self.get_ref().get(data_name)
    
        def set_ref(self, ref_id:str):
            self.ref_id = ref_id
        
        def set(self, data_name:str, value:Any):
            self.get_ref().set(data_name, value)
        
        def verify(self):
            valid = self.ref_id in VisualLoader._refernce_map[self.ref_id.split(":", 1)[0]].keys()
            self.broken_reference = not valid
            return valid
    
    class InheretenceLink:
        def __init__(self, reference, attr:str, fallback:dict=None):
            self.reference: VisualLoader.ObjectReference = reference
            self.attr = attr
            
            self.has_fallback = False
            self.fallback = None
            if fallback and self.attr in fallback.keys():
                self.has_fallback = True
                self.fallback = fallback[self.attr]
    
        def get(self):
            if self.reference:
                return self.reference.get(self.attr)
            else:
                return self.fallback
        
        def set(self, value:Any):
            if self.reference:
                self.reference.set(self.attr, value)
            elif self.has_fallback:
                self.fallback = value
        
        def verify(self):
            return bool(self.reference) or self.has_fallback
    
    class VisualObject:
        def __init__(self, source:str, dungeon:str, uid:str, data:dict, locked:bool=False):
            self.source = source
            self.dungeon = dungeon
            self.uid = uid
            self.data = data
            self.locked = locked
            
            VisualLoader._refernce_map[self.dungeon].update({self.uid: self})
        
        def __repr__(self):
            return f"VisualObject( {self.uid} )"
        
        def ref(self):
            return VisualLoader.ObjectReference(self.uid)
    
        def get(self, data_name:str, default=None):
            if data_name in self.data:
                obj = self.data[data_name]
                if isinstance(obj, VisualLoader.ObjectReference):
                    return obj.get()
                return obj
            return default
        
        def set(self, data_name:str, value:Any):
            self.data.update({data_name: value})
        
        def verify(self):
            results = []
            
            for key, val in self.data.items():
                if isinstance(val, (VisualLoader.ObjectReference, VisualLoader.InheretenceLink, VisualLoader.VisualObject)):
                    results.append(val.verify())

            return all(results)

    class MissingValue:
        _instance = None
        def __new__(cls):
            if not cls._instance:
                cls._instance = super().__new__(cls)
            return cls._instance
    
        def split(self, *args, **kwargs):
            return "[unnamed]".split(*args, **kwargs)

        def __str__(self):
            return "[unnamed]"
        
        def lower(self):
            return "[unnamed]"
    
    _refernce_map: dict[str, dict[str, VisualObject]] = {}
        
    @classmethod
    def analyze_project_structure(cls, root:str, dungeon_id:str) -> list[str]|str:
        """
        returns the list of files returned from glob.glob  \n
        if there are errors with the file structure, returns a string instead
        """
        to_load: list[str] = []
        
        # issues = []
        
        if not os.path.exists(f"{root}/{dungeon_id}.json"):
            return f"Folder does not contain a '{dungeon_id}.json' file."
        # to_load.append(f"{root}/{dungeon_id}.json")
        
        to_load += glob.glob("**/*.ds", root_dir=root, recursive=True) + \
                   glob.glob("**/*.dungeon_script", root_dir=root, recursive=True) + \
                   glob.glob("**/*.json", root_dir=root, recursive=True)
        
        if f"{root}/vcfg.json" in to_load:
            to_load.remove(f"{root}/vcfg.json")
        
        return [t.replace("\\", "/") for t in to_load]
    
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
    
    _category_map = {
        "weapons": "weapon",
        "enemies": "enemy",
        "tools": "tool",
        "items": "item",
        "attacks": "attack",
        "combats": "combat",
        "status_effects": "status_effect"
    }
    
    @classmethod
    def load(cls, root:str, loading_bar:LoadingBar, load_toast:Toasts.Toast, toasts:Toasts, aesa, loading_engine=False):
        
        if not cls._engine_loaded:
            load_toast.text_dsiplay.set_content("Loading Engine resources...")
            cls._engine_loaded = True
            cls.load("./", loading_bar, load_toast, toasts, aesa, True)
            load_toast.text_dsiplay.set_content("Loading dungeon...")

        root = root.replace("\\", "/")
        dungeon_id = root.rsplit("/", 1)[-1]
        
        if dungeon_id in cls._refernce_map.keys():
            toasts.toast("dungeon already loaded.")
            load_toast.remove()
            return
        
        if loading_engine:
            dungeon_id = "engine"
            result = [f"resources/{f}".replace("\\", "/") for f in (glob.glob("**/*.json", root_dir="./resources", recursive=True) +\
                     glob.glob("**/*.ds", root_dir="./resources", recursive=True) + \
                     glob.glob("**/*.dundeon_script", root_dir="./resources", recursive=True))]
            # print(f"engine load: {result}")
        else:
            result = cls.analyze_project_structure(root, dungeon_id)
        
        
        if not isinstance(result, list):
            cls.error(result, loading_bar, load_toast, toasts)
        else:
            loading_bar.set_max_progress(len(result))
            
            cls._refernce_map.update({dungeon_id: {}})
            
            cls.build_visuals(root, loading_bar, load_toast, toasts, result, dungeon_id, aesa, loading_engine)

    @classmethod
    def build_visuals(cls, root, loading_bar, load_toast, toasts, result, dungeon_id, aesa, loading_engine:bool):
        loaded = 0
        for file_name in result:
            fn = file_name.replace("resources/", "").replace(".json", "")
            if file_name.endswith(".json"): # weapon/tool/armor/etc
                # print(file_name)
                with open(f"{root}/{file_name}", "r+", encoding="utf-8") as f:
                    data: dict[str, Any] = json.load(f)
                # analyze files, look for external references
                if file_name.startswith("resources/weapons/"):
                    if "parent" in data:
                        parent = VisualLoader.ObjectReference(data["parent"])
                        vdata = {
                            "template": data.get("template", False),
                            "parent": parent,
                            "name": data.get("name", VisualLoader.MissingValue()),
                            "damage": VisualLoader.InheretenceLink(parent, "damage", data),
                            "range": VisualLoader.InheretenceLink(parent, "range", data),
                            "max_durability": VisualLoader.InheretenceLink(parent, "max_durability", data),
                            "durability": VisualLoader.InheretenceLink(parent, "durability", data)
                        }
                    else:
                        vdata = {
                            "template": data.get("template", False),
                            "parent": VisualLoader.MissingValue(),
                            "name": data.get("name", VisualLoader.MissingValue()),
                            "damage": data.get("damage", VisualLoader.MissingValue()),
                            "range": data.get("range", VisualLoader.MissingValue()),
                            "max_durability": data.get("max_durability", VisualLoader.MissingValue()),
                            "durability": data.get("durability", VisualLoader.MissingValue())
                        }

                    VisualLoader.VisualObject(file_name, dungeon_id, f"{dungeon_id}:{fn}", vdata, loading_engine)

                elif file_name.startswith("resources/ammo/"):
                    if "parent" in data:
                        parent = VisualLoader.ObjectReference(data["parent"])
                        vdata = {
                            "template": data.get("template", False),
                            "parent": parent,
                            "name": data.get("name", VisualLoader.MissingValue()),
                            "description": VisualLoader.InheretenceLink(parent, "description", data),
                            "bonus_damage": VisualLoader.InheretenceLink(parent, "bonus_damage", data),
                            "max_count": VisualLoader.InheretenceLink(parent, "max_count", data),
                            "count": VisualLoader.InheretenceLink(parent, "count", data)
                        }
                    else:
                        vdata = {
                            "template": data.get("template", False),
                            "parent": VisualLoader.MissingValue(),
                            "name": data.get("name", VisualLoader.MissingValue()),
                            "description": data.get("description", VisualLoader.MissingValue()),
                            "bonus_damage": data.get("bonus_damage", VisualLoader.MissingValue()),
                            "max_count": data.get("max_count", VisualLoader.MissingValue()),
                            "count": data.get("count", VisualLoader.MissingValue()),
                        }

                    VisualLoader.VisualObject(file_name, dungeon_id, f"{dungeon_id}:{fn}", vdata, loading_engine)

                elif file_name.startswith("resources/armor/"):
                    if "parent" in data:
                        parent = VisualLoader.ObjectReference(data["parent"])
                        vdata = {
                            "template": data.get("template", False),
                            "parent": parent,
                            "name": data.get("name", VisualLoader.MissingValue()),
                            "description": VisualLoader.InheretenceLink(parent, "description", data),
                            "damage_reduction": VisualLoader.InheretenceLink(parent, "damage_reduction", data),
                            "max_durability": VisualLoader.InheretenceLink(parent, "max_cdurability", data),
                            "durability": VisualLoader.InheretenceLink(parent, "durability", data),
                            "events": VisualLoader.InheretenceLink(parent, "events", data)
                        }
                    else:
                        vdata = {
                            "template": data.get("template", False),
                            "parent": VisualLoader.MissingValue(),
                            "name": data.get("name", VisualLoader.MissingValue()),
                            "description": data.get("description", VisualLoader.MissingValue()),
                            "damage_reduction": data.get("damage_reduction", VisualLoader.MissingValue()),
                            "max_durability": data.get("max_cdurability", VisualLoader.MissingValue()),
                            "durability": data.get("durability", VisualLoader.MissingValue()),
                            "events": data.get("events", VisualLoader.MissingValue())
                        }

                    VisualLoader.VisualObject(file_name, dungeon_id, f"{dungeon_id}:{fn}", vdata, loading_engine)
                    
                elif file_name.startswith("resources/tools/"):
                    if "parent" in data:
                        parent = VisualLoader.ObjectReference(data["parent"])
                        vdata = {
                            "template": data.get("template", False),
                            "parent": parent,
                            "name": data.get("name", VisualLoader.MissingValue()),
                            "description": VisualLoader.InheretenceLink(parent, "description", data),
                            "data": VisualLoader.InheretenceLink(parent, "data", data),
                            "max_durability": VisualLoader.InheretenceLink(parent, "max_cdurability", data),
                            "durability": VisualLoader.InheretenceLink(parent, "durability", data),
                            "events": VisualLoader.InheretenceLink(parent, "events", data)
                        }
                    else:
                        vdata = {
                            "template": data.get("template", False),
                            "parent": VisualLoader.MissingValue(),
                            "name": data.get("name", VisualLoader.MissingValue()),
                            "description": data.get("description", VisualLoader.MissingValue()),
                            "data": data.get("data", VisualLoader.MissingValue()),
                            "max_durability": data.get("max_cdurability", VisualLoader.MissingValue()),
                            "durability": data.get("durability", VisualLoader.MissingValue()),
                            "events": data.get("events", VisualLoader.MissingValue())

                        }

                    VisualLoader.VisualObject(file_name, dungeon_id, f"{dungeon_id}:{fn}", vdata, loading_engine)
                    
                elif file_name.startswith("resources/items/"):
                    if "parent" in data:
                        parent = VisualLoader.ObjectReference(data["parent"])
                        vdata = {
                            "template": data.get("template", False),
                            "parent": parent,
                            "name": data.get("name", VisualLoader.MissingValue()),
                            "description": VisualLoader.InheretenceLink(parent, "description", data),
                            "data": VisualLoader.InheretenceLink(parent, "data", data),
                            "events": VisualLoader.InheretenceLink(parent, "events", data),
                            "max_count": VisualLoader.InheretenceLink(parent, "max_count", data),
                            "count": VisualLoader.InheretenceLink(parent, "count", data)
                        }
                    else:
                        vdata = {
                            "template": data.get("template", False),
                            "parent": VisualLoader.MissingValue(),
                            "name": data.get("name", VisualLoader.MissingValue()),
                            "description": data.get("description", VisualLoader.MissingValue()),
                            "data": data.get("data", VisualLoader.MissingValue()),
                            "events": data.get("events", VisualLoader.MissingValue()),
                            "max_count": data.get("max_count", VisualLoader.MissingValue()),
                            "count": data.get("count", VisualLoader.MissingValue()),
                        }

                    VisualLoader.VisualObject(file_name, dungeon_id, f"{dungeon_id}:{fn}", vdata, loading_engine)
                    
                elif file_name.startswith("resources/enemies/"):
                    ...
                elif file_name.startswith("resources/attacks/"):
                    ...
                elif file_name.startswith("resources/status_effects/"):
                    ...
                elif file_name.startswith("resources/sounds/"):
                    ...
                elif file_name.startswith("resources/loot_tables/"):
                    ...
                elif file_name.startswith("resources/interactable/"):
                    ...
            elif file_name.endswith((".ds", ".dungeon_script")): # script
                ... # compile the scripts and analyze the tokens for references

            loaded += 1
            loading_bar.set_progress(loaded)


        missing = []
        
        if not loading_engine:
            if os.path.exists(f"{root}/vcfg.json"):
                with open(f"{root}/vcfg.json", "r+", encoding="utf-8") as f:
                    config = json.load(f)
            else:
                with open(f"{root}/vcfg.json", "w+", encoding="utf-8") as f:
                    f.write("{}")
                config = {}
        else:
            config = {}

        load_toast.text_dsiplay.set_content("Building Panels...")
        for id, ref in VisualLoader._refernce_map[dungeon_id].items():
            if not ref.verify():
                missing.append(ref)
            
            if id not in config:
                config.update({id: "stashed"})
            cat = re.match(f"(?:{dungeon_id}:)(?P<category>[^/]+)(?:/)", id).groupdict()["category"]
            category = cls._category_map.get(cat, cat)
            panel_data = {"ref": ref, "type": f"{category}-base"}
            if config[id] == "stashed":
                aesa.create_stashed_panel(category, (300, 400), ref.get("name", id), id, True, ref.get("keywords", []) + [dungeon_id], panel_data=panel_data)
            
            else:
                aesa.create_panel(category, (config[id][0], config[id][1], 300, 400), ref.get("name", id), id, True, ref.get("keywords", []) + [dungeon_id], panel_data=panel_data)

        toasts.toast(f"Panels loaded!" + (f"\n{len(missing)} object{'s have' if len(missing) > 1 else " has"} broken or unloaded references." if missing else ""))

        # print(missing)
        # print(cls._refernce_map)

        if not loading_engine:
            with open(f"{root}/vcfg.json", "w+", encoding="utf-8") as f:
                json.dump(config, f)

        load_toast.keep_showing = False

