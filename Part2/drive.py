import enum
import time
import picar_4wd as fc

import map 
import mapping 
import constants 
import routing

# from ..picar_4wd.Ultrasonic import Ultrasonic
                     
us = fc.Ultrasonic(fc.Pin('D8'), fc.Pin('D9'))                


class Drive:

    def __init__(self, map):
        self.map = map
        self.stop_sign_flag = False
        
    def check_stop_sign(self):
        x = self.map.current_position[0]
        y = self.map.current_position[1]

        if (self.map.map[x][y] != constants.STOP_SIGN_ADJACENT):
            self.stop_sign_flag = False
            return
        
        if (self.stop_sign_flag == False):
            self.stop_sign_flag = True
            time.sleep(2)

    def emergency_stop(self):
        global us
        distance = us.get_distance() 
        print(distance)
        print("--")
        x1, y1 = self.map.current_position
        x2, y2 = self.map.current_position

        if self.map.orientation == constants.UP:
            x1 -= 1
            x2 -= 2
        if self.map.orientation == constants.RIGHT:
            y1 += 1
            y2 += 2
        if self.map.orientation == constants.DOWN:
            x1 += 1
            x2 += 2
        if self.map.orientation == constants.LEFT:
            y1 -= 1
            y2 -= 2

        while (distance < 20 and distance > 2) and ( self.map.isPointInBounds((x1, y1)) and self.map.map[x1][y1] == constants.FREE_SPACE) :    
            fc.stop()
            distance = us.get_distance() 
            print("stop")
            
        print("exitted")

  # nd ( self.map.isPointInBounds((x2, y2)) and self.map.map[x2][y2] == constants.FREE_SPACE)

    def turning_dir(self, new_pos):
        dir = ''

        if (new_pos[0] == self.map.current_position[0] - 1) and (new_pos[1] == self.map.current_position[1]):
            dir = constants.UP
        elif (new_pos[0] == self.map.current_position[0]) and (new_pos[1] == self.map.current_position[1] - 1):
            dir = constants.LEFT
        elif (new_pos[0] == self.map.current_position[0]) and (new_pos[1] == self.map.current_position[1] + 1):
            dir = constants.RIGHT
        else:
            dir = constants.DOWN

        return dir

    def dir_from_val(val):
        if (val == 0):
            return constants.UP
        elif (val == 1):
            return constants.RIGHT
        elif (val == 2):
            return constants.DOWN
        elif (val == 3):
            return constants.LEFT 

    def update_pos(self):
        if (self.map.orientation == constants.UP):
            self.map.current_position = (self.map.current_position[0] - 1, self.map.current_position[1])
        elif (self.map.orientation == constants.RIGHT):
            self.map.current_position = (self.map.current_position[0], self.map.current_position[1] + 1)
        elif (self.map.orientation == constants.DOWN):
            self.map.current_position = (self.map.current_position[0] + 1, self.map.current_position[1])
        elif (self.map.orientation == constants.LEFT):
            self.map.current_position = (self.map.current_position[0], self.map.current_position[1] - 1)

    """
    Rotate the car
    """
    def turn(self, new_dir):
        dir_num = new_dir - self.map.orientation
        
        if (dir_num > 0):
            fc.turn_right(constants.TURN_POWER)
            sleep_time = ( dir_num * constants.POWER_RIGHT_TURN_TIME[constants.TURN_POWER] ) / 4
            time.sleep(sleep_time)
            fc.stop() 
            
        elif (dir_num < 0):
            fc.turn_left(constants.TURN_POWER)
            sleep_time = ( abs(dir_num) * constants.POWER_LEFT_TURN_TIME[constants.TURN_POWER] ) / 4
            time.sleep(sleep_time)
            fc.stop() 

        self.map.orientation = new_dir   

    def translate(self): 
        
        fc.forward(constants.DRIVE_POWER)
        sleep_time = constants.GRANULARITY / constants.POWER_TO_SPEED[constants.DRIVE_POWER]
        time.sleep(sleep_time)
        fc.stop() 
        self.update_pos()

    """
    Main drive function 
    """
    def drive_step(self, new_pos):

        if (self.map.current_position == new_pos):
            return

        temp_orientation = self.turning_dir(new_pos)
        self.turn(temp_orientation)
        self.map.orientation = temp_orientation
        self.emergency_stop()
        self.translate()
        self.check_stop_sign()



# map = map.Map(30, 30, (0, 0), constants.RIGHT)
# driver = Drive(map)

# while map.current_position != (10, 3):
#     map.scanSurroundings()
#     route = routing.astar(map.map, map.current_position, (10, 3))
#     print(route)
#     for step in route:
#         print(step)
#         driver.drive_step(step)