# import isAnythingInFront, stopAndTurnRandom
import mapping
import picar_4wd as fc
import sys
import signal

def signal_handler(sig, frame):
    fc.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":

    # Run while loop and coordinate all helper functions
    speed = 30
    while (True):
        fc.forward(30)
        atObstacle = mapping.isAnythingInFront()
        if (atObstacle == True):
            fc.stop()
            mapping.turnRandomAndStop()
        else:
            fc.forward(speed)
