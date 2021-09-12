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

class Map:
    
    def __init__(self, x, y, start_position):
        self.map = np.zeros((x,y), dtype=int)
        self.current_position = start_position
        self.orientation = 0

    def printSelf(self):
        print(self.map)
        print(self.current_position)
        print(self.orientation)