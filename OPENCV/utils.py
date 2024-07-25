img_size = (640, 480)

COLOR_THRESHOLD = {
    'BLUE': [12, 40, -5, 14, -36, -14],  
    'PRUPLE': [0, 70, 12, 40, -80, -35], 
    'ORANGE' : [6, 136, 171, 26, 255, 255],
    'RED': [38, 70, 54, 76, 16, 57],  
    'BROWN': [11, 70, 11, 55, 4, 33]  
}

COLOR = {
    'BLUE': 0,
    'BROWN': 1,
    'PRUPLE': 2,
    'RED': 3,
    'ORANGE': 4,
}

BALL_COLOR_THRESHOLD = {
    'RED': [27, 50, 33,66 , 9, 50],  
    'BROWN': [40,80 , 0, 37, 35, 56],  
    'PRUPLE': [5, 90, 8, 36, -70, -20],  
}

STATE = {
    'state_1_recognize_ball': 1,
    'state_2_blue_climb': 2,
    'state_3_red_turn': 3,
    'state_4_user': 4,
    'state_5_orage_end': 5,
    'state_debug': 6
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
