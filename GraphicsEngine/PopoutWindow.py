# pylint: disable=[W,R,C]

import pygame
import sys # for grabbing cmd-line args
import json # for parsing cmd-line args
try:
    from .ui_library import * # for access to all the stuff I've already defined
except ImportError:
    from ui_library import *





if __name__ == "__main__":
    args = sys.argv[1:]
    
    if len(args) != 1:
        exit()
    PopoutWindow(**json.loads(args[0]))

