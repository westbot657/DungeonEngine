# pylint: disable=[W,R,C]

try:
    from GraphicsEngine.Options import DO_RICH_PRESENCE, client_id
except ImportError:
    from Options import DO_RICH_PRESENCE, client_id
    
# discord presence for game
from pypresence import Presence
from mergedeep import merge

import time


class fake_presence:
    def __init__(self, *_, **__): pass
    def update(self, *_, **__): pass
    def connect(self, *_, **__): pass


if DO_RICH_PRESENCE:
    RPC = Presence(client_id)
else:
    RPC = fake_presence()
RPC.connect()

class DiscordPresence(dict):
    def __init__(self, rpc):
        self.RPC = rpc
        self.active = {"default": {}}
        self.activity = "default"
        self.old = []
        self.default = {
            "details": "Testing <Insert Dungeon Name Here>",
            "state": "debugging",
            "start": time.time(),
            "large_image": "dungeon_builder_icon",
            "large_text": "<Insert Dungeon Name Here>"
        }
        self.update()
        
    def update(self, *_, **__):
        self.RPC.update(*merge({}, self.default, self.active[self.activity]))
        
    def start_activity(self, id, **kwargs):
        self.active.update({id: kwargs})
        self.old.insert(0, self.activity)
        self.activity = id
        self.update()
    
    def end_activity(self, id):
        if id in self.active:
            self.activity = id
            self.active.pop(id)
        self.update()
        
    def __dict__(self):
        return {}
        
    def __setitem__(self, item, value):
        return self.active[self.activity].__setitem__(item, value)
    
    def __getitem__(self, item):
        return self.active[self.activity].__getitem__(item)

    def modify_activity(self, id, **kwargs):
        if id in self.active:
            self.active[id].update(kwargs)

RPCD = DiscordPresence(RPC)
RPC = RPCD