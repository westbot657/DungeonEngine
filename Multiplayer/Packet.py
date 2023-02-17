# pylint: disable=[W,R,C,import-error]


class Packet:
    _content_builders = {}

    def __init__(self, source, content):
        self.source = source
        self.content = content

    @classmethod
    def build(cls, source, content):
        ...
