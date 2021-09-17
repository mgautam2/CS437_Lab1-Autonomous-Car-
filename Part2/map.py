import numpy as np
import math

class Map:
    
    def __init__(self, x, y, start_position, orientation):
        self.map = np.zeros((x,y), dtype=int)
        self.current_position = start_position
        self.orientation = orientation
        self.height = x
        self.width = y

    def insertMapSection(self, ultrasonicMap):
        ultrasonic_map_width = ultrasonicMap.shape[1]
        for i in range(ultrasonicMap.shape[0]):
            for j in range(ultrasonic_map_width):
                if (self.orientation == 0):
                    map_i_idx = self.current_position[0] + i
                    map_j_idx = self.current_position[1] + (j - math.floor(ultrasonic_map_width/2))
                elif (self.orientation == 1): # facing 'right'
                    map_i_idx = self.current_position[0] + (j - math.floor(ultrasonic_map_width/2))
                    map_j_idx = self.current_position[1] - i
                elif (self.orientation == 2): # facing 'down'
                    map_i_idx = self.current_position[0] - i
                    map_j_idx = self.current_position[1] - (j - math.floor(ultrasonic_map_width/2))
                elif (self.orientation == 3): # facing 'left'
                    map_i_idx = self.current_position[0] - (j - math.floor(ultrasonic_map_width/2))
                    map_j_idx = self.current_position[1] + i
                else:
                    print("ERROR: UNKNWON ORIENTATION IN MAP.PY:", self.orientation)
                    map_i_idx = 0
                    map_j_idx = 0
                if (map_i_idx >= 0 and map_i_idx < self.map.shape[0] and map_j_idx >= 0 and map_j_idx < self.map.shape[1]):
                    self.map[map_i_idx][map_j_idx] = ultrasonicMap[i][j]


    def printSelf(self):
        print(self.map)
        print(self.current_position)
        print(self.orientation)

    def getLabelAtPoint(self, point):
        return self.map[point[0]][point[1]]
    
    def setLabelAtPoint(self, point, label):
        self.map[point[0]][point[1]] = label

    def isPointInBounds(self, point):
        x, y = point
        if x < self.width and x >= 0 and y < self.height and y >= 0:
            return True
        return False
        
