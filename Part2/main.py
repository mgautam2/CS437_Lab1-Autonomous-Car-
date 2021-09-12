import time
import sys
import signal
import argparse
import _thread

import picar_4wd as fc
import mapping as mp
import detect_object as do
import routing as rt
import map as ma

def signal_handler(sig, frame):
    fc.stop()
    sys.exit(0)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Create map and routing input")
    parser.add_argument('--x', help='Total cells in the x direction', required=True, type=int, default=100)
    parser.add_argument('--y', help='Total cells in the y direction', required=True, type=int, default=100)
    parser.add_argument('--startx', help='Start x coord', required=True, type=int, default=0)
    parser.add_argument('--starty', help='Start y coord', required=True, type=int, default=0)
    parser.add_argument('--endx', help='End x coord', required=True, type=int, default=100)
    parser.add_argument('--endy', help='End y coord', required=True, type=int, default=100)
    args = parser.parse_args()

    # Initialise routing parameters and Map
    map = ma.Map(args.x, args.y, (args.startx, args.starty))

    # Initialise oject detection object

    # Create thread for mapping and ultrasonic sensor

    # Create thread for routing algorithm and driving

    # Create thread for camera
    eye = do.Eye(map)
    try:
        _thread.start_new_thread( eye.main(), ("Camera thread") )
    except:
        print ("Error: unable to start thread")

    while True:
        pass
