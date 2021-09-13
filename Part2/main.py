import time
import sys
import signal
import argparse
import _thread
import threading

import picar_4wd as fc
import mapping as mp
import detect_object as do
import routing as rt
import map as ma

class myThread(threading.Thread):
    def __init__(self, threadID, name, map, map_lock):    
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.map = map
        self.map_lock = map_lock

    def run(self):

        # Routing and drive instance thread
        if self.threadID == 1:
            pass

        # Mapping instance thread
        if self.threadID == 2:
            pass

        # Camera instance thread
        if self.threadID == 3:
            eye = do.Eye(self.map, self.map_lock)
            eye.main()


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
    map_lock = threading.Lock()
    threads = []

    # Initialise oject detection object

    # Create thread for mapping and ultrasonic sensor

    # Create thread for routing algorithm and driving

    # Create thread for camera
    eye_thread = myThread(3, "Eye", map, map_lock)
    threads.append(eye_thread)

    # Run threads
    for t in threads:
        t.start()

    # Wait for threads to complete and join threads
    for t in threads:
        t.join()
