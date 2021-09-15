import enum
import time
import picar_4wd as fc


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

power_to_turn_time = {
    20: 3.25
}

power_val = 40
turn_power_val = 20
GRID_SIZE = 30

class Dir(enum.Enum):
   Up = 0
   Right = 1
   Left = 2
   Down = 3

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
            return Dir.Left
        elif (val == 3):
            return Dir.Down

    """
    Rotate the car
    """
    def turn(self, dir_num):
        print("Turning")
        if (dir_num > 0):
            fc.right(turn_power_val)
            sleep_time = dir_num * GRID_SIZE / power_to_turn_time[turn_power_val]
            time.sleep(sleep_time)
            fc.stop() 
            
        elif (dir_num < 0):
            fc.left(turn_power_val)
            sleep_time = abs(dir_num) * GRID_SIZE / power_to_turn_time[turn_power_val]
            time.sleep(sleep_time)
            fc.stop()    
        pass

    """
    Translate the car
    """
    def translate(self): 
        print("Move")
        # move a car in a particular direction for one unit
        fc.forward(power_val)
        sleep_time = GRID_SIZE / power_to_speed[power_val]
        time.sleep(sleep_time)
        fc.stop() 

    """
    Main drive function 
    """
    def drive(self, new_pos):
        
        new_dir = self.turning_dir(new_pos)
        self.turn(self.direction.value - new_dir.value)
        self.translate()
        
d = Drive()
d.drive((0,1))

