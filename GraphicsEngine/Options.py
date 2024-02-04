# pylint: disable=W,R,C


import json

# discord presence application id
client_id = "1149136139341541446"


DO_RICH_PRESENCE = False


PATH = "./ui_resources"
FONT = f"{PATH}/PTMono-Regular.ttf" # PTMono-Regular has correct lineup for │ and ┼!

with open("./editor_settings.json", "r+", encoding="utf-8") as f:
    SETTINGS = json.load(f)

try:
    from .RenderPrimitives import Color
except ImportError:
    from RenderPrimitives import Color
    

TEXT_SIZE = SETTINGS["text_size"]
TEXT_COLOR = tuple(SETTINGS["text_color"])
TEXT_BG_COLOR = tuple(SETTINGS["text_bg_color"])
TEXT_HIGHLIGHT = tuple(SETTINGS["text_highlight"])
TAB_SIZE = 4
CURSOR_BLINK_TIME = 50
CURSOR_COLOR = (190, 190, 190)
SCROLL_MULTIPLIER = 15

