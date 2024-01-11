# pylint: disable=[W,R,C]

import json
import socket

class Comm:
    _port = 10000
    
    def __init__(self):
        self.backlog = ""
        self.socket = socket.socket
    
    def next(self) -> dict|None:
        while True:
            if "&e" in self.backlog:
                packet, self.backlog = self.backlog.split("&e", 1)
                packet = packet.replace("&a", "&")

                try:
                    return json.loads(packet)
                except json.JSONDecodeError:
                    return None
            self.backlog += self.socket.recv(1024).decode()
    
    def send(self, data:dict):
        self.socket.send((json.dumps(data).replace("&", "&a") + "&e").encode())

