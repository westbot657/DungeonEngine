# pylint: disable=W,R,C,import-error, no-member

import heapq
import math
import cython

class Pathfinding:
    
    class Plane:
        
        class _intermediate(list):
            instance = None
            def __init__(self, plane):
                self.plane = plane
                self.x: cython.int = 0
            
            def __getitem__(self, y: cython.int):
                return self.plane.get_point(self.x, y)
            
            # def __setitem__(self, index, val):
            #     print(f"set {self.x}, {index} to {val}")

        def add_shape(self, grid, offset:tuple[int, int]=None):
            x, y = offset = offset or (0, 0)
            x: cython.int
            y: cython.int
            points = []
            
            
            for h in grid:
                y = offset[1]
                for val in h:
                    if val:
                        points.append((y, x))
                    y += 1
                    
                x += 1
            
            self.add_points(points)
        
        def __init__(self, points:list[tuple[int, int]]=None):
            points = points if points is not None else []
            self.intermediate = Pathfinding.Plane._intermediate(self)
            self.regions = set()

            self.minX: cython.int
            self.minY: cython.int
            self.maxX: cython.int
            self.maxY: cython.int

            self.map = set()
            if points:
                self.minX, self.minY = self.maxY, self.maxY = points[0]
                self.maxX += 1
                self.maxY += 1
            else:
                self.minX, self.minY = self.maxX, self.maxY = (0, 0)

            self.add_points(points)

        def add_points(self, points):
            for point in points:
                self.minX = min(self.minX, point[0])
                self.maxX = max(self.maxX, point[0]+1)
                self.minY = min(self.minY, point[1])
                self.maxY = max(self.maxY, point[1]+2)
            self.shape = [self.minX, self.minY, self.maxX+1, self.maxY+1]
            self.map.update(points)
            
        def add_region(self, rect:tuple[int, int, int, int]) -> cython.void:
            self.regions.add(rect)

        def get_point(self, x, y) -> cython.int:
            if (x, y) in self.map:
                return 1
            else:
                for x1, y1, w, h in self.regions:
                    if x1 <= x < x1+w and y1 <= y < y1+h:
                        return 1
            return 0
            
        def __getitem__(self, x):
            self.intermediate.x = x
            return self.intermediate
        
    @classmethod
    def vectorize(cls, path_points:set) -> set:
        """
        Takes a list of points chosen by pathfinding, and returns the smallest list of points that when connected, draw the same line
        """
        direction = None
        output = set()
        i = 0
        for point in path_points[1:]:
            prev_point = path_points[i]
            
            if direction is None:
                output.add(prev_point)
            
            if prev_point[0] < point[0]:
                if prev_point[1] < point[1]:
                    new_dir = 1 # tl-br
                elif prev_point[1] > point[1]:
                    new_dir = 2 # bl-tr
                else:
                    new_dir = 3 # l-r
            elif prev_point[0] > point[0]:
                if prev_point[1] < point[1]:
                    new_dir = 4 # tr-bl
                elif prev_point[1] > point[1]:
                    new_dir = 5 # br-tl
                else:
                    new_dir = 6 # r-l
            
            else:
                if prev_point[1] < point[1]:
                    new_dir = 7 # t-b
                else:
                    new_dir = 8 # b-t

            if new_dir != direction:
                output.add(prev_point)
                direction = new_dir
            
            
            if point == path_points[-1]:
                output.add(point)
            
            i += 1
        
        return output

    @classmethod
    def astar_heuristic(cls, x:tuple[int, int], y:tuple[int, int]) -> cython.float:
        return math.sqrt(((y[1]-x[1])**2) + ((y[0]-x[0])**2))
    
    @classmethod
    def astar(cls, array, start, goal):
        neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
        close_set = set()
        came_from = {}
        gscore = {start:0}
        fscore = {start:cls.astar_heuristic(start, goal)}
        oheap = []
        heapq.heappush(oheap, (fscore[start], start))

        while oheap:
            current = heapq.heappop(oheap)[1]
            if current == goal:
                data = [start]
                while current in came_from:
                    data.append(current)
                    current = came_from[current]
                return data
            close_set.add(current)
            for i, j in neighbors:
                neighbor = current[0] + i, current[1] + j
                tentative_g_score = gscore[current] + cls.astar_heuristic(current, neighbor)
                if array.shape[0] <= neighbor[0] < array.shape[2]:
                    if array.shape[1] <= neighbor[1] < array.shape[3]:
                        if array[neighbor[0]][neighbor[1]] == 1:
                            continue
                    else:
                        # array bound y walls
                        continue
                else:
                    # array bound x walls
                    continue

                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue

                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + cls.astar_heuristic(neighbor, goal)
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))
        return False

    @classmethod
    def astar_linear(cls, array, start, goal):
        neighbors = [(0,1),(0,-1),(1,0),(-1,0)]
        close_set = set()
        came_from = {}
        gscore = {start:0}
        fscore = {start:cls.astar_linear_heuristic(start, goal, None)}  # Pass None as prev for start node
        oheap = []
        heapq.heappush(oheap, (fscore[start], start))

        while oheap:
            current = heapq.heappop(oheap)[1]
            if current == goal:
                data = [start]
                while current in came_from:
                    data.append(current)
                    current = came_from[current]
                return data
            close_set.add(current)
            for i, j in neighbors:
                neighbor = current[0] + i, current[1] + j
                tentative_g_score = gscore[current] + cls.astar_linear_heuristic(current, neighbor, came_from.get(current))

                if array.shape[0] <= neighbor[0] < array.shape[2]:
                    if array.shape[1] <= neighbor[1] < array.shape[3]:
                        if array[neighbor[0]][neighbor[1]] == 1:
                            continue
                    else:
                        # array bound y walls
                        continue
                else:
                    # array bound x walls
                    continue

                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue

                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + cls.astar_linear_heuristic(neighbor, goal, came_from.get(neighbor))
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))
        return False

    @classmethod
    def astar_linear_heuristic(cls, current, goal, prev) -> cython.double:
        # Euclidean distance as base heuristic
        base_heuristic = ((goal[0] - current[0]) ** 2 + (goal[1] - current[1]) ** 2) ** 0.5
        
        # Calculate the direction from current to goal
        dx = goal[0] - current[0]
        dy = goal[1] - current[1]
        direction_to_goal = (dx, dy)
        
        # Calculate the direction from current to previous node
        if prev is not None:
            dx_prev = current[0] - prev[0]
            dy_prev = current[1] - prev[1]
            direction_to_prev = (dx_prev, dy_prev)
        else:
            direction_to_prev = None
        
        # Penalize turns by checking if directions are different
        if direction_to_prev is not None and direction_to_prev != direction_to_goal:
            turn_penalty = 0.5  # Adjust this value as needed
        else:
            turn_penalty = 0
        
        # Apply turn penalty to the base heuristic
        return base_heuristic + turn_penalty