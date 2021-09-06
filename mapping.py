import picar_4wd as fc
import time
from random import random 

# Helper function which returns true if obstacle is within x cm
def isAnythingInFront():

    # Using implementation from obstacle_avoidance.py in examples
    # scan_list = fc.scan_step(35)
    # if not scan_list:
    #     return False

    # tmp = scan_list[3:7]
    # return tmp != [2,2,2,2]

    # Don't turn servo, just return True when distance is 50 cm
    threshhold = 50
    distance = fc.get_distance_at(0)
    if distance > threshhold or distance == -2:
        return False
    else:
        return True

# Helper function which turns to a random angle
def turnRandom():
    power = 50
    time = 2.5 

    fc.turn_left(power)
    time.sleep(random()*time)
    fc.stop()
    