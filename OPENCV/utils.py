COLOR_THRESHOLD = {
    'BLACK': [20, 59, -19, 8, -14, 14],  # version 1
    'BLUE': [(12, 40, -5, 14, -36, -14)],  # version 3
    'RED': [(38, 70, 54, 76, 16, 57)],  # version 2
    'YELLOW': [(50, 100, -61, 17, 12, 83)],  # version 3
    'BROWN': [(11, 70, 11, 55, 4, 33)],  # version 2
    'GREEN': [(15, 50, -67, -18, 13, 50)],  # version 2

    # (15, 100, -67, -8, -18, 50)
    # (0, 45, -38, -19, 0, 56)
    # (20, 100, -57, 23, -15, 53)
    'PRUPLE': [(0, 70, 12, 40, -80, -35)],  # version 1

    'ORANGE' : [6, 136, 171, 26, 255, 255]
}

COLOR = {
    'BLACK': 0,
    'BLUE': 1,
    'RED': 2,
    'YELLOW': 3,
    'BROWN': 4,
    'GREEN': 5,
    'PRUPLE': 6,
    'BUCKET': 7,
}

BALL_COLOR_THRESHOLD = {
    'RED': [(27, 50, 33,66 , 9, 50)],  # version2
    'BROWN': [40,80 , 0, 37, 35, 56],  # version3
    'PRUPLE': [5, 90, 8, 36, -70, -20],  # verion2
}

STATE = {
    'state_1_begin': 1,
    'state_recognize_ball': 2,
    'state_2_user1': 3,
    'state_3_yellow_climb': 4,
    'state_4_black_obstacle': 5,
    'state_5_user2': 6,
    'state_6_grass': 7,
    'state_7_user3': 8,
    'state_debug': 9
}

LEFT = 1
STRAIGHT = 0
RIGHT = 2


def limit_angle(value, max, min=0):
    if value > max:
        value = max
    if value < 0:
        value = 0
    return value
