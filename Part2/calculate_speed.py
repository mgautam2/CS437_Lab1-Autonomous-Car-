from os import name
import picar_4wd as fc
import time

def printMoveSpeed(power):
    distance_start = fc.get_distance_at(0)
    time.sleep(1)
    fc.forward(power)
    time.sleep(1)
    fc.stop()
    time.sleep(1)
    distance_end = fc.get_distance_at(0)

    print("Start:    " + str(distance_start))
    print("End:      " + str(distance_end))
    print("Speed:    " + str(distance_start - distance_end))
    
def printRotateTime(power):
    fc.turn_left(power)

# power_to_speed = {
#     20: 35.5,
#     30: 39.5,
#     40: 44.1,
#     50: 47.7,
#     60: 52.5,
#     70: 55.4,
#     80: 59.5,
#     90: 62.9 
# }

# power_to_turn_time = {
#     20: 3.25,
#     30: ,
#     40: ,
#     50: ,
#     60: ,
#     70: ,
#     80: ,
#     90: 
# }

if __name__ == "__main__":
    printRotateTime(20)
    time.sleep(0.8125)
    fc.stop()
    
