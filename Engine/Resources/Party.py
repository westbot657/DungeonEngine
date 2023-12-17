# pylint: disable=[W,R,C]

try:
    from .Serializer import Serializable, Serializer
except ImportError:
    from Serializer import Serializable, Serializer



@Serializable("Party")
class Party:
    
    def __init__(self, host):
        self.host = host
        self.players = [host]

    def addPlayer(self, player):
        self.players.append(player)
    
    def removePlayer(self, player):
        if player in self.players:
            self.players.remove(player)







    def serialize(self) -> dict:
        return {
            "host": Serializer.serialize(self.host),
            "players": Serializer.serialize(self.players)
        }

    @classmethod
    def deserialize(cls, instance, data:dict) -> None:
        Serializer.smartDeserialize(instance, data)


