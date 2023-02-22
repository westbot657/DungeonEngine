# pylint: disable=[W,R,C,import-error]
import socket

class Packet:
    _content_builders = {}
    _queue = []

    def __init__(self, source, content):
        self.source = source
        self.content = content

    @classmethod
    def build(cls, source:socket.socket, address:str, content:str):
        if address not in cls._content_builders:
            cls._content_builders.update({address: ""})
        cls._content_builders[address] += content

        while "\n" in (text := cls._content_builders[address]):
            packet_content, text = text.split("\n", 1)
            packet_content = packet_content.replace("&new;", "\n").replace("&amp;", "&")
            cls._content_builders[address] = text
            packet = cls(source, content)

            cls._queue.append(packet)

    @classmethod
    def nextPacket(cls):
        if cls._queue:
            return cls._queue.pop(0)
        return None



