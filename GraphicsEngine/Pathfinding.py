# pylint: disable=W,R,C,import-error

import heapq
import math

class Pathfinding:
    
    class Plane:
        
        class _intermediate:
            instance = None
            def __init__(self, plane):
                self.plane = plane
                self.x = 0
            
            def __getitem__(self, y):
                return self.plane.get_point(self.x, y)
        
        def convert(self, grid, offset:tuple[int, int]=None):
            x, y = offset or (0, 0)
            points = []
            for h in grid:
                for val in h:
                    if val:
                        points.append((x, y))
                    y += 1
                    
                x += 1
            
            self.add_points(points)
        
        def __init__(self, points:list[tuple[int, int]]=None):
            points = points if points is not None else []
            self.intermediate = Pathfinding.Plane._intermediate(self)

            self.map = set()
            self.minX = 0
            self.maxX = 0
            self.minY = 0
            self.maxY = 0

            self.add_points(points)
            

        def add_points(self, points):
            for point in points:
                self.minX = min(self.minX, point[0])
                self.maxX = max(self.maxX, point[0])
                self.minY = min(self.minY, point[1])
                self.maxY = max(self.maxY, point[1])
            self.shape = [self.minX, self.minY, self.maxX, self.maxY]
            self.map.update(points)
            

        def get_point(self, x, y):
            if (x, y) in self.map:
                return 1
            return 0
            
        def __getitem__(self, x):
            self.intermediate.x = x
            return self.intermediate

    @classmethod
    def astar_heuristic(cls, x:tuple[int, int], y:tuple[int, int]):
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
                data = []
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

                if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
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
                data = []
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

                if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + cls.astar_linear_heuristic(neighbor, goal, came_from.get(neighbor))
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))
        return False

    @classmethod
    def astar_linear_heuristic(cls, current, goal, prev):
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
