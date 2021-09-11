import picar_4wd as fc
import math
import numpy as np

ANGLE_RANGE = 180
STEP = 10
us_step = STEP
current_angle = -us_step
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2

errors = []
map = np.zeros([100,200], dtype=int)

def scan_step_return_distances():
    global scan_list, current_angle, us_step, x_list, y_list, angle_list, map
    # set the current angle
    current_angle += us_step
    if current_angle >= max_angle:
        current_angle = max_angle
        us_step = -STEP
    elif current_angle <= min_angle:
        current_angle = min_angle
        us_step = STEP
    
    # find the distance to the object and the x/y components
    status = fc.get_distance_at(current_angle)
    y_dist = round(math.cos(math.radians(abs(current_angle)))*status)
    x_dist = round(math.sin(math.radians(abs(current_angle)))*status)
    if (current_angle < 0):
        x_dist = x_dist * -1
    x_dist = x_dist + 100 # shift horizontal distances by 1/2 the size of the grid for indexing

    # save the objects coordinates and their distances/angles (reject ones that are far away or not detected)
    if status != -2 and status < 100:
        print("adding (", x_dist-100, ",", y_dist, ") from angle", current_angle , " and distance ", status)
        map[y_dist][x_dist] = 1


def main():
    global map
    while True:
        scan_step_return_distances()
        

if __name__ == "__main__":
    try:
        main()
    finally:
        # print("done")
        for row in range(map.shape[0]):
            for col in range(map.shape[1]):
                print(map[row][col], end=', ')
            print('\n', end='')
        
    fc.get_distance_at(0) #hack to set the starting position to the left

