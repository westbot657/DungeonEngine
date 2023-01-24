# pylint: disable=[W,R,C,import-error]


class Util:
    ...

    @staticmethod
    def getRoundedUpKey(key:float, data:dict[float]):
        old = 0
        for v in data:
            if old <= key <= v:
                return v
            old = v

    @staticmethod
    def getRoundedDownKey(key:float, data:dict[float]):
        old = 0
        for v in data:
            if old <= key <= v:
                return old
            old = v

