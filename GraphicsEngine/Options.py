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

POPOUTS = {
    "text-editor": {
        "size": [300, 200],
        "components": {
            "text_edit": {
                "type": "NumberedTextArea",
                "args": [
                    5, 21, 240, 208
                ],
                "kwargs": {}
            }
        },
        "links": [
            {
                "parent": "editor",
                "child": "editor",
                "parent_attr": "width",
                "child_attr": "width",
                "link_handler": "max(a, 250)"
            },
            {
                "parent": "editor",
                "child": "editor",
                "parent_attr": "height",
                "child_attr": "height",
                "link_handler": "max(a, 250)"
            },
            {
                "parent": "editor",
                "child": "text_edit",
                "parent_attr": "width",
                "child_attr": "width",
                "link_handler": "a"
            },
            {
                "parent": "editor",
                "child": "text_edit",
                "parent_attr": "height",
                "child_attr": "height",
                "link_handler": "a"
            }
        ],
        "editor_layers": {
            "0": [
                "text_edit"
            ]
        },
        "window_limits": [300, 200, 1920, 1280]
    }
}


