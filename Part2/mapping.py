import picar_4wd as fc
import math
import numpy as np

ANGLE_RANGE = 160
STEP = 10
us_step = STEP
current_angle = -80
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2

errors = []
map = np.zeros([25, 50], dtype=int)

def scan_step_return_distances():
    global scan_list, current_angle, us_step, x_list, y_list, angle_list, map
    # set the current angle
    current_angle += us_step
    print("current angle: ", current_angle)
    if current_angle >= max_angle:
        current_angle = max_angle
        us_step = -STEP
    elif current_angle <= min_angle:
        current_angle = min_angle
        us_step = STEP
    
    # find the distance to the object and the x/y components
    distance = fc.get_distance_at(current_angle)
    print("current distance: ", distance)
    # y_idx = round(distance/4)
    # x_idx = round((math.tan(math.radians((current_angle)))*distance)/4)
    y_idx = round((math.cos(math.radians((current_angle)))*distance)/4)
    x_idx = round((math.sin(math.radians((current_angle)))*distance)/4)
    x_idx = x_idx + 25 # shift horizontal distances by 1/2 the size of the grid for indexing

    # save the objects coordinates and their distances/angles (reject ones that are far away or not detected)
    if distance != -2 and y_idx < 25 and x_idx >= 0 and x_idx < 50:
        print("adding (", x_idx, ",", y_idx, ") from angle", current_angle , " and distance ", distance)
        map[24-y_idx][49-x_idx] = 1


def main():
    global map
    while True:
        scan_step_return_distances()
        

if __name__ == "__main__":
    try:
        main()
    finally:
        # print("done")
        fc.get_distance_at(0) #hack to set the servo position back to center
        for row in range(map.shape[0]):
            for col in range(map.shape[1]):
                print(map[row][col], end=', ')
            print('\n', end='')
        

