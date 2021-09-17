import heapq
import numpy as np
import test_maze


GRID_SIZE = 30
MAZE = test_maze.maze
start_pos = (0, 0)
end_pos = (10, 10)
curr_pos = start_pos

class Node:
    def __init__(self, pos, parent, p_cost = 0, g_h = 0):
        self.pos = pos
        self.parent = parent
        self.p_cost = p_cost
        self.g_h = g_h

    def __eq__(self, other):
        return (self.g_h == other.g_h) 

    def __ne__(self, other):
        return not (self.g_h == other.g_h)

    def __lt__(self, other):
        return (self.g_h < other.g_h)

    def __gt__(self, other):
        return (self.g_h > other.g_h) 

    def __le__(self, other):
        return (self.g_h < other.g_h) or (self.g_h == other.g_h)

    def __ge__(self, other):
        return (self.g_h > other.g_h) or (self.g_h == other.g_h)

def manhattan_dist(pos, end):
    dist = (pos[0] - end[0])**2 + (pos[1] - end[1])**2
    return dist

def get_neighbors(pos):
    neighbors = []
    rowNbr = [-1,0,0,1]
    colNbr = [0,-1,1,0]

    for i in range(4):
        if (pos[0] + rowNbr[i] < MAZE.shape[0] and pos[0] + rowNbr[i] >= 0):
            if (pos[1] + colNbr[i] < MAZE.shape[1] and pos[1] + colNbr[i] >= 0):
                neighbors.append((pos[0] + rowNbr[i], pos[1] + colNbr[i]))
    
    return neighbors

def astar():
    path = []
    state = Node( start_pos, None, 0, 0)
    list = []
    heapq.heappush(list, (state.g_h, state))
    visited = {state.pos : state}

    while (list):
        state = heapq.heappop(list)[1]

        if (state.pos == end_pos):
            break
        
        neighbors = get_neighbors(state.pos)

        for neighbor in neighbors:
                if (neighbor not in visited or visited[neighbor].p_cost > state.p_cost + 1 ):
                    neigh_state = Node(neighbor, state.pos, state.p_cost + 1, state.p_cost + 1 + manhattan_dist(neighbor, end_pos))
                    heapq.heappush(list, (neigh_state.g_h, neigh_state))
                    visited[neigh_state.pos] =  neigh_state

    path.insert(0, state.pos)
    parent = state.parent
    
    
    while (parent != None):
        path.insert(0, visited[parent].pos)
        parent = visited[parent].parent

    print("-------")
    for x in visited:
        print(str(x)+ "the manHat is " + str(manhattan_dist(x, end_pos)) + " the path cost is " + str(visited[x].p_cost)  + " the parent is : "+ str(visited[x].parent) )

    
    print()
    print(path)
    return path
    
astar()