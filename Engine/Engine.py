# pylint: disable=[W,R,C,import-error]
from Resources.AbstractAmmo         import AbstractAmmo
from Resources.AbstractArmor        import AbstractArmor
from Resources.AbstractItem         import AbstractItem
from Resources.AbstractStatusEffect import AbstractStatusEffect
from Resources.AbstractWeapon       import AbstractWeapon



class Engine:
    _engine = None
    def __new__(cls):
        if not cls._engine:
            cls._engine = self = super().__new__(cls)
            
        return cls._engine



