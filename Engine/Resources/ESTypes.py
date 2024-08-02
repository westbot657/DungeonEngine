# pylint: disable=W,R,C,import-error



class ESType:
    _types = {}

    def __init__(self, name:str, data_table:dict[str, tuple[str, str, str|tuple[str, str]]]):
        self.name = name
        # data table format: attribute: (data type, object type, access rules)
        
        # access rules:
        #  r: read only
        #  w: write only
        #  rw: read and write
        #  (w/rw, t): writable if type is t
        
        self.data_table = data_table



    @classmethod
    def init(cls):
        
        ### BASIC TYPES ###
        
        cls.t_string = cls("string", {
            "capitalize": ("str",       "callable", "r"),
            "endswith":   ("bool",      "callable", "r"),
            "find":       ("int|none",  "callable", "r"),
            "format":     ("str",       "callable", "r"),
            "index":      ("int|none",  "callable", "r"),
            "join":       ("str",       "callable", "r"),
            "lower":      ("str",       "callable", "r"),
            "replace":    ("str",       "callable", "r"),
            "split":      ("list[str]", "callable", "r"),
            "startswith": ("bool",      "callable", "r"),
            "strip":      ("str",       "callable", "r"),
            "upper":      ("str",       "callable", "r"),
        })
        
        cls.t_int = cls("int", {
            "clamp": ("int|float", "callable", "r"),
            "abs":   ("int",       "callable", "r"),
        })
        
        
        cls.t_float = cls("float", {
            "clamp": ("int|float", "callable", "r"),
            "abs":   ("float",     "callable", "r"),
        })
        
        cls.t_bool = cls("bool", {
        })
        
        cls.t_list = cls("list", {
            "append":   ("none",      "callable", "r"),
            "clear":    ("none",      "callable", "r"),
            "copy":     ("list[any]", "callable", "r"),
            "count":    ("int",       "callable", "r"),
            "index":    ("int|none",  "callable", "r"),
            "insert":   ("none",      "callable", "r"),
            "pop":      ("any",       "callable", "r"),
            "remove":   ("none",      "callable", "r"),
            "reverse":  ("none",      "callable", "r"),
            "reversed": ("list[any]", "callable", "r"),
            "sort":     ("none",      "callable", "r"),
            "sorted":   ("list[any]", "callable", "r"),
            "as_set":   ("list[any]", "callable", "r"),
        })
        
        cls.t_dict = cls("dict", {
            "clear":  ("none",                  "callable", "r"),
            "copy":   ("dict[any, any]",        "callable", "r"),
            "get":    ("any",                   "callable", "r"),
            "items":  ("list[tuple[any, any]]", "callable", "r"),
            "keys":   ("list[any]",             "callable", "r"),
            "pop":    ("any",                   "callable", "r"),
            "update": ("none",                  "callable", "r"),
            "values": ("list[any]",             "callable", "r"),
        })
        
        
        ### COMPLEX TYPES ###
        
        cls.t_Player = cls("player", {
            "uid":            ("int",            "object", "r"),
            "name":           ("str",            "object", "r"),
            "health":         ("int",            "object", ("rw", "int")),
            "max_health":     ("int",            "object", ("rw", "int")),
            "location":       ("location",       "object", ("rw", "location")),
            "last_location":  ("location",       "object", ("rw", "location")),
            "position":       ("position",       "object", ("rw", "position")),
            "inventory":      ("inventory",      "object", ("rw", "inventory")),
            "currency":       ("currency",       "object", ("rw", "currency")),
            # "status_effects": ("status_effects", "object", "r"),
            "in_combat":      ("bool",           "object", "r"),
            "tag":            ("any",            "macro",  "r"),
        })
        
        cls.t_Inventory = cls("inventory", {
            "contents":              ("list[game_object]",      "object",   "r"),
            "equips":                ("dict[str, game_object]", "object",   "r"),
            "equip":                 ("none",                   "callable", "r"),
            "unequip":               ("none",                   "callable", "r"),
            "remove":                ("none",                   "callable", "r"),
            "add":                   ("none",                   "callable", "r"),
            "get_of_type":           ("list[game_object]",      "callable", "r"),
            "contains":              ("bool",                   "callable", "r"),
            "get_of_abstract_type":  ("list[game_object]",      "callable", "r"),
            "is_equipped":           ("bool",                   "callable", "r"),
            "get_equipped_of_type":  ("list[game_object]",      "callable", "r"),
            "unequip_type":          ("none",                   "callable", "r"),
            "get_full_stat_display": ("str",                    "callable", "r"),
            "get_stat_display":      ("str",                    "callable", "r"),
        })

        cls.t_Location = cls("location", {
            "dungeon":   ("dungeon", "object",   "r"),
            "room_path": ("str",     "object",   "r"),
            "room":      ("room",    "object",   "r"),
            "as_string": ("str",     "callable", "r"),
        })

        cls.t_Position = cls("position", {
            "x":       ("float",       "object",   ("rw", "float")),
            "y":       ("float",       "object",   ("rw", "float")),
            "as_list": ("list[float]", "callable", "r"),
        })

        cls.t_Currency = cls("currency", {
            "gold":        ("int",       "object",   ("rw", "int")),
            "silver":      ("int",       "object",   ("rw", "int")),
            "copper":      ("int",       "object",   ("rw", "int")),
            "as_list":     ("list[int]", "callable", "r"),
            "consolidate": ("none",      "callable", "r"),
            "convert":     ("none",      "macro",    "r"),
        })

        # t_StatusEffect = cls("status_effect", {
        # })

        cls.t_Dungeon = cls("dungeon", {
            "name":              ("str",           "object",   "r"),
            "version":           ("str|int|float", "object",   "r"),
            "rooms":             ("list[room]",    "object",   "r"),
            "player_ids":        ("list[int]",     "object",   "r"),
            "recovery_location": ("location",      "object",   "r"),
            # "map":               ("map",           "object",   "r"),
        })

        cls.t_Room = cls("room", {
            "name":       ("str",       "object", "r"),
            "location":   ("location",  "object", "r"),
            # "map":        ("map",       "object", "r"),
            "player_ids": ("list[int]", "object", "r"),
        })
        
        # cls.t_Combat = cls("combat", {
        # })
        
        # cls.t_Map = cls("map", {
        # })






