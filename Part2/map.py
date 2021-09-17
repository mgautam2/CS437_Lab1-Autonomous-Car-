import numpy as np

class Map:
    
    def __init__(self, x, y, start_position, orientation):
        self.map = np.zeros((x,y), dtype=int)
        self.current_position = start_position
        self.orientation = orientation
        self.height = x
        self.width = y

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
        
