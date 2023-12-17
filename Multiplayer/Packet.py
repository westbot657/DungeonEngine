# pylint: disable=[W,R,C]

import json

class Packet:
    backlog = ""
    socket = None
    
    @classmethod
    def next(cls) -> dict|None:
        while True:
            if "&e" in cls.backlog:
                packet, cls.backlog = cls.backlog.split("&e", 1)
                packet = packet.replace("&a", "&")

                try:
                    return json.loads(packet)
                except json.JSONDecodeError:
                    return None
            cls.backlog += cls.socket.recv(1024).decode()
    
    @classmethod
    def send(cls, data:dict):
        cls.socket.send((json.dumps(data).replace("&", "&a") + "&e").encode())

