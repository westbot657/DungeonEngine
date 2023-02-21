# pylint: disable=[W,R,C,import-error]
import socket

class Packet:
    _content_builders = {}

    def __init__(self, source, content):
        self.source = source
        self.content = content

    @classmethod
    def build(cls, source:str, content:str):
        if source not in cls._content_builders:
            cls._content_builders.update({source: ""})
        cls._content_builders[source] += content

        if ">" in (text := cls._content_builders[source]):
            ...
