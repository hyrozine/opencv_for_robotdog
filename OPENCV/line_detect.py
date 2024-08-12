import cv2
import numpy as np
import math
#from uart import my_uart
from utils import STRAIGHT, LEFT, RIGHT, limit_angle, img_size, offset_turn_right, offset_turn_left
def calculate_slope(line):
    x1, y1, x2, y2 = line[0]
    if x1 - x2 == 0:
        return 0
    else:
        return (y1 - y2) / (x1 - x2)

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
    # distinguish the lines depends on slope first
    positive_slope = [line for line in lines if calculate_slope(line) > 0]
    negative_slope = [line for line in lines if calculate_slope(line) < 0]
    # if lose line or close to curve and the lines slope are all negative or positive
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
        for line in right_lines:
            x1, y1, x2, y2 = line[0]
            if x1 <= img_size[0] / 2 or x2 <= img_size[0] / 2:
                left_lines.append(line)
                right_lines.remove(line)
    elif negative_slope == []:
        for line in positive_slope:
            x1, y1, x2, y2 = line[0]
            mean_x = (x1 + x2) / 2
            if mean_x < img_size[0]:
                left_lines.append(line)
            else:
                right_lines.append(line)
        for line in left_lines:
            x1, y1, x2, y2 = line[0]
            if x1 > img_size[0] / 2 or x2 > img_size[0] / 2:
                right_lines.append(line)
                left_lines.remove(line)
    return left_lines, right_lines


def least_squares_fit(lines):
    x_coords = np.ravel([[line[0][0], line[0][2]] for line in lines])
    y_coords = np.ravel([[line[0][1], line[0][3]] for line in lines])
    poly = np.polyfit(x_coords, y_coords, deg=1)
    point_min = (np.min(x_coords), np.polyval(poly, np.min(x_coords)))
    point_max = (np.max(x_coords), np.polyval(poly, np.max(x_coords)))
    return np.array([point_min, point_max], dtype=np.int32)


def judge(left_lower, left_upper, right_lower, right_upper):
    lane_flag = 0
    if calculate_slope(left_lower, left_upper) >= 0 and calculate_slope(right_lower, right_upper) <= 0:
        lane_flag = 0
        return lane_flag
    if calculate_slope(left_lower, left_upper) >= 0 and calculate_slope(right_lower, right_upper) >= 0:
        lane_flag = 1
        return lane_flag
    if right_lower == [] or right_upper == []:
        lane_flag = 2
        return lane_flag
    if left_lower == [] or left_upper == []:
        lane_flag = 4
        return lane_flag

def straight_walk(left_lower, left_upper, right_lower, right_upper, lane_flag):
    if lane_flag == 1:
        mid_lower = (left_lower + right_lower) // 2
        mid_upper = (left_upper + right_upper) // 2
        # print(mid_lower, mid_upper)
        angle = calculate_angle(mid_upper, mid_lower)
        mid_x = (mid_upper[0] + mid_lower[0]) // 2

        draw_line(left_lower, left_upper, right_lower, right_upper)

        return angle, mid_x
    # close to the curve, walk straight till lose the line
    if lane_flag == 2:
        mid_lower = (left_lower + right_lower) // 2
        mid_upper = (left_upper + right_upper) // 2
        angle = 0
        mid_x = (mid_upper[0] + mid_lower[0]) // 2

        draw_line(left_lower, left_upper, right_lower, right_upper)

        return angle, mid_x

def curve_walk(lower, upper, lane_flag):
    mid_upper = []
    mid_lower = []
    mid_upper[1] = upper[1]
    mid_lower[1] = lower[1]

    # if lose the line, provide a line
    if lane_flag == 2:
        mid_upper[0] = (lower[0] + img_size[0]) / 2 + offset_turn_right
        mid_lower[0] = (upper[0] + img_size[0]) / 2 + offset_turn_right

        draw_line(lower, upper, [img_size[0], lower[1]], [img_size[0], upper[1]], mid_upper, mid_lower)

    if lane_flag == 4:
        mid_upper[0] = lower[0] / 2 - offset_turn_left 
        mid_lower[0] = upper[0] / 2 - offset_turn_left

        draw_line(lower, upper, [0, lower[1]], [0, upper[1]], mid_upper, mid_lower)

    angle = calculate_angle(lower, upper)
    mid_x = (mid_lower[0] +mid_upper[0]) // 2
    return angle, mid_x

def angle_deg_and_dir(angle, err = 20):
    direct = STRAIGHT
    angle_deg = 0
    if angle > 90:
        angle_deg = angle - 90
        if angle_deg < err:
            direct = STRAIGHT
        else:
            direct = LEFT  
    elif angle < 90:
        angle_deg = 90 - angle
        if angle_deg < err:
            direct = STRAIGHT
        else:
            direct = RIGHT 
    return direct, int(angle_deg)

def draw_lines(frame, left_upper, left_lower, right_upper, right_lower, mid_lower, mid_upper):
    cv2.line(frame, tuple(left_upper), tuple(left_lower), color=(0, 255,255), thickness = 5)
    cv2.line(frame, tuple(right_upper), tuple(right_lower), color=(0, 255,255), thickness = 5)
    cv2.line(frame, tuple(mid_lower), tuple(mid_upper), color=(0, 0,255), thickness = 5)

def mid_line_detect(frame, lane_flag):

    angle = 0
    mid_x = img_size[0] / 2
    left_lines_mod = []
    right_lines_mod = []
    left_line_ret = []
    right_line_ret = []

    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret,img_bin = cv2.threshold(img_gray, 110, 255, cv2.THRESH_BINARY) 
    # cv2.imshow('img_bin', img_bin)

    edge = cv2.Canny(img_bin, 0, 0)
    # cv2.imshow('edge', edge)

    mask = np.zeros_like(edge)
    # mask = cv2.fillPoly(mask, np.array([[[100,415], [300, 313], [1000, 305], [1500, 415]]]), color = 255)   # TODO: need to be specified
    #mask = cv2.fillPoly(mask, np.array([[[0,mask.shape[0] // 4 * 3], [0, mask.shape[0] // 2], [1280, mask.shape[0] // 2], [1280, mask.shape[0] // 4 * 3]]]), color = 255)   # TODO: need to be specified
    mask = cv2.fillPoly(mask, np.array([[[mask.shape[1] // 5, mask.shape[0] // 2], [mask.shape[1] // 5, mask.shape[0] // 4], [mask.shape[1] // 5 * 4, mask.shape[0] // 4], [mask.shape[1] // 5 * 4, mask.shape[0] // 2 ]]]), color = 255)   # TODO: need to be specified
    # cv2.imshow('mask', mask)

    # print(mask.shape[0] // 3)
    masked_edge = cv2.bitwise_and(edge, mask)
    # cv2.imshow('mask_edge', masked_edge)
    #print(masked_edge.shape)
     
    lines = cv2.HoughLinesP(masked_edge, 1, np.pi/180, 15, minLineLength = 40, maxLineGap = 20)
    # print(lines)
    
    # distinguish the left lines and the right lines
    if lines is not None:
        #print(lines)
        left_lines, right_lines = distinguish_line(lines)
        #print(left_lines, right_lines)
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
        return 0, img_size[0]/2, 2
    
    # use least squares fit to get two lines
    if left_lines_mod != []: 
        left_line_ret = least_squares_fit(left_lines_mod)
    if right_lines_mod != []:
        right_line_ret = least_squares_fit(right_lines_mod)
    if left_lines_mod == [] and right_lines_mod == []:
        return 0, img_size[0]/2, 2
    
    # distinguish the upper points and lower points
    if left_line_ret[0][1] >= left_line_ret[1][1]:
        left_upper = left_line_ret[0]
        left_lower = left_line_ret[1]
    else:
        left_upper = left_line_ret[1]
        left_lower = left_line_ret[0]
    if right_line_ret[0][1] >= right_line_ret[1][1]:
        right_upper = right_line_ret[0]
        right_lower = right_line_ret[1]
    else:
        right_upper = right_line_ret[1]
        right_lower = right_line_ret[0]
   
   # straight
    if lane_flag == 0: 
        lane_flag = judge(left_lower, left_upper, right_lower, right_upper)
        angle, mid_x = staight_walk(left_lower, left_upper, right_lower, right_upper, lane_flag)
        return angle, mid_x, lane_flag
    # close to curve
    elif lane_flag == 1:
        lane_flag = judge(left_lower, left_upper, right_lower, right_upper)
        angle, mid_x = straight_walk(left_lower, left_upper, right_lower, right_upper, lane_flag)
        return angle, mid_x, lane_flag
    # in the curve 
    elif lane_flag == 2:
        lane_flag = judge(left_lower, left_upper, right_lower, right_upper)
        angle, mid_x = curve_walk(left_lower, left_upper, right_lower, right_upper, lane_flag)
        return angle, mid_x, lane_flag
    # fork
    elif lane_flag == 3:
        lane_flag = judge(left_lower, left_upper, right_lower, right_upper)
        angle, mid_x = curve_walk(left_lower, left_upper, right_lower, right_upper, lane_flag)
        return angle, mid_x, lane_flag
    # lose left line
    elif lane_flag == 4:
        lane_flag = judge(left_lower, left_upper, right_lower, right_upper)
        angle, mid_x = curve_walk(left_lower, left_upper, right_lower, right_upper, lane_flag)
        return angle, mid_x, lane_flag

def line_track(frame, lane_flag, err=1, angle_limit=20):
    
    direct = STRAIGHT
    angle_deg = 0
    w = frame.shape[1]
    h = frame.shape[0]
    mid_x = w / 2
    angle, mid_x, lane_flag = mid_line_detect(frame, lane_flag)

    direct, angle_deg = angle_deg_and_dir(angle, err)
    # if type == 'grass':  
    #     angle_err = w / 2 - mid_x
    #     angle_deg = int(angle_deg + 1 * angle_err / 2)
    angle_deg = limit_angle(angle_deg, angle_limit)  
    #     if angle_deg > 1:
    #         if mid_x > w / 2:
    #             direct = RIGHT
    #         elif mid_x < w / 2:
    #             direct = LEFT
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

    #my_uart.set_data(direct, 'direction')
    #my_uart.set_data(angle_deg, 'angle')
    print('direct', direct)
    print('angle_deg', angle_deg)
    return lane_flag
