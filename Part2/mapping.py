import picar_4wd as fc
import math
import numpy as np
from constants import *

ANGLE_RANGE = 160
STEP = 10
us_step = STEP
current_angle = -80
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2
prev_point = (0,0)

map = np.full([100,200], UNKNOWN_SPACE, dtype=int)
condensed_map = np.full([20, 40], UNKNOWN_SPACE, dtype=int)

def plotLine(x0, y0, x1, y1, type=UNCLASSIFIED_OBJECT):
    dx =  abs(x1-x0)
    sx = 1 if x0<x1 else -1
    dy = -abs(y1-y0)
    sy = 1 if y0<y1 else -1
    err = dx+dy
    while (True):
        if (map[x0][y0] != UNCLASSIFIED_OBJECT):
            map[x0][y0] = type
        if (x0 == x1 and y0 == y1):
            break
        e2 = 2*err
        if (e2 >= dy):
            err += dy
            x0 += sx
        if (e2 <= dx):
            err += dx
            y0 += sy

def scan_step_return_distances():
    global scan_list, current_angle, us_step, x_list, y_list, angle_list, map, prev_point
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
    y_idx = round((math.cos(math.radians((current_angle)))*distance))
    x_idx = round((math.sin(math.radians((current_angle)))*distance))
    x_idx = x_idx + 100 # shift horizontal distances by 1/2 the size of the grid for indexing

    # save the objects coordinates and their distances/angles (reject ones that are far away or not detected)
    if distance != -2 and y_idx < 100 and x_idx >= 0 and x_idx < 200:
        print("adding (", x_idx, ",", y_idx, ") from angle", current_angle , " and distance ", distance)
        map[y_idx][x_idx] = UNCLASSIFIED_OBJECT
        print("prev_point: ", prev_point)
        if (prev_point[0] != 0 and prev_point[1] != 0):
            if (((prev_point[0] - y_idx)**2) + ((prev_point[1] - x_idx)**2) < 30**2):
                # print("drawing line from ", prev_point, "to ", (y_idx,x_idx))
                plotLine(prev_point[0], prev_point[1], y_idx, x_idx)
        prev_point = (y_idx,x_idx)
    else:
        prev_point = (0,0)

# def mark_free_space():
#     for i in range(100):
#         for j in range(200):
#             if (map[i][j] == UNCLASSIFIED_OBJECT):
#                 print("drawing line from (0,19) to ", (i, j))
#                 plotLine(i, j, 0, 19, type=FREE_SPACE)

def condense():
    # clear the condensed map
    for i in range(100):
        for j in range(200):
            if (map[i][j] == UNCLASSIFIED_OBJECT):
                condensed_map[math.floor(i/5)][math.floor(j/5)] = UNCLASSIFIED_OBJECT
            elif (map[i][j] == FREE_SPACE and condensed_map[math.floor(i/5)][math.floor(j/5)] != UNCLASSIFIED_OBJECT):
                condensed_map[math.floor(i/5)][math.floor(j/5)] = FREE_SPACE

def main():
    global map, condensed_map
    map = np.full([100,200], UNKNOWN_SPACE, dtype=int)
    condensed_map = np.full([20, 40], UNKNOWN_SPACE, dtype=int)
    for i in range(64):
        scan_step_return_distances()
    
    fc.get_distance_at(0) #hack to set the servo position back to center
    print('\n\n', end='')
    condense()
    for row in range(condensed_map.shape[0]):
        for col in range(condensed_map.shape[1]):
            print(condensed_map[19-row][39-col], end=', ')
        print('\n', end='')
        

if __name__ == "__main__":
    main()

        

