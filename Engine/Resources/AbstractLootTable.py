# pylint: disable=[W,R,C,import-error]

try:
    from .LootTable import LootTable
    from .Identifier import Identifier
except ImportError:
    from LootTable import LootTable
    from Identifier import Identifier



"""
<id>.json
{
    "entries": [
        {
            "item": "<namespace>:<category>/<item>",
            "<item attribute>": <override value>,
            "<item attribute>": {
                "function": "random",
                "type": "uniform",
                "min": <int>,
                "max": <int>
            },
            "<item attribute>": {
                "function": "random",
                "type": "uniform",
                "choices": [
                    ...
                ]
            }
        }
    ],
    "rolls": {
        "type": "uniform",
        "min": <int>,
        "max": <int>
    }
}
"""

class AbstractLootTable:

    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        

