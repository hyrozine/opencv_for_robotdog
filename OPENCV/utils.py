img_size = (1280, 720)

COLOR_THRESHOLD = {
    'BLUE': [102, 179, 102, 204, 98, 212],  
    'BROWN': [100, 179, 0, 105, 0, 141],
    'PRUPLE': [103, 179, 109, 255, 60, 159], 
    'RED': [112, 179, 0,195, 81, 123],
    'ORANGE' : [6, 136, 171, 26, 255, 255]
}

COLOR = {
    'BLUE': 0,
    'BROWN': 1,
    'PRUPLE': 2,
    'RED': 3,
    'ORANGE': 4,
}

BALL_COLOR_THRESHOLD = {
    'RED': [112, 179, 0,195, 81, 123],  
    'BROWN': [100, 179, 0, 105, 0, 141],  
    'PRUPLE': [103, 179, 109, 255, 60, 159],  
}

STATE = {
    'state_1_init': 1,
    'state_1_out': 2,
    'state_2_obstacle': 3,
    'state_3_upstair': 4,
    'state_4_downstair': 5,
    'state_5_user1': 6,
    'state_5_user2': 7,
    'state_6_backhome': 8,
    'state_7_debug': 9
}

LEFT = 1
STRAIGHT = 0
RIGHT = 2


def limit_angle(value, max, min=0):
    if value > max:
        value = max
    if value < 0:
        value = min
    return value
