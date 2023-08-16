# pylint: disable=[W,R,C,import-error]

try:
    from .Vector2 import Vector2
except ImportError:
    from Vector2 import Vector2

class Mouse:

    def __init__(self):
        self.left_button = False
        self.middle_button = False
        self.right_button = False

        self.p_left_button = False
        self.p_middle_button = False
        self.p_right_button = False

        self.scroll = 0

        self.position = Vector2(0, 0)

    def onLeftClick(self):
        return (not self.left_button) and (self.p_left_button)

    def onMiddleClick(self):
        return (not self.middle_button) and (self.p_middle_button)

    def onRightClick(self):
        return (not self.right_button) and (self.p_right_button)

    def offLeftClick(self):
        return (self.left_button) and (not self.p_left_button)

    def offMiddleClick(self):
        return (self.middle_button) and (not self.p_middle_button)

    def offRightClick(self):
        return (self.right_button) and (not self.p_right_button)

