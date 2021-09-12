import time
import sys
import signal

import picar_4wd as fc
import mapping as mp
import detect_object as do
import routing as rt

def signal_handler(sig, frame):
    fc.stop()
    sys.exit(0)

if __name__ == "__main__":

    # Initialise routing parameters

    eye = do.Eye()

    eye.classifyImage()

    # Run while loop
    while True:

        # Stop and build relative map

        # Use A star to get to best possible location on current map

        while True:

            # Move to that location

            # While driving, keep getting ultrasonic sensor data and 
            # if an object exists in front, use openCV to detect object
            pass

