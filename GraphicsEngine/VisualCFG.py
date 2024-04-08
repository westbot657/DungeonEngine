# pylint: disable=W,R,C


class VisualCFG:
    
    @classmethod
    def load(cls, root:str):
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
            "scripts": []
        }

