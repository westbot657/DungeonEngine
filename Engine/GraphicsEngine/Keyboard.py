# pylint: disable=[W,R,C,import-error]

class KeyBoard:

    def __init__(self):
        self.keys = {}

    def _setKeyDown(self, key):
        self.keys.update({key: True})
    
    def _setKeyUp(self, key):
        self.keys.update({key: False})

    def getKeyDown(self, key):
        return self.keys.get(key, False)

    def getKeyUp(self, key):
        return not self.keys.get(key, False)

