# pylint: disable=[W,R,C]

import pygame
import sys # for grabbing cmd-line args
import json # for parsing cmd-line args
try:
    from .ui_library import *
except ImportError:
    from ui_library import *


if __name__ == "__main__":
    # breakpoint()
    PopoutWindow()

