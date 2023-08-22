# pylint: disable=[W,R,C,import-error]

try:
    from .Vector2 import Vector2
except ImportError:
    from Vector2 import Vector2

import pygame
class Mouse:

    def __init__(self):
        self.left_button = False
        self.middle_button = False
        self.right_button = False

        self.p_left_button = False
        self.p_middle_button = False
        self.p_right_button = False

        self.xscroll = 0
        self.yscroll = 0

        self.position = Vector2(0, 0)

        self.holding_obj = False
        self.held_obj = None
        self.hold_offset = [0, 0]

        self.last_selected = None
        self.clicked = None

        self.hovering = None

    def update(self, engine):
        self.clicked = None
        self.hovering = None

        if self.holding_obj:
            if (not self.left_button) and (self.p_left_button):
                self.held_obj.held = False
                self.held_obj = None
                self.holding_obj = False
                self.hold_offset = [0, 0]
            else:
                self.held_obj.parent.bringToTop(self.held_obj)
                self.held_obj.held = True
                par = self.held_obj.getTopParent()
                absolute_pos = par.getRealPosition()
                relative_pos = par.getPosition()
                difference = absolute_pos - relative_pos
                mouse_relative = self.position - difference
                self.held_obj.setPosition(mouse_relative - self.hold_offset)

    def setClicked(self, obj):
        if self.last_selected:
            self.last_selected.selected = False
            self.last_selected = None
        self.clicked = obj

    def post_update(self, engine):

        reset_mouse = True
        if self.hovering:
            self.hovering.hovered = True
            reset_mouse = False

        if self.onLeftClick():
            if self.clicked:
                self.last_selected = self.clicked
                self.last_selected.selected = True
            else:
                if self.last_selected:
                    self.last_selected.selected = False
                self.last_selected = None


        if reset_mouse and pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW: # pylint: disable=[no-member]
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) # pylint: disable=[no-member]
            

    def onLeftClick(self):
        return (self.left_button) and (not self.p_left_button)

    def onMiddleClick(self):
        return (self.middle_button) and (not self.p_middle_button)

    def onRightClick(self):
        return (self.right_button) and (not self.p_right_button)

    def offLeftClick(self):
        return (not self.left_button) and (self.p_left_button)

    def offMiddleClick(self):
        return (not self.middle_button) and (self.p_middle_button)

    def offRightClick(self):
        return (not self.right_button) and (self.p_right_button)

    def getPosition(self) -> Vector2:
        return self.position

    def getScroll(self) -> Vector2:
        return Vector2(self.xscroll, self.yscroll)

    def _setButtons(self, l, m, r):
        self.p_left_button = self.left_button
        self.p_middle_button = self.middle_button
        self.p_right_button = self.right_button
        self.left_button = l
        self.middle_button = m
        self.right_button = r
