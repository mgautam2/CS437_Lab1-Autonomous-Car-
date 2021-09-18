UNKNOWN_SPACE = 0
UNCLASSIFIED_OBJECT = 1
FREE_SPACE = 2
WALL = 3
TRAFFIC_CONE = 4
LIVING_THING = 5
STOP_SIGN = 6
CURRENT_CAR_POSITION = 9

GRANULARITY = 5
RELATIVE_MAP_WIDTH = 200 / GRANULARITY
RELTAIVE_MAP_HEIGHT = 100 / GRANULARITY

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

LABEL_TO_MAP = {
    0: 5,
    1: 5,
    2: 5,
    3: 5,
    4: 5,
    5: 5,
    6: 5,
    7: 5,
    8: 5,
    9: 6,
    10: 4,
    12: 6,
    13: 4,
    14: 3,
    15: 3,
    16: 3,
    17: 3,
    18: 3,
    19: 3,
    20: 3,
    21: 3,
    22: 3,
    23: 3,
    24: 3,
    26: 3,
    27: 3,
    30: 3,
    31: 3,
    32: 3,
    33: 3,
    34: 3,
    35: 3,
    36: 3,
    37: 3,
    38: 3,
    39: 3,
    40: 3,
    41: 3,
    42: 3,
    43: 3,
    45: 3,
    46: 3,
    47: 3,
    48: 3,
    49: 3,
    50: 3,
    51: 3,
    52: 3,
    53: 3,
    54: 3,
    55: 3,
    56: 3,
    57: 3,
    58: 3,
    59: 3,
    60: 3,
    61: 3,
    62: 3,
    63: 3,
    64: 3,
    66: 3,
    69: 3,
    71: 3,
    72: 3,
    73: 3,
    74: 3,
    75: 3,
    76: 3,
    77: 3,
    78: 3,
    79: 3,
    80: 3,
    81: 3,
    83: 3,
    84: 3,
    85: 3,
    86: 3,
    87: 3,
    88: 3,
    89: 3
}

POWER_TO_SPEED = {
    20: 35.5,
    30: 39.5,
    40: 44.1,
    50: 47.7,
    60: 52.5,
    70: 55.4,
    80: 59.5,
    90: 62.9 
}

POWER_TO_TURN_TIME = {
    20: 3.25
}

POWER_RIGHT_TURN_TIME = {
10: 3.95
}

POWER_LEFT_TURN_TIME = {
10: 3.8
}

DRIVE_POWER = 20

TURN_POWER = 10