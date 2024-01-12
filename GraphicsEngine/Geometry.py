# pylint: disable=W,R,C,no-member

from UIElement import UIElement
from RenderPrimitives import Color, Image, Animation
from Options import TEXT_COLOR
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon as Poly
from Util import rotate, rotate3D, rotate3DV, quad_to_tris, \
    invert_tris, angle_between, warp
from meshpy import geometry

import pygame
import math

class Box(UIElement):
    
    __slots__ = [
        "x", "y", "width", "height",
        "color", "children", "hovered"
    ]

    def __init__(self, x, y, width, height, color:Color|Image|tuple|int=TEXT_COLOR):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = Color.color(color)
        self.children = []
        self.hovered = False

    def _update(self, editor, X, Y):
        if isinstance(self.color, (Image, Animation)):
            self.color._update(editor, X, Y)
            self.color.x = 0
            self.color.y = 0
            self.color.width = self.width
            self.color.height = self.height
        elif self.color:
            editor.screen.fill(tuple(self.color), (X + self.x, Y + self.y, self.width, self.height))
        for child in self.children:
            child._update(editor, X + self.x, Y + self.y)
    
    def _event(self, editor, X, Y):
        _x, _y = editor.mouse_pos
        #if (max(editor.X, X + self.x) <= _x <= min(X + self.x + self.width, editor.Width) and max(editor.Y, Y + self.y) <= _y <= min(Y + self.y + self.height, editor.Height)):
        for child in self.children[::-1]:
            child._event(editor, X + self.x, Y + self.y)

        
        if editor.collides((_x, _y), (X+self.x, Y+self.y, self.width, self.height)):
            if editor._hovering is None:
                self.hovered = editor._hovered = True
                editor._hovering = self
        else:
            self.hovered = False

class Polygon(UIElement):
    closest_point_disp = Box(-1, -1, 3, 3, (200, 20, 20))
    second_closest_disp = Box(-1, -1, 3, 3, (200, 200, 20))
    default_disp = Box(-1, -1, 3, 3, (20, 200, 20))
    class PointMover(UIElement):
        __slots__ = ["parent_poly", "mesh_index", "held"]
        def __init__(self, parent_poly, mesh_index):
            self.parent_poly = parent_poly
            self.mesh_index = mesh_index
            self.held = True
            self.parent_poly.children.append(self)
        def _update(self, editor, X, Y): pass
        def _event(self, editor, X, Y):
            self.parent_poly.mesh[self.mesh_index] = Point(*editor.mouse_pos)
            self.parent_poly.refresh()
            if editor.left_mouse_up():
                self.held = False
                if editor._focused_object is self:
                    self.parent_poly.children.remove(self)
                    editor._focused_object = None

    @classmethod
    def load(cls, data:dict):
        return cls([Point(a, b) for a, b in data["mesh"]], data["color"], **data["options"])

    def save(self):
        return {
            "mesh": [[a.x, a.y] for a in self.mesh],
            "color": list(self.color),
            "options": {
                "draggable_points": self.draggable_points,
                "draggable": self.draggable,
            }
        }

    def __init__(self, mesh:list[Point], color:Color|tuple|int=TEXT_COLOR, **options):
        """
        Args:
            mesh (list[Point]): list of polygon points going clockwise
            color (Color | tuple | int, optional): color to fill the polygon with. Defaults to TEXT_COLOR.

        options:
            draggable_points (bool): whether polygon's points can be moved. Defaults to False.
            draggable (bool): whether the entire polygon can be moved. Defaults to False.
        """
        if len(mesh) < 3:
            raise ValueError("mesh must contain at least 3 points")
        self.mesh = mesh
        self.relative_mesh = []
        self.color = Color.color(color)
        self.draggable_points: bool = options.get("draggable_points", False)
        self.draggable: bool = options.get("draggable", False)
        self.hovered = False
        self.held = False
        self.point_displays = []
        self.refresh()
        self.children = []

    def refresh(self):
        self.poly = Poly(self.mesh)
        self.minX = min(p.x for p in self.mesh)
        self.maxX = max(p.x for p in self.mesh)
        self.minY = min(p.y for p in self.mesh)
        self.maxY = max(p.y for p in self.mesh)
        self.width = self.maxX - self.minX
        self.height = self.maxY - self.minY
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        pygame.draw.polygon(self.surface, tuple(self.color), [(p.x-self.minX, p.y-self.minY) for p in self.mesh])
        # self.point_displays.clear()

    def collides(self, x, y):
        return self.poly.contains(Point(x, y))

    def _update(self, editor, X, Y):
        editor.screen.blit(self.surface, (self.minX, self.minY))
        for disp, x, y in self.point_displays:
            disp._update(editor, X+x, Y+y)
        for child in self.children:
            child._update(editor, X, Y)
    
    def _event(self, editor, X, Y):
        if self.children:
            for c in self.children[::-1]:
                c._event(editor, X, Y)
        if self.collides(*editor.mouse_pos):
            if editor._hovering is None:
                self.hovered = editor._hovered = True
                editor._hovering = self
        else:
            self.hovered = False

        # check point collisions if points are draggable
        if editor.left_mouse_down() and self.draggable_points:
            i = 0
            for point in self.mesh:
                if math.sqrt(((point.x - editor.mouse_pos[0]) ** 2) + ((point.y - editor.mouse_pos[1]) ** 2)) <= 3:
                    if editor._focused_object is None:
                        mover = Polygon.PointMover(self, i)
                        editor._focused_object = mover
                    break
                i += 1

        # check polygon collision for dragging
        if editor.left_mouse_down() and self.draggable:
            if self.hovered:
                if editor._focused_object is None:
                    editor._focused_object = self
                    editor.cancel_mouse_event()
                    self.relative_mesh.clear()
                    self.relative_mesh += [[p.x-editor.mouse_pos[0], p.y-editor.mouse_pos[1]] for p in self.mesh]
                    # print(f"RELATIVE MESH: {self.relative_mesh}")
                    self.held = True
                    # self.pickup_point = editor.mouse_pos
                    # self.pickup_offset = [editor.mouse_pos[0] - self.minX, editor.mouse_pos[1] - self.minY]
                    # self.hx = _x - (X + self.x)
                    # self.hy = _y - (Y + self.y)
                    editor.previous_mouse = editor.mouse # set this so that only 1 object is picked up
                    
            else:
                self.held = False
                if editor._focused_object is self:
                    editor._focused_object = None

        elif editor.left_mouse_up():
            self.held = False
            if editor._focused_object is self:
                self.relative_mesh.clear()
                editor._focused_object = None

        if self.held:
            self.mesh.clear()
            self.mesh += [
                Point(x+editor.mouse_pos[0], y+editor.mouse_pos[1]) for x, y in self.relative_mesh
            ]
            self.refresh()

        if self.hovered and self.draggable:

            if pygame.K_TAB in editor.keys:
                points = []
                i = 0
                for point in self.mesh:
                    pd = math.sqrt(((point.x - editor.mouse_pos[0]) ** 2) + ((point.y - editor.mouse_pos[1]) ** 2))
                    points.append((pd, i, point.x, point.y))
                    i += 1
                points.sort( # sort points by distance
                    key=lambda a: a[0]
                )
                dist, index, _, __ = points[0]
                idx_down = index - 1 if index > 0 else len(points)-1
                idx_up = index + 1 if index < len(points) - 1 else 0
                dist_down = [p[0] for p in points if p[1] == idx_down]
                dist_up = [p[0] for p in points if p[1] == idx_up]
                i2 = idx_down if dist_down <= dist_up else idx_up
                self.point_displays.clear()
                for p in points:
                    if p[1] == index:
                        self.point_displays.append((self.closest_point_disp, *p[2:4]))
                    elif p[1] == i2:
                        self.point_displays.append((self.second_closest_disp, *p[2:4]))
                    else:
                        self.point_displays.append((self.default_disp, *p[2:4]))
            else:
                self.point_displays.clear()

            for key in editor.typing:
                print(f"{key!r}")
                if key == "\x10": # CTRL+P
                    points = []
                    i = 0
                    for point in self.mesh:
                        pd = math.sqrt(((point.x - editor.mouse_pos[0]) ** 2) + ((point.y - editor.mouse_pos[1]) ** 2))
                        points.append((pd, i))
                        i += 1
                    
                    points.sort( # sort points by distance
                        key=lambda a: a[0]
                    )

                    dist, index = points[0]

                    if pygame.K_LSHIFT in editor.keys:
                        if len(self.mesh) > 3:
                            self.mesh.pop(index)
                            self.refresh()
                        continue

                    idx_down = index - 1 if index > 0 else len(points)-1
                    idx_up = index + 1 if index < len(points) - 1 else 0

                    dist_down = [p[0] for p in points if p[1] == idx_down]
                    dist_up = [p[0] for p in points if p[1] == idx_up]

                    if dist_down <= dist_up:
                        self.mesh.insert(index, Point(*editor.mouse_pos))
                    else:
                        self.mesh.insert(idx_up, Point(*editor.mouse_pos))
                    self.refresh()
                # elif key == "\t":
                #     if self.point_displays:
                #         self.point_displays.clear()
                #         continue
                elif key == "$→":
                    if pygame.K_LALT in editor.keys: # rotate
                        degrees = 45 if pygame.K_LSHIFT in editor.keys else 1 if pygame.K_LCTRL in editor.keys else 10
                        new = [Point(rotate(editor.mouse_pos, (p.x, p.y), math.radians(degrees))) for p in self.mesh]
                        self.mesh.clear()
                        self.mesh += new
                        self.refresh()
                    else: # move
                        distance = 50 if pygame.K_LSHIFT in editor.keys else 1 if pygame.K_LCTRL in editor.keys else 10
                        new = [Point(p.x+distance, p.y) for p in self.mesh]
                        self.mesh.clear()
                        self.mesh += new
                        self.refresh()

                elif key == "$←":
                    if pygame.K_LALT in editor.keys: # rotate
                        degrees = 45 if pygame.K_LSHIFT in editor.keys else 1 if pygame.K_LCTRL in editor.keys else 10
                        new = [Point(rotate(editor.mouse_pos, (p.x, p.y), math.radians(-degrees))) for p in self.mesh]
                        self.mesh.clear()
                        self.mesh += new
                        self.refresh()
                    else: # move
                        distance = 50 if pygame.K_LSHIFT in editor.keys else 1 if pygame.K_LCTRL in editor.keys else 10
                        new = [Point(p.x-distance, p.y) for p in self.mesh]
                        self.mesh.clear()
                        self.mesh += new
                        self.refresh()
                
                elif key == "$↓":
                    if pygame.K_LALT in editor.keys: # flip along vertical axis
                        new = [Point(editor.mouse_pos[0]-(p.x - editor.mouse_pos[0]), p.y) for p in self.mesh]
                        self.mesh.clear()
                        self.mesh += new
                        self.refresh()
                    else: # move
                        distance = 50 if pygame.K_LSHIFT in editor.keys else 1 if pygame.K_LCTRL in editor.keys else 10
                        new = [Point(p.x, p.y+distance) for p in self.mesh]
                        self.mesh.clear()
                        self.mesh += new
                        self.refresh()
                elif key == "$↑":
                    if pygame.K_LALT in editor.keys: # flip along horizontal axis
                        new = [Point(p.x, editor.mouse_pos[1]-(p.y - editor.mouse_pos[1])) for p in self.mesh]
                        self.mesh.clear()
                        self.mesh += new
                        self.refresh()
                    else: # move
                        distance = 50 if pygame.K_LSHIFT in editor.keys else 1 if pygame.K_LCTRL in editor.keys else 10
                        new = [Point(p.x, p.y-distance) for p in self.mesh]
                        self.mesh.clear()
                        self.mesh += new
                        self.refresh()

class Poly3D(UIElement):
    FOV = 90 # degrees
    width = 1280
    height = 720
    # dist = (width/2) / math.degrees(math.tan(math.radians(FOV/2)))
    # dist = math.sin(math.radians(90-(FOV/2)))*(width/2)
    dist = (math.sin(math.radians(90-(FOV/2))) * (width/2)) / (math.sin(math.radians(FOV/2)))
    cam_position = [0, 0, -dist]
    light_angle = [2, 1, 3] # x, y, z vector
    brightness = [200, 200, 200] # for images

    # print(f"{dist=}")

    @classmethod
    def cube(cls, position:list|tuple, size:int|float, color, rotations:list[tuple|list]=None, controllers:list=None, data:dict=None, texture_mapping:list=None):
        # rotations = rotations or []

        s = size/2
        vertices = [rotate3D((0, 0, 0), xyz, rotations) for xyz in [
            (-s, -s, -s), # 0
            (-s, -s, s), # 1
            (-s, s, -s),  # 2
            (-s, s, s),  # 3
            (s, -s, -s),  # 4
            (s, -s, s),  # 5
            (s, s, -s),   # 6
            (s, s, s)    # 7
        ]]
        tris = [
            (0, 2, 4), (4, 2, 6), # front
            (2, 3, 6), (6, 3, 7), # bottom
            (2, 0, 3), (3, 0, 1), # left
            (3, 1, 7), (7, 1, 5), # back
            (5, 4, 7), (7, 4, 6), # right
            (1, 0, 5), (5, 0, 4) # top
        ]
        vertices = [(v[0]+position[0], v[1]+position[1], v[2]+position[2]) for v in vertices.copy()]

        return cls(vertices, tris, color, controllers, data, texture_mapping)

    @classmethod
    def ensure_alpha(cls, img):
        s = pygame.Surface((img.get_width(), img.get_height()), pygame.SRCALPHA, 32)
        s.blit(img, (0, 0))
        return s

    @classmethod
    def cube_map(cls, image=None, top=None, north=None, east=None, south=None, west=None, bottom=None):
        return [
            (cls.ensure_alpha(top or image), (5, 1, 0, 4)),
            (cls.ensure_alpha(north or image), (1, 5, 7, 3)),
            (cls.ensure_alpha(east or image), (5, 4, 6, 7)),
            (cls.ensure_alpha(south or image), (4, 0, 2, 6)),
            (cls.ensure_alpha(west or image), (0, 1, 3, 2)),
            (cls.ensure_alpha(bottom or image), (3, 7, 6, 2))
        ]


    @classmethod
    def cylinder(cls, position, radius, length, color, subdivisions=8, rotations:list[tuple|list]=None, controllers:list=None, data:dict=None, texture_mapping:list=None):
        rotations = rotations or []
        if subdivisions < 3:
            raise ValueError("subdivisions must be greater than 3")
        h = length/2
        vertices = [(0, h, 0), (0, -h, 0), (radius, h, 0), (radius, -h, 0)]
        tris = []

        diff = -360/subdivisions

        for sub in range(subdivisions-1):
            vertices = rotate3DV((0, 0, 0), vertices, (0, diff, 0))
            vertices += [(radius, h, 0), (radius, -h, 0)]
            tris += [
                (0, len(vertices)-2, len(vertices)-4),
                (1, len(vertices)-3, len(vertices)-1),
                (len(vertices)-2, len(vertices)-1, len(vertices)-4),
                (len(vertices)-1, len(vertices)-3, len(vertices)-4)
            ]
        
        tris += [
            (0, 2, len(vertices)-2),
            (1, len(vertices)-1, 3),
            (len(vertices)-2, 2, len(vertices)-1),
            (2, 3, len(vertices)-1)
        ]
        vertices = [(v[0]+position[0], v[1]+position[1], v[2]+position[2]) for v in rotate3DV((0, 0, 0), vertices, [(0, diff, 0), *rotations])]


        return cls(vertices, tris, color, controllers, data, texture_mapping)

    @classmethod
    def sphere(cls, position, radius, color, subdivisions=10, rotations=None, controllers:list=None, data:dict=None, texture_mapping:list=None):
        vertices, _tris = geometry.make_ball(radius, subdivisions)[0:2]

        # print(f"VERTICES: {vertices}\n\nTRIS: {_tris}")

        vertices = [(v[0]+position[0], v[1]+position[1], v[2]+position[2]) for v in rotate3DV((0, 0, 0), vertices, rotations or [])]

        tris = []
        for tri in _tris:
            tris += quad_to_tris(tri[0])
        
        return cls(vertices, invert_tris(tris), color, controllers, data, texture_mapping)

    @classmethod
    def extrude_polygon(cls, position, polygon:Polygon, height:int, color, rotations=None, controllers:list=None, data:dict=None, texture_mapping:list=None):
        vertices = []
        tris = []
        
        points = [(p.x, p.y) for p in polygon.mesh.copy()]
        
        mx = sum(p[0] for p in points) / len(points)
        my = sum(p[1] for p in points) / len(points)
        
        # slice list to put furthest point from middle at beginning of list
        # furthest = (0, 0) # (distance, index)
        # i = 0
        # for p in points:
        #     d = math.sqrt(((p[0]-mx) ** 2) + ((p[1]-my) ** 2))
        #     if d > furthest[0]:
        #         furthest = (d, i)
        #     i += 1
        
        # pre = points[0:furthest[1]]
        # points = points[len(pre):] + pre
        h = height/2
        
        # iterate points for extrusion
        i = -1
        for p in points:
            prev = points[i]

            v1 = (p[0], -h, p[1])
            v2 = (p[0], h, p[1])
            v3 = (prev[0], -h, prev[1])
            v4 = (prev[0], h, prev[1])

            if v1 in vertices:
                v1i = vertices.index(v1)
            else:
                vertices.append(v1)
                v1i = len(vertices)-1

            if v2 in vertices:
                v2i = vertices.index(v2)
            else:
                vertices.append(v2)
                v2i = len(vertices)-1
            
            if v3 in vertices:
                v3i = vertices.index(v3)
            else:
                vertices.append(v3)
                v3i = len(vertices)-1
            
            if v4 in vertices:
                v4i = vertices.index(v4)
            else:
                vertices.append(v4)
                v4i = len(vertices)-1

            tris += [
                (v3i, v1i, v2i),
                (v4i, v3i, v2i)
            ]

            i += 1
        
        # generate polygon surface mesh
        
        op = 0
        mp = 1
        ep = len(points)-1
        fails = 0

        while len(points) >= 3:
            p1 = points[op]
            p2 = points[mp]
            p3 = points[ep]

            r1 = angle_between(p1, p2)
            r2 = angle_between(p1, p3)
        
            while r1 < 0: r1 += 360
            while r1 >= 360: r1 -= 360

            while r2 < 0: r2 += 360
            while r2 >= 360: r2 -= 360

            # dr = abs(r2-r1)

            pol = Poly((p1, p2, p3))
            contained = any([pol.contains_properly(Point(*p)) for p in points if p not in [p1, p2, p3]])

            c = (pol.intersection(polygon.poly).area / pol.area) if pol.area else False

            # print(dr, c, points)

            if (not contained) and (c == 1): #and (dr < 180) :
                v11 = (p1[0], -h, p1[1])
                v12 = (p1[0], h, p1[1])
                v21 = (p2[0], -h, p2[1])
                v22 = (p2[0], h, p2[1])
                v31 = (p3[0], -h, p3[1])
                v32 = (p3[0], h, p3[1])

                if v11 in vertices:
                    v11i = vertices.index(v11)
                else:
                    vertices.append(v11)
                    v11i = len(vertices)-1
                
                if v12 in vertices:
                    v12i = vertices.index(v12)
                else:
                    vertices.append(v12)
                    v12i = len(vertices)-1

                if v21 in vertices:
                    v21i = vertices.index(v21)
                else:
                    vertices.append(v21)
                    v21i = len(vertices)-1

                if v22 in vertices:
                    v22i = vertices.index(v22)
                else:
                    vertices.append(v22)
                    v22i = len(vertices)-1

                if v31 in vertices:
                    v31i = vertices.index(v31)
                else:
                    vertices.append(v31)
                    v31i = len(vertices)-1

                if v32 in vertices:
                    v32i = vertices.index(v32)
                else:
                    vertices.append(v32)
                    v32i = len(vertices)-1
                
                tris += [
                    (v31i, v21i, v11i),
                    (v12i, v22i, v32i)
                ]
                points.remove(p1)
                # fails = -op
                op = 0
                mp = 1
                ep = len(points)-1
            else:
                op += 1
                mp += 1
                ep += 1

                if op >= len(points): op = 0
                if mp >= len(points): mp = 0
                if ep >= len(points): ep = 0
                # fails += 1

                # if fails > len(points):
                #     break


        vertices = [(v[0]+position[0], v[1]+position[1], v[2]+position[2]) for v in vertices]
        vertices = rotate3DV(position, vertices, rotations or [])


        return cls(vertices, tris, color, controllers, data, texture_mapping)

    def __init__(self, vertices, tris, color, controllers:list=None, data:dict=None, texture_mapping:list=None):
        """
        texture mapping:
        [(pygame.Surface, (p1, p2, p3, p4)), ...]
        """
        self.vertices = vertices
        self.tris = tris
        self.color = color
        self.surfaces = []
        self.controllers = controllers or []
        self.data = data or {}
        self.texture_mapping = texture_mapping or []


    def mod_color(self, v1, v2, v3, color=None) -> tuple:
        color = color or self.color
        x0, y0, z0 = v1
        x1, y1, z1 = v2
        x2, y2, z2 = v3

        ux, uy, uz = u = [x1-x0, y1-y0, z1-z0]
        vx, vy, vz = v = [x2-x0, y2-y0, z2-z0]

        normal = [uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx]

        diff = max(abs(n) for n in normal)

        normal = [n/diff for n in normal]

        # print(normal)

        dot = ((normal[0]*self.light_angle[0]) + (normal[1]*self.light_angle[1]) + (normal[2]*self.light_angle[2]))
        mag1 = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
        mag2 = math.sqrt(self.light_angle[0]**2 + self.light_angle[1]**2 + self.light_angle[2]**2)

        d = mag1*mag2

        try:
            if d != 0:

                diff = dot/d

                angle = math.degrees(math.acos(diff))
            else:
                print("LIGTHING ERROR: d == 0!!")
        except Exception as e:
            print(f"{d=}, {dot=}, {mag1=}, {mag2=}, {normal=}, {dot/d=}, {diff=}")
            raise

        lighting_diff = (angle/180)

        # print(pre)
        # lighting_diff = abs(pre/3) #if pre != 0 else 0
        # lighting_diff = max(abs(normal[0]-self.light_angle[0]), abs(normal[1]-self.light_angle[0]), abs(normal[1]-self.light_angle[0]))

        # print(lighting_diff)

        c = (int(color[0] * lighting_diff), int(color[1] * lighting_diff), int(color[2] * lighting_diff))
        c = [min(max(0, _c), 255) for _c in c] + ([color[3]] if len(color) == 4 else [])
        # print(c)
        return c

    def project_point(self, point) -> tuple:
        px, py, pz = point
        cx, cy, cz = self.cam_position
        x = ((px-cx) * (((pz+self.dist)-cz)/(pz+self.dist))) + cx
        y = ((py-cy) * (((pz+self.dist)-cz)/(pz+self.dist))) + cy

        return int(x), int(y)

    @classmethod
    def check_rotation(cls, p1, p2, p3, mp="center"):
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        if mp == "center":
            mx = (x1 + x2 + x3) / 3
            my = (y1 + y2 + y3) / 3
        else:
            mx, my = mp
        
        r1 = math.degrees(math.atan2(y1 - my, x1 - mx))
        r2 = math.degrees(math.atan2(y2 - my, x2 - mx))
        r3 = math.degrees(math.atan2(y3 - my, x3 - mx))
        
        return "c" if (r1 > r2 > r3 or r2 > r3 > r1 or r3 > r1 > r2 ) else "cc"

    def calc_render(self):
        if self.color:
            self.surfaces.clear()
            for tri in self.tris:
                v1 = self.vertices[tri[0]]
                v2 = self.vertices[tri[1]]
                v3 = self.vertices[tri[2]]

                x1, y1 = self.project_point(v1)
                x2, y2 = self.project_point(v2)
                x3, y3 = self.project_point(v3)

                mx = (x1 + x2 + x3) / 3
                my = (y1 + y2 + y3) / 3

                r1 = math.degrees(math.atan2(y1 - my, x1 - mx))
                r2 = math.degrees(math.atan2(y2 - my, x2 - mx))
                r3 = math.degrees(math.atan2(y3 - my, x3 - mx))

                if (r1 > r2 > r3 or r2 > r3 > r1 or r3 > r1 > r2) and all(self.cam_position[2] < a for a in [v1[2], v2[2], v3[2]]):
                    # print("clockwise?")
                    # print(f"{x1=} {x2=} {x3=} {y1=} {y2=} {y3=}")
                    minX = min(x1, x2, x3)
                    maxX = max(x1, x2, x3)
                    minY = min(y1, y2, y3)
                    maxY = max(y1, y2, y3)
                    width = maxX - minX
                    height = maxY - minY

                    surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)

                    pygame.draw.polygon(surface,self.mod_color(v1, v2, v3), [(x1-minX, y1-minY), (x2-minX, y2-minY), (x3-minX, y3-minY)])
                    
                    # surface = pygame.transform.scale(surface, [2+surface.get_width(), 2+surface.get_height()])
                    # print(f"SURFACE: at {minX}, {minY} ({width}x{height})")
                    self.surfaces.append(((v1[2] + v2[2] + v3[2])/3, surface, minX, minY))

            self.surfaces.sort(
                key=lambda a: a[0]
            )
            self.surfaces.reverse()
        
        if self.texture_mapping:
            s2 = []
            for surface, quad in self.texture_mapping:
                v1 = self.vertices[quad[0]]
                v2 = self.vertices[quad[1]]
                v3 = self.vertices[quad[2]]
                v4 = self.vertices[quad[3]]

                color = [0, 0, 0, min(max(0, 255-self.mod_color(v1, v2, v3, self.brightness)[0]), 255)]

                x1, y1 = self.project_point(v1)
                x2, y2 = self.project_point(v2)
                x3, y3 = self.project_point(v3)
                x4, y4 = self.project_point(v4)

                mx = (x1 + x2 + x3 + x4) / 4
                my = (y1 + y2 + y3 + y4) / 4

                r1 = math.degrees(math.atan2(y1 - my, x1 - mx))
                r2 = math.degrees(math.atan2(y2 - my, x2 - mx))
                r3 = math.degrees(math.atan2(y3 - my, x3 - mx))
                r4 = math.degrees(math.atan2(y4 - my, x4 - mx))

                s = pygame.Surface(surface.get_size(), pygame.SRCALPHA, 32)
                s.blit(surface, (0, 0))
                _s = pygame.Surface(surface.get_size(), pygame.SRCALPHA, 32)
                _s.fill(color)
                s.blit(_s, (0, 0))

                if (r1 > r2 > r3 > r4 or r2 > r3 > r4 > r1 or r3 > r4 > r1 > r2 or r4 > r1 > r2 > r3) and all(self.cam_position[2] < a for a in [v1[2], v2[2], v3[2], v4[2]]) and Poly(((x1, y1), (x2, y2), (x3, y3), (x4, y4))).area >= 80:
                    out, pos = warp(s, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)], False)
                    s2.append(((v1[2] + v2[2] + v3[2] + v4[2])/4, out, int(min(x1, x2, x3, x4))-pos[0], int(min(y1, y2, y3, y4))-pos[1]))
            s2.sort(
                key=lambda a: a[0]
            )
            s2.reverse()
            self.surfaces += s2

        # vert = self.vertices.copy()
        # self.vertices.clear()
        # for v in vert:
        #     a, b = rotate((0, 200), (v[0], v[2]), 0.01)
        #     self.vertices.append([a, v[1], b])

    def _event(self, editor, X, Y):
        for c in self.controllers:
            c(self)
        self.calc_render()
    
    def _update(self, editor, X, Y):
        for _, surface, x, y in self.surfaces:
            pos = (X+x+(self.width/2)-self.cam_position[0], Y+y+(self.height/2)-self.cam_position[1])
            # print(pos)
            editor.screen.blit(surface, pos)
