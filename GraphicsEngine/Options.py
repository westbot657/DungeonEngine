# pylint: disable=W,R,C


import json

# discord presence application id
client_id = "1149136139341541446"


DO_RICH_PRESENCE = False


PATH = "./ui_resources"
FONT = f"{PATH}/PTMono-Regular.ttf" # PTMono-Regular has correct lineup for │ and ┼!

with open("./editor_settings.json", "r+", encoding="utf-8") as f:
    SETTINGS = json.load(f)

from RenderPrimitives import Color

TEXT_SIZE = SETTINGS["text_size"]
TEXT_COLOR = Color(*SETTINGS["text_color"])
TEXT_BG_COLOR = Color(*SETTINGS["text_bg_color"])
TEXT_HIGHLIGHT = Color(*SETTINGS["text_highlight"])
TAB_SIZE = 4
CURSOR_BLINK_TIME = 50
CURSOR_COLOR = Color(190, 190, 190)
SCROLL_MULTIPLIER = 15

