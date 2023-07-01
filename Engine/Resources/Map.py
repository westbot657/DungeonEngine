# pylint: disable=[W,R,C,import-error]

try:
    from .Location import Location
    from .Position import Position
    from .Region import Region
except ImportError:
    from Location import Location
    from Position import Position
    from Region import Region


class Map:

    def __init__(self, **kwargs):
        """
        referance `Map.draw()` for valid arguments to `kwargs`
        """

        self.map = {}
        self.regions = []

        self.draw(**kwargs)

    def draw(self, **kwargs):
        """
        kwargs: 
            floors must use the following naming styles:
            - `floor_<n>`
            - `basement[_<n>]`\n
            maps are drawn in ascii art, special grid spaces can be labeled with a key (use kwarg `'key'`)

        ex:
        ```
        Map().draw(
            floor_1 = [
                "#########",
                "#   @   #",
                "#     ++#",
                "#:    ++#",
                "####=####"
            ],
            basement_1 = [
                "~########",
                "~#      #",
                "~#   $$ #",
                "#:   $$ #",
                "#       #",
                "#########"
            ]
            key = {
                "#": "engine:map/wall",
                "=": "engine:map/door",
                "@": "engine:map/enemy_spawn_space",
                "+": "engine:map/difficult_terrain",
                "~": "engine:map/filler_space",
                "$": [
                    "engine:map/difficult_terrain",
                    "engine:map/enemy_spawn_space"
                ],
                "floor_1": {
                    ":": "engine:map/stairs/down/south"
                },
                "basement_1": {
                    ":": "engine:map/stairs/up/north"
                }
            }
        )
        ```
        """

        return self

    def getRandomEnemySpawnPosition(self) -> Position:
        if self is None: return Position(0, 0)
        else:
            return Position(0, 0) # WOW! such a random position! :O
