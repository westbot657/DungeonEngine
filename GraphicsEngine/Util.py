# pylint: disable=W,R,C,no-member

import re
import math
import pygame
import numpy
import cv2

def expand_text_lists(ls):
    """
    turns a list of lists of strings into a list of lists of chars
    ie: [["hello", "world"], ["!!!"]]
    turns into
    [["h", "e", "l", "l", "o", "w", "o", "r", "l", "d"], ["!", "!", "!"]]
    """
    out = []
    for l in ls:
        _out = []
        for t in l:
            _out += [a for a in re.split(r"", t) if a]
        out.append(_out)
    return out

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    dx = px - ox
    dy = py - oy
    sa = math.sin(math.radians(angle))
    ca = math.cos(math.radians(angle))

    qx = ox + ca * (dx) - sa * (dy)
    qy = oy + sa * (dx) + ca * (dy)
    return qx, qy

def rotate3D(origin, point, angle):
    """
    rotates a point around an origin in 3D space
    """
    if not angle:
        return point

    if isinstance(angle, list) and isinstance(angle[0], (tuple, list)):
        angles = angle.copy()
    else:
        angles = [angle]

    pt = point
    while angles:
        angle = angles.pop(0)
        xrot = [pt[0], *rotate(origin[1:3], pt[1:3], angle[0])]
        a, b = rotate((origin[0], origin[2]), (xrot[0], xrot[2]), angle[1])
        xyrot = [a, xrot[1], b]
        xyzrot = [*rotate(origin[0:2], xyrot[0:2], angle[2]), xyrot[2]]
        pt = xyzrot
    return pt

def rotate3DV(origin, vertices, angle):
    """rotates a collection of points around an origin in 3D space"""
    return [rotate3D(origin, point, angle) for point in vertices]

def quad_to_tris(quad):
    """converts a quad into 2 tris"""
    if len(quad) == 4:
        return [quad[0:3], [*quad[2:4], quad[0]]]
    if len(quad) == 3:
        return [quad]
    raise ValueError("Invalid quad/tri")

def invert_tris(tris):
    """inverts a tri so it faces the opposite way"""
    return [(t[2], t[1], t[0]) for t in tris]

def angle_between(p1, p2):
    """returns the angle between 2 points"""
    return math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))

def warp(surf: pygame.Surface,
         warp_pts,
         smooth=True,
         out: pygame.Surface = None) -> tuple[pygame.Surface, pygame.Rect]:
    """Stretches a pygame surface to fill a quad using cv2's perspective warp.

        Args:
            surf: The surface to transform.
            warp_pts: A list of four xy coordinates representing the polygon to fill.
                Points should be specified in clockwise order starting from the top left.
            smooth: Whether to use linear interpolation for the image transformation.
                If false, nearest neighbor will be used.
            out: An optional surface to use for the final output. If None or not
                the correct size, a new surface will be made instead.

        Returns:
            [0]: A Surface containing the warped image.
            [1]: A Rect describing where to blit the output surface to make its coordinates
                match the input coordinates.
    """
    if len(warp_pts) != 4:
        raise ValueError("warp_pts must contain four points")

    w, h = surf.get_size()
    is_alpha = surf.get_flags() & pygame.SRCALPHA

    # throughout this method we need to swap x and y coordinates
    # when we pass stuff between pygame and cv2. I'm not sure why .-.
    src_corners = numpy.float32([(0, 0), (0, w), (h, w), (h, 0)])
    quad = [tuple(reversed(p)) for p in warp_pts]

    # find the bounding box of warp points
    # (this gives the size and position of the final output surface).
    min_x = min(p[0] for p in quad)
    max_x = max(p[0] for p in quad)
    min_y = min(p[1] for p in quad)
    max_y = max(p[1] for p in quad)
    warp_bounding_box = pygame.Rect(float(min_x), float(min_y),
                                    float(max_x - min_x + 10),
                                    float(max_y - min_y + 10))

    shifted_quad = [(p[0] - min_x + 5, p[1] - min_y + 5) for p in quad]
    dst_corners = numpy.float32(shifted_quad)

    mat = cv2.getPerspectiveTransform(src_corners, dst_corners)

    orig_rgb = pygame.surfarray.pixels3d(surf)

    flags = (cv2.INTER_LINEAR if smooth else cv2.INTER_NEAREST)

    out_rgb = cv2.warpPerspective(orig_rgb, mat, warp_bounding_box.size, flags=flags)

    if out is None or out.get_size() != out_rgb.shape[0:2]:
        out = pygame.Surface(out_rgb.shape[0:2], pygame.SRCALPHA)

    pygame.surfarray.blit_array(out, out_rgb)

    if is_alpha:
        orig_alpha = pygame.surfarray.pixels_alpha(surf)
        out_alpha = cv2.warpPerspective(orig_alpha, mat, warp_bounding_box.size, flags=flags)
        alpha_px = pygame.surfarray.pixels_alpha(out)
        alpha_px[:] = out_alpha
    else:
        out.set_colorkey(surf.get_colorkey())

    pixel_rect = out.get_bounding_rect()
    # print(pixel_rect)
    # # trimmed_surface = pygame.Surface(pixel_rect.size, pygame.SRCALPHA, 32)
    # # trimmed_surface.blit(out, (0, 0), pixel_rect)
    # out = pygame.transform.chop(out, pixel_rect)

    # swap x and y once again...
    return out, pixel_rect


class Selection:
    
    __slots__ = [
        "text", "start", "end"
    ]
    
    def __init__(self, text:str, start:int, end:int):
        self.text = text
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Selection [{self.start}:{self.end}]: '{self.text}'"

class Cursor:
    
    __slots__ = [
        "line",
        "col"
    ]
    
    def __init__(self, line, col):
        self.line = line
        self.col = col
    def copy(self):
        return Cursor(self.line, self.col)

    def __bool__(self):
        return True

    def __lt__(self, other):
        if isinstance(other, Cursor):
            if self.line == other.line: return self.col < other.col
            return self.line < other.line

    def __le__(self, other):
        if isinstance(other, Cursor):
            if self.line == other.line: return self.col <= other.col
            return self.line < other.line

    def __gt__(self, other):
        if isinstance(other, Cursor):
            if self.line == other.line: return self.col > other.col
            return self.line > other.line
    
    def __ge__(self, other):
        if isinstance(other, Cursor):
            if self.line == other.line: return self.col >= other.col
            return self.line > other.line

    def __eq__(self, other):
        if isinstance(other, Cursor):
            if self is other: return True
            return self.line == other.line and self.col == other.col

    def __repr__(self):
        return f"Cursor({self.line}, {self.col})"

