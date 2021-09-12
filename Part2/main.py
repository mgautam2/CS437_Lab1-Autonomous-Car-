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

    # Initialise routing parameters and Map

    # Initialise oject detection object

    # Create thread for routing algorithm and ultrasonic sensor

    # Create thread for camera

    pass
