# pylint: disable=W,R,C,import-error

import heapq
import math
import numpy

class Pathfinding:

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
                if 0 <= neighbor[0] < array.shape[0]:
                    if 0 <= neighbor[1] < array.shape[1]:
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


