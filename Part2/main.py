import time
import sys
import signal
import argparse
import threading

import picar_4wd as fc
from picar_4wd.ultrasonic import Ultrasonic
import mapping as mp
import detect_object as do
import routing as rt
import map as ma
import drive as dv

class myThread(threading.Thread):
    def __init__(self, threadID, name, map, map_lock):    
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.map = map
        self.map_lock = map_lock

    def run(self):

        # Routing, drive and mapping instance thread
        if self.threadID == 1:
            pass

        # Camera instance thread
        if self.threadID == 2:
            eye = do.Eye(self.map, self.map_lock)
            eye.main()


def signal_handler(sig, frame):
    fc.stop()
    sys.exit(0)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Create map and routing input")
    parser.add_argument('--h', help='Total cells in the x direction', required=True, type=int, default=100)
    parser.add_argument('--w', help='Total cells in the y direction', required=True, type=int, default=100)
    parser.add_argument('--starth', help='Start x coord', required=True, type=int, default=0)
    parser.add_argument('--startw', help='Start y coord', required=True, type=int, default=0)
    parser.add_argument('--endh', help='End x coord', required=True, type=int, default=100)
    parser.add_argument('--endw', help='End y coord', required=True, type=int, default=100)
    parser.add_argument('--orientation', help='0: -ve height direction, 1: +ve width direction, 2: +ve height direction, 3: -ve width direction', required=True, type=int, default=2)
    args = parser.parse_args()

    # Initialise routing parameters and Map
    map = ma.Map(args.h, args.w, (args.starth, args.startw), args.orientation)
    map_lock = threading.Lock()
    threads = []

    # Create thread for camera
    eye_thread = myThread(2, "Eye", map, map_lock)
    threads.append(eye_thread)

    # Run threads
    for t in threads:
        t.start()

    # Create thread for routing algorithm and driving
    driver = dv.Drive(map)
    while map.current_position != (args.endh, args.endw):
        map.scanSurroundings()
        route = rt.astar(map.map, map.current_position, (args.endh, args.endw))
        for step in route:
            print(step)
            # driver.drive_step(step)

    # Wait for threads to complete and join threads
    for t in threads:
        t.join()
