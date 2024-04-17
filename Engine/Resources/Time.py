# pylint: disable=[W,R,C,import-error]

from .Serializer import Serializer, Serializable


import time

@Serializable("Time")
class Time:
    _weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.data = time.localtime(timestamp)
        
        # _wday: weekday, _yday: day of the year, _isdst: is daylight savings time
        self.year, self.month, self.day, self.hour, self.minute, self.second, _wday, _yday, _isdst = self.data
        self.weekday = self._weekdays[_wday]
        
    def serialize(self):
        return Serializer.smartSerialize(self, "year", "month", "day", "hour", "minute", "second", "weekday", "timestamp")
    
    @classmethod
    def deserialize(cls, instance:object, data:dict):
        Serializer.smartDeserialize(instance, data)
        
    def __repr__(self) -> str:
        return time.asctime(self.data)
    
    def getLocalVariables(self) -> dict:
        return {
            ".year": self.year,
            ".month": self.month,
            ".day": self.day,
            ".hour": self.hour,
            ".minute": self.minute,
            ".second": self.second,
            ".weekday": self.weekday,
            ".timestamp": self.timestamp
        }
    
    def updateLocalVariables(self, locals: dict):
        ...