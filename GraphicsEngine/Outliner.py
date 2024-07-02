# pylint: disable=[W,R,C, no-member, import-error]

from UIElement import UIElement

from Easing import easeInOutCirc

import math
import pygame
import time

class Outliner(UIElement):
    def __init__(self, x, y, width, height, color, start_angle=90, direction=1, thickness=1, animation_time=1, animation_delay=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.start_angle = start_angle
        self.direction = direction
        self.thickness = thickness
        self.animation_time = animation_time
        self.start_time = 0
        self.animation_delay = animation_delay
        
        self.last_angle = 0
        self.surface = pygame.Surface((self.width+self.thickness, self.height+self.thickness), pygame.SRCALPHA, 32)
        self.bottom_right = math.degrees(math.atan2(self.height/2, self.width/2)) % 360
        self.top_right = math.degrees(math.atan2(-self.height/2, self.width/2)) % 360
        self.bottom_left = math.degrees(math.atan2(self.height/2, -self.width/2)) % 360
        self.top_left = math.degrees(math.atan2(-self.height/2, -self.width/2)) % 360

        # print(self.bottom_right, self.top_right, self.bottom_left, self.top_left)

        self.start_point = self.get_perimeter_point(self.start_angle)
        self.last_point = self.start_point
        
        self.subsection_size = 0.5
        
        self.br_corner = (
            self.width,
            self.height
        )
        self.bl_corner = (
            0,
            self.height
        )
        self.tr_corner = (
            self.width,
            0
        )
        self.tl_corner = (
            0,
            0
        )

    def clear(self):
        self.start_time = 0
        self.surface = pygame.Surface((self.width+self.thickness, self.height+self.thickness), pygame.SRCALPHA, 32)

    def get_perimeter_point(self, angle):
        theta = math.radians(angle)

        aa = self.width
        bb = self.height

        rectAtan = math.atan2(bb,aa)
        tanTheta = math.tan(theta)

        xFactor = 1
        yFactor = 1
        
        # determine regions
        if theta > (2*math.pi)-rectAtan or theta <= rectAtan:
            region = 1
        elif theta > rectAtan and theta <= math.pi-rectAtan:
            region = 2

        elif theta > math.pi - rectAtan and theta <= math.pi + rectAtan:
            region = 3
            xFactor = -1
            yFactor = -1
        elif theta > math.pi + rectAtan and theta < (2*math.pi) - rectAtan:
            region = 4
            xFactor = -1
            yFactor = -1
        else:
            # print(f"region assign failed : {theta}")
            return None
        
        # print(region, xFactor, yFactor)
        edgePoint = [0,0]
        ## calculate points
        if (region == 1) or (region == 3):
            edgePoint[0] += xFactor * (aa / 2.)
            edgePoint[1] += yFactor * (aa / 2.) * tanTheta
        else:
            edgePoint[0] += xFactor * (bb / (2. * tanTheta))
            edgePoint[1] += yFactor * (bb /  2.)

        return (edgePoint[0] + (self.width/2), edgePoint[1] + (self.height/2))

    def resize(self, width, height):
        if self.width != width or self.height != height:
            self.width = width
            self.height = height
            self.surface = pygame.Surface((self.width+self.thickness, self.height+self.thickness), pygame.SRCALPHA, 32)
            self.bottom_right = math.degrees(math.atan2(self.height/2, self.width/2)) % 360
            self.top_right = math.degrees(math.atan2(-self.height/2, self.width/2)) % 360
            self.bottom_left = math.degrees(math.atan2(self.height/2, -self.width/2)) % 360
            self.top_left = math.degrees(math.atan2(-self.height/2, -self.width/2)) % 360

            # print(self.bottom_right, self.top_right, self.bottom_left, self.top_left)

            self.start_point = self.get_perimeter_point(self.start_angle)
            self.last_point = self.start_point
            
            self.br_corner = (
                self.width,
                self.height
            )
            self.bl_corner = (
                0,
                self.height
            )
            self.tr_corner = (
                self.width,
                0
            )
            self.tl_corner = (
                0,
                0
            )
            # self.subsection_size = (self.width*2 + self.height*2) / 30
            
            self.start_animation(0)

    def start_animation(self, delay=0):
        self.last_angle = self.start_angle
        self.last_point = self.start_point
        self.start_time = time.time() + delay + self.animation_delay
        self.surface = pygame.Surface((self.width+self.thickness, self.height+self.thickness), pygame.SRCALPHA, 32)
        
    
    def draw_segment(self, angle):
        new_point = self.get_perimeter_point(angle)
        if new_point:
            # print(self.last_point, new_point)
            
            if angle >= self.bottom_right and (self.bottom_right > self.last_angle or self.last_angle > self.top_right):
                pygame.draw.line(self.surface, self.color, self.last_point, self.br_corner, self.thickness)
                self.last_angle = self.bottom_right
                self.last_point = self.br_corner
            elif angle >= self.bottom_left >= self.last_angle:
                pygame.draw.line(self.surface, self.color, self.last_point, self.bl_corner, self.thickness)
                self.last_angle = self.bottom_left
                self.last_point = self.bl_corner
            elif self.top_right >= self.last_angle and (angle >= self.top_right or angle <= self.bottom_right):
                pygame.draw.line(self.surface, self.color, self.last_point, self.tr_corner, self.thickness)
                self.last_angle = self.top_right
                self.last_point = self.tr_corner
            elif angle >= self.top_left >= self.last_angle:
                pygame.draw.line(self.surface, self.color, self.last_point, self.tl_corner, self.thickness)
                self.last_angle = self.top_left
                self.last_point = self.tl_corner
            
            
            pygame.draw.line(self.surface, self.color, self.last_point, new_point, self.thickness)
            self.last_point = new_point
            self.last_angle = angle
    
    def _event(self, editor, X, Y):
        if self.start_time > 0:
            if time.time() < self.start_time: return
            if self.direction == 1: # clockwise
                dt = (time.time() - self.start_time) / self.animation_time
                if dt >= 1:
                    dt = 1
                    self.start_time = 0
                angle = (self.start_angle + (easeInOutCirc(dt) * 360)) % 360
                
                while (angle - self.last_angle) % 360 > self.subsection_size or (angle - (self.last_angle + 360)) % 360 > self.subsection_size:
                    la = (self.last_angle + self.subsection_size) % 360
                    self.draw_segment(la)
                    self.last_angle = la
                self.draw_segment(angle)


    def _update(self, editor, X, Y):
        editor.screen.blit(self.surface, (X+self.x, Y+self.y))