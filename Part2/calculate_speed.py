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


if __name__ == "__main__":
    printRotateTime(20)
    time.sleep(0.8125)
    fc.stop()
    
