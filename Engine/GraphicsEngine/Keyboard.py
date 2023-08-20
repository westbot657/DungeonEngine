# pylint: disable=[W,R,C,import-error]

import time



class KeyBoard:

    def __init__(self):
        self.keys = {}
        self.unicodes = {}
        self.typing = []

    def _setKeyDown(self, key):
        self.keys.update({key: True})
    
    def _setKeyUp(self, key):
        self.keys.pop(key)

    def _addUnicode(self, unicode):
        if unicode:
            self.unicodes.update({unicode: time.time()})
            self.typing.append(unicode)
        #print(self.unicodes, self.typing)
    
    def _removeUnicode(self, unicode):
        if unicode in self.unicodes:
            self.unicodes.pop(unicode)

    def update(self, engine):
        if self.unicodes:
            t = time.time()

            for key, _time in self.unicodes.items():
                diff = t - _time

                if diff >= 0.8:
                    if int((diff * 100) % 5) == 0:
                        self.typing.append(key)

    def getKeyDown(self, key):
        return self.keys.get(key, False)

    def getKeyUp(self, key):
        return not self.keys.get(key, False)
