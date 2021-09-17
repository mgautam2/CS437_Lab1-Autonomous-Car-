# 0. Unknown
# 1. Free Space
# 2. Walls
# 3. Stop signs - Come to complete stop, look around for traffic, then continue moving
# 4. Traffic cones - Reduce power to 20
# 5. Not defined
# 6. Not defined
# 7. Not defined
# 8. Not defined
# 9. Current car position

import numpy as np
import math

class Map:
    
    def __init__(self, x, y, start_position):
        self.map = np.zeros((x,y), dtype=int)
        self.current_position = start_position
        self.orientation = 0

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