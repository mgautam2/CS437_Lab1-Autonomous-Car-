import enum
import time
import picar_4wd as fc

import map 
import mapping 
import constants 
import routing


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
            print("Stopping")
            time.sleep(2)

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
        self.translate()
        self.check_stop_sign()
