import enum
import time
import picar_4wd as fc

import map 
import mapping 
import constants
import routing

power_to_speed = {
    20: 35.5,
    30: 39.5,
    40: 44.1,
    50: 47.7,
    60: 52.5,
    70: 55.4,
    80: 59.5,
    90: 62.9 
}

power_right_turn_time = {
10: 3.95
}

power_left_turn_time = {
10: 3.8
}

power_val = 20
turn_power_val = 10
GRID_SIZE = 20

class Dir(enum.Enum):
   Up = 0
   Right = 1
   Down = 2
   Left = 3

class Drive:

    def __init__(self, direction = Dir.Right, pos = (0, 0)):
        self.direction = direction
        self.pos = pos

    def turning_dir(self, new_pos):
        dir = ''

        if (new_pos[0] == self.pos[0] - 1) and (new_pos[1] == self.pos[1]):
            dir = Dir.Up
        elif (new_pos[0] == self.pos[0]) and (new_pos[1] == self.pos[1] - 1):
            dir = Dir.Left
        elif (new_pos[0] == self.pos[0]) and (new_pos[1] == self.pos[1] + 1):
            dir = Dir.Right
        else:
            dir = Dir.Down

        return dir

    def dir_from_val(val):
        if (val == 0):
            return Dir.Up
        elif (val == 1):
            return Dir.Right
        elif (val == 2):
            return Dir.Down
        elif (val == 3):
            return Dir.Left 

    def update_pos(self):
        if (self.direction == Dir.Up):
            self.pos = (self.pos[0] - 1, self.pos[1])
        elif (self.direction == Dir.Right):
            self.pos = (self.pos[0], self.pos[1] + 1)
        elif (self.direction == Dir.Down):
            self.pos = (self.pos[0] + 1, self.pos[1])
        elif (self.direction == Dir.Left):
            self.pos = (self.pos[0], self.pos[1] - 1)

    """
    Rotate the car
    """
    def turn(self, new_dir):
        dir_num = new_dir.value - self.direction.value
        print("Turning ->  " + new_dir.name)
        
        if (dir_num > 0):
            fc.turn_right(turn_power_val)
            sleep_time = ( dir_num * power_right_turn_time[turn_power_val] ) / 4
            time.sleep(sleep_time)
            fc.stop() 
            
        elif (dir_num < 0):
            fc.turn_left(turn_power_val)
            sleep_time = ( abs(dir_num) * power_left_turn_time[turn_power_val] ) / 4
            time.sleep(sleep_time)
            fc.stop() 

        self.direction = new_dir   

    def translate(self): 
        print("Moveing  -> " + self.direction.name)
        
        fc.forward(power_val)
        sleep_time = GRID_SIZE / power_to_speed[power_val]
        time.sleep(sleep_time)
        fc.stop() 
        self.update_pos()

    """
    Main drive function 
    """
    def drive_step(self, new_pos):
        
        if (self.pos == new_pos):
            return

        new_dir = self.turning_dir(new_pos)
        self.turn(new_dir)
        self.translate()
        print("New pos is " + str(self.pos) + " And direction is " + self.direction.name +"\n-----------------")


# TEST THE PATH
maze = map.Map(30, 30, (0, 0), constants.RIGHT)

faltu_mapping = mapping.UltrasonicMap()
maze.scanSurroundings()
faltu_mapping.print_map(maze.map)
route = routing.astar(maze.map, (0, 0), (20, 20))

d = Drive()
print("Starting pos is " + str(d.pos) + " And direction is " + d.direction.name +"\n-----------------")


for step in route:
    print(step)
    # d.drive_step(step)
