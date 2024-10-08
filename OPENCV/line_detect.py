import cv2
import numpy as np
import math
from uart import my_uart
from utils import STRAIGHT, LEFT, RIGHT, limit_angle, img_size, offset_turn_right, offset_turn_left
def calculate_slope(line):
    x1, y1, x2, y2 = line[0]
    if x1 - x2 == 0:
        return 0
    else:
        return (y1 - y2) / (x1 - x2)

def calculate_slope_point(pt1, pt2):
    dx = pt1[0] - pt1[0]
    dy = pt2[1] - pt2[1]
    if dx == 0:
        return 0
    else:
        return dy / dx

def calculate_angle(pt1, pt2):
    dx = pt1[0] - pt2[0]
    dy = pt1[1] - pt2[1]
    if dx == 0 or dy == 0:
        return 90
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    return angle_deg

def rm_abnormal_lines(lines, threshold = 0.2):
    slopes = [calculate_slope(line) for line in lines]
    while len(lines) > 0:
        mean = np.mean(slopes)
        diff = [abs(k - mean) for k in slopes]
        idx = np.argmax(diff)
        if diff[idx] > threshold:
           slopes.pop(idx)
           lines.pop(idx)
        else:
            break
    return lines 

def distinguish_line(lines):
    left_lines = []
    right_lines = []
    positive_slope = []
    negative_slope = []
    # distinguish the lines depends on slope first
    positive_slope = [line for line in lines if calculate_slope(line) > 0]
    negative_slope = [line for line in lines if calculate_slope(line) < 0]
    #print('positive_slope', positive_slope)
    #print('negative_slope', negative_slope)
    '''
    # if lose line 
    if positive_slope == []:
        # distinguish by image width
        for line in negative_slope:
            x1, y1, x2, y2 = line[0]
            mean_x = (x1 + x2) / 2
            if mean_x <= img_size[0]:
                left_lines.append(line)
            else:
                right_lines.append(line)
        # while mean_x > img_size[0], it's still possible on the left because of deviation
        for i, line in enumerate(right_lines):
            x1, y1, x2, y2 = line[0]
            if x1 <= img_size[0] / 2 or x2 <= img_size[0] / 2:
                left_lines.append(line)
                right_lines.pop(i)
    elif negative_slope == []:
        
        for line in positive_slope:
            x1, y1, x2, y2 = line[0]
            mean_x = (x1 + x2) / 2
            if mean_x < img_size[0]:
                left_lines.append(line)
            else:
                right_lines.append(line)
        for i, line in enumerate(left_lines):
            x1, y1, x2, y2 = line[0]
            if x1 > img_size[0] / 2 or x2 > img_size[0] / 2:
                right_lines.append(line)
                left_lines.pop(i)
        
        return [], positive_slope
    elif positive_slope != [] and negative_slope != []:
        return negative_slope, positive_slope 
    '''
    #print(left_lines, right_lines)
    return negative_slope, positive_slope


def least_squares_fit(lines):
    x_coords = np.ravel([[line[0][0], line[0][2]] for line in lines])
    y_coords = np.ravel([[line[0][1], line[0][3]] for line in lines])
    poly = np.polyfit(x_coords, y_coords, deg=1)
    point_min = (np.min(x_coords), np.polyval(poly, np.min(x_coords)))
    point_max = (np.max(x_coords), np.polyval(poly, np.max(x_coords)))
    return np.array([point_min, point_max], dtype=np.int32)


def judge(left_lower, left_upper, right_lower, right_upper):
    lane_flag = 0
    if right_lower == [] or right_upper == []:
        lane_flag = 1
    if left_lower == [] or left_upper == []:
        lane_flag = 2
    if left_lower != [] and left_upper != [] and right_lower != [] and right_upper != []:
        lane_flag = 0
    return lane_flag

def straight_walk(left_lower, left_upper, right_lower, right_upper, frame):
    mid_lower = (left_lower + right_lower) // 2
    mid_upper = (left_upper + right_upper) // 2
    #print(mid_lower, mid_upper)
    angle = calculate_angle(mid_upper, mid_lower)
    mid_x = (mid_upper[0] + mid_lower[0]) // 2

    draw_lines(frame, left_lower, left_upper, right_lower, right_upper, mid_lower, mid_upper)

    return angle, mid_x

def lose_line_walk(lower, upper, lane_flag, frame):
    mid_upper = lower
    mid_lower = upper

    # if lose the line, provide a line
    if lane_flag == 1:
        mid_upper[0] = (lower[0] + img_size[0]) // 2 + offset_turn_right
        mid_lower[0] = (upper[0] + img_size[0]) // 2 + offset_turn_right

        draw_lines(frame, lower, upper, [img_size[0], lower[1]], [img_size[0], upper[1]], mid_upper, mid_lower)

    if lane_flag == 2:
        mid_upper[0] = lower[0] // 2 - offset_turn_left 
        mid_lower[0] = upper[0] // 2 - offset_turn_left

        draw_lines(frame, lower, upper, [0, lower[1]], [0, upper[1]], mid_upper, mid_lower)

    angle = calculate_angle(mid_lower, mid_upper)
    mid_x = (mid_lower[0] + mid_upper[0]) // 2
    return angle, mid_x

def fork_walk(left_lower, left_upper, right_lower, right_upper, lane_flag, frame):
    pass

def angle_and_direction(angle, err = 10):
    direct = STRAIGHT
    angle_ret = 0
    if angle > 90:
        angle_ret = angle - 90
        print('angle>90')
        if angle_ret < err:
            direct = STRAIGHT
        else:
            direct = LEFT
    elif angle < 90:
        angle_ret = 90 - angle
        if angle_ret < err:
            direct = STRAIGHT
        else:
            direct = RIGHT
    return direct, int (angle_ret)

def draw_lines(frame, left_upper, left_lower, right_upper, right_lower, mid_lower, mid_upper):
    cv2.line(frame, tuple(left_upper), tuple(left_lower), color=(0, 255,255), thickness = 5)
    cv2.line(frame, tuple(right_upper), tuple(right_lower), color=(0, 255,255), thickness = 5)
    cv2.line(frame, tuple(mid_lower), tuple(mid_upper), color=(0, 0,255), thickness = 5)

def mid_line_detect(frame):
    angle = 0
    mid_x = img_size[0] / 2
    left_lines_mod = []
    right_lines_mod = []
    left_line_ret = []
    right_line_ret = []
    left_lower = []
    left_upper = []
    right_lower = []
    right_upper = []

    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret,img_bin = cv2.threshold(img_gray, 110, 255, cv2.THRESH_BINARY) 
    # cv2.imshow('img_bin', img_bin)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    erode = cv2.erode(img_bin, kernel)
    dilate = cv2.dilate(erode, kernel, iterations = 2)

    edge = cv2.Canny(dilate, 0, 0)
    # cv2.imshow('edge', edge)

    mask = np.zeros_like(edge)
    # mask = cv2.fillPoly(mask, np.array([[[100,415], [300, 313], [1000, 305], [1500, 415]]]), color = 255)   # TODO: need to be specified
    #mask = cv2.fillPoly(mask, np.array([[[0,mask.shape[0] // 4 * 3], [0, mask.shape[0] // 2], [1280, mask.shape[0] // 2], [1280, mask.shape[0] // 4 * 3]]]), color = 255)   # TODO: need to be specified
    mask = cv2.fillPoly(mask, np.array([[[0, mask.shape[0] // 2], [0, mask.shape[0] // 3 - 50], [1280, mask.shape[0] // 2 - 50], [1280, mask.shape[0] // 3 ]]]), color = 255)   # TODO: need to be specified
    #cv2.imshow('mask', mask)

    # print(mask.shape[0] // 3)
    masked_edge = cv2.bitwise_and(edge, mask)
    #cv2.imshow('mask_edge', masked_edge)
    #print(masked_edge.shape)
     
     
    lines = cv2.HoughLinesP(masked_edge, 1, np.pi/180, 15, minLineLength = 20, maxLineGap = 100)
    # print(lines)
    
    # distinguish the left lines and the right lines
    if lines is not None:
        #print(lines)
        left_lines, right_lines = distinguish_line(lines)
        #print('left_lines', left_lines)
        #print('right_lines', right_lines)
    else:
        return 0, img_size[0]/2, 0
    
    # remove abnormals lines, which are apparently invalid
    if left_lines != []: 
        left_lines_mod = rm_abnormal_lines(left_lines)
    if right_lines != []:
        right_lines_mod = rm_abnormal_lines(right_lines)
        # print(len(left_lines_mod) + len(right_lines_mod))
        # print(left_lines_mod + right_lines_mod)
    if left_lines == [] and right_lines == []:
        return 0, img_size[0]/2, 0
    
    # use least squares fit to get two lines
    if left_lines_mod != []: 
        left_line_ret = least_squares_fit(left_lines_mod)
        #print(left_line_ret)
    if right_lines_mod != []:
        right_line_ret = least_squares_fit(right_lines_mod)
        #print(right_line_ret)
    if left_lines_mod == [] and right_lines_mod == []:
        return 0, img_size[0]/2, 0
    
    # distinguish the upper points and lower points
    if left_line_ret != []:
        if left_line_ret[0][1] >= left_line_ret[1][1]:
            left_upper = left_line_ret[0]
            left_lower = left_line_ret[1]
        else:
            left_upper = left_line_ret[1]
            left_lower = left_line_ret[0]
        #print('left_upper', left_upper)
        #print('left_lower', left_lower)
    if right_line_ret != []:
        if right_line_ret[0][1] >= right_line_ret[1][1]:
            right_upper = right_line_ret[0]
            right_lower = right_line_ret[1]
        else:
            right_upper = right_line_ret[1]
            right_lower = right_line_ret[0]
        #print('right_upper', right_upper)
        #print('right_lower', right_lower)
   
    lane_flag = judge(left_lower, left_upper, right_lower, right_upper)
    print(lane_flag)
    # straight
    if lane_flag == 0: 
        angle, mid_x = straight_walk(left_lower, left_upper, right_lower, right_upper, frame)
        return angle, mid_x, lane_flag
    # lose right lines 
    elif lane_flag == 1:
        angle, mid_x = lose_line_walk(left_lower, left_upper, lane_flag, frame)
        return angle, mid_x, lane_flag
    # lose left lines
    elif lane_flag == 2:
        angle, mid_x = lose_line_walk(right_lower, right_upper, lane_flag, frame)
        return angle, mid_x, lane_flag

def line_track(frame, err= 10, angle_limit = 10):
    
    direct = STRAIGHT
    angle = 0
    w = img_size[0] 
    h = img_size[1]
    mid_x = w / 2
    angle, mid_x, lane_flag = mid_line_detect(frame)
    direct, angle = angle_and_direction(angle, err)
    #angle = int(angle + 1 * angle_err / 2)
    #angle_err = img_size[0] / 2 - mid_x
    #angle = angle + angle_err / 2
    angle = limit_angle(angle , angle_limit)  
    #if angle > 1:
    #    if mid_x > w / 2:
    #          direct = RIGHT
    #    elif mid_x < w / 2:
    #          direct = LEFT
            #else:
                #direct = STRAIGHT

    # elif type == 'turn':  
    #     if mid_x / 2 < (w/2 - offset_turn):  
    #         direct = LEFT
    #         angle_err = w/2 - mid_x
    #         angle_deg = int((angle_deg + angle_err / 2))
    #         limit_angle(angle_deg, angle_limit)
    #         direct = LEFT
    # else:
    #     angle_err = w/2 - offset_default - mid_x
    #     angle_deg = int(angle_deg + angle_err / 2)
    #     limit_angle(angle_deg, angle_limit)  # 角度限幅
    #     if angle_deg > 1:
    #         if mid_x / 2 > w/2 - offset_default:
    #             direct = RIGHT
    #         elif mid_x / 2 < w/2 - offset_default:
    #             direct = LEFT

    my_uart.set_data(direct, 'direction')
    my_uart.set_data(angle_deg, 'angle')
    print('direct', direct)
    print('angle', angle)
    return lane_flag
