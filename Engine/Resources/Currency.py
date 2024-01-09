# pylint: disable=[W,R,C,import-error]

try:
    from .EngineErrors import CurrencyError
    from .Serializer import Serializer, Serializable
except ImportError:
    from EngineErrors import CurrencyError
    from Serializer import Serializer, Serializable

@Serializable("Currency")
class Currency:

    def __init__(self, gold=0, silver=0, copper=0):
        self.gold = gold
        self.silver = silver
        self.copper = copper

    def __repr__(self):
        if self.gold + self.silver + self.copper == 0:
            return "[No Money]"
        return ((f"{self.gold} Gold  " if self.gold else "") + (f"{self.silver} Silver  " if self.silver else "") + (f"{self.copper} Copper" if self.copper else "")).strip()

    def __int__(self):
        return self.copper + (10*self.silver) + (100*self.gold)

    def __eq__(self, other):
        return int(self) == int(other)

    def __ne__(self, other):
        return int(self) != int(other)

    def __lt__(self, other):
        return int(self) < int(other)

    def __gt__(self, other):
        return int(self) > int(other)

    def __le__(self, other):
        return int(self) <= int(other)

    def __ge__(self, other):
        return int(self) >= int(other)

    def __add__(self, other):
        if isinstance(other, Currency):
            return Currency(self.gold+other.gold, self.silver+other.silver, self.copper+other.copper)
        elif isinstance(other, int):
            g = other // 100
            s = (other % 100) // 10
            c = (other % 100) % 10
            return Currency(self.gold+g, self.silver+s, self.copper+c)

    def __sub__(self, other):
        if isinstance(other, Currency):
            c = Currency(self.gold-other.gold, self.silver-other.silver, self.copper-other.copper)
            c.convert_positive()
            return c

    def getLocalVariables(self):
        d = {
            "gold": self.gold,
            "silver": self.silver,
            "copper": self.copper
        }
        return d

    def convert(self, conversion, target=1):
        g = self.gold
        s = self.silver
        c = self.copper

        while True:
            match conversion:
                case "g->s":
                    if s >= target: break
                    if g > 0:
                        g -= 1
                        s += 10
                    elif c >= 10:
                        c -= 10
                        s += 1
                    else:
                        raise CurrencyError("Not enough currency to convert!")
                case "g->c":
                    if c >= target: break
                    if g > 0:
                        g -= 1
                        c += 100
                    elif s > 0:
                        s -= 1
                        c += 10
                    else:
                        raise CurrencyError("Not enough currency to convert!")
                case "s->g":
                    if g >= target: break
                    if s >= 10:
                        s -= 10
                        g += 1
                    elif c >= 100:
                        c -= 100
                        g += 1
                    elif c >= 10:
                        c -= 10
                        s += 1
                    else:
                        raise CurrencyError("Not enough currency to convert!")
                case "s->c":
                    if c >= target: break
                    if s > 0:
                        s -= 1
                        c += 10
                    elif g > 0:
                        g -= 1
                        c += 100
                    else:
                        raise CurrencyError("Not enough currency to convert!")
                case "c->g":
                    if g >= target: break
                    if c >= 100:
                        c -= 100
                        g += 1
                    elif s >= 10:
                        s -= 10
                        g += 1
                    elif c >= 10:
                        c -= 10
                        s += 1
                    else:
                        raise CurrencyError("Not enough currency to convert!")
                case "c->s":
                    if s >= target: break
                    if c >= 10:
                        c -= 10
                        s += 1
                    elif g > 0:
                        g -= 1
                        s += 10
                    else:
                        raise CurrencyError("Not enough currency to convert!")
        
        self.gold = g
        self.silver = s
        self.copper = c

    def convert_positive(self):
        # for when a > b, so you do a - b to get c, and then c has -2 gold, 300 silver, and -6 copper (or something like that)
        # This function assumes that each property can be converted to make each value >= 0
        
        self.convert("s->g", 0)
        self.convert("c->s", 0)
        self.convert("s->c", 0)

    def maximize(self):
        while self.copper >= 10:
            self.copper -= 10
            self.silver += 1
        
        while self.silver >= 10:
            self.silver -= 10
            self.gold += 1

    def get_save(self):
        return [self.gold, self.silver, self.copper]

    def serialize(self):
        return {
            "gold": Serializer.serialize(self.gold),
            "silver": Serializer.serialize(self.silver),
            "copper": Serializer.serialize(self.copper)
        }
    
    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)
