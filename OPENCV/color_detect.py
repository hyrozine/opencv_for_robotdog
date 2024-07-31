from operator import truediv
import cv2
import numpy as np
from utils import COLOR_THRESHOLD, img_size


def detect_blue_upstair(frame):
    roi = np.array([[[0, img_size[1]], [0, img_size[1] // 2], [img_size[0], img_size[1] // 2], [img_size[0], img_size[1]]]])

    hsv = COLOR_THRESHOLD['BLUE']
    hsv_low =  np.array([hsv[0], hsv[1], hsv[2]])
    hsv_upper = np.array([hsv[3], hsv[4], hsv[5]])
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # print(hsv_low, hsv_upper)
    mask = cv2.inRange(imgHSV, hsv_low, hsv_upper)
    
    roi_mask = np.zeros_like(mask)
    roi_mask = cv2.fillPoly(roi_mask, roi, color = 255)
    mask = cv2.bitwise_and(mask, roi_mask)
    # cv2.imshow('mask', mask)   

    cnts, hier = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if cnts == []:
        print("color isn't detected")
        return False
    
    min_area = 50    # TODO: need to be specified
    filtered_contours = [cnt for cnt in cnts if cv2.contourArea(cnt) > min_area]
    # print(filtered_contours)
    
    if filtered_contours == []:
        print("rect isn't big enough")
        return False
    
    filtered_mask = np.zeros_like(mask)
    cv2.drawContours(filtered_mask, filtered_contours, -1, 255, cv2.FILLED)
    # cv2.imshow('filtered_mask', filtered_mask)

    x,y,w,h = cv2.boundingRect(filtered_contours[0])

    ratio = round(w/h, 2)
    ratio_min = 1  # TODO: need to be specify
    ratio_max = 10  # TODO: need to be specify
    print(ratio)

    if not(ratio <= ratio_max and ratio_min <= ratio):
        print("rect isn't valid")
        return False

    cv2.rectangle(frame, (x, y), (w+x, h+y), (255, 0, 0), 2)

    return True

def detect_red_divpath(frame):
    roi = np.array([[[0, img_size[1]], [0, img_size[1] // 2], [img_size[0], img_size[1] // 2], [img_size[0], img_size[1]]]])

    hsv = COLOR_THRESHOLD['RED']
    hsv_low =  np.array([hsv[0], hsv[1], hsv[2]])
    hsv_upper = np.array([hsv[3], hsv[4], hsv[5]])
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # print(hsv_low, hsv_upper)
    mask = cv2.inRange(imgHSV, hsv_low, hsv_upper)

    roi_mask = np.zeros_like(mask)
    roi_mask = cv2.fillPoly(roi_mask, roi, color = 255)
    mask = cv2.bitwise_and(mask, roi_mask)
    # cv2.imshow('mask', mask)

    cnts, hier = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if cnts == []:
        print("color isn't detected")
        return False
    
    min_area = 50     # TODO: need to be specify
    filtered_contours = [cnt for cnt in cnts if cv2.contourArea(cnt) > min_area]
    # print(filtered_contours)
    
    if filtered_contours == []:
        print("rect isn't big enough")
        return False
    
    filtered_mask = np.zeros_like(mask)
    cv2.drawContours(filtered_mask, filtered_contours, -1, 255, cv2.FILLED)
    # cv2.imshow('filtered_mask', filtered_mask)

    x,y,w,h = cv2.boundingRect(filtered_contours[0])

    ratio = round(w/h, 2)
    ratio_min = 1  # TODO: need to be specify
    ratio_max = 10  # TODO: need to be specify
    print(ratio)
    if not(ratio <= ratio_max and ratio_min <= ratio):
        print("rect isn't valid")
        return False

    cv2.rectangle(frame, (x, y), (w+x, h+y), (255, 0, 0), 2)
   
    return True

def detect_user(frame, id: int):
    roi = np.array([[[0, img_size[1]], [0, img_size[1] // 2], [img_size[0], img_size[1] // 2], [img_size[0], img_size[1]]]])

    ID_dict = {'1': 'BROWN', '2': 'PRUPLE'}
    hsv = COLOR_THRESHOLD[ID_dict[str(id)]]
    hsv_low =  np.array([hsv[0], hsv[1], hsv[2]])
    hsv_upper = np.array([hsv[3], hsv[4], hsv[5]])
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # print(hsv_low, hsv_upper)
    mask = cv2.inRange(imgHSV, hsv_low, hsv_upper)

    roi_mask = np.zeros_like(mask)
    roi_mask = cv2.fillPoly(roi_mask, roi, color = 255)
    mask = cv2.bitwise_and(mask, roi_mask)
    # cv2.imshow('mask', mask)

    cnts, hier = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if cnts == []:
        print("color isn't detected")
        return False
    
    min_area = 50   # TODO: need to be specify
    filtered_contours = [cnt for cnt in cnts if cv2.contourArea(cnt) > min_area]
    # print(filtered_contours)
    
    if filtered_contours == []:
        print("rect isn't big enough")
        return False
    
    filtered_mask = np.zeros_like(mask)
    cv2.drawContours(filtered_mask, filtered_contours, -1, 255, cv2.FILLED)
    # cv2.imshow('filtered_mask', filtered_mask)

    x,y,w,h = cv2.boundingRect(filtered_contours[0])

    ratio = round(w/h, 2)
    ratio_min = 1  # TODO: need to be specify
    ratio_max = 10  # TODO: need to be specify
    print(ratio)
    if not(ratio <= ratio_max and ratio_min <= ratio):
        print("rect isn't valid")
        return False

    cv2.rectangle(frame, (x, y), (w+x, h+y), (255, 0, 0), 2)

    return True

def detect_orange_end(frame):
    roi = np.array([[[0, img_size[1]], [0, img_size[1] // 2], [img_size[0], img_size[1] // 2], [img_size[0], img_size[1]]]])

    hsv = COLOR_THRESHOLD['ORANGE']
    hsv_low =  np.array([hsv[0], hsv[1], hsv[2]])
    hsv_upper = np.array([hsv[3], hsv[4], hsv[5]])
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # print(hsv_low, hsv_upper)
    mask = cv2.inRange(imgHSV, hsv_low, hsv_upper)

    roi_mask = np.zeros_like(mask)
    roi_mask = cv2.fillPoly(roi_mask, roi, color = 255)
    mask = cv2.bitwise_and(mask, roi_mask)
    # cv2.imshow('mask', mask)

    cnts, hier = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if cnts == []:
        print("color isn't detected")
        return False
    
    min_area = 50   # TODO: need to be specify
    filtered_contours = [cnt for cnt in cnts if cv2.contourArea(cnt) > min_area]
    # print(filtered_contours)
    
    if filtered_contours == []:
        print("rect isn't big enough")
        return False
    
    filtered_mask = np.zeros_like(mask)
    cv2.drawContours(filtered_mask, filtered_contours, -1, 255, cv2.FILLED)
    # cv2.imshow('filtered_mask', filtered_mask)

    x,y,w,h = cv2.boundingRect(filtered_contours[0])

    ratio = round(w/h, 2)
    ratio_min = 1  # TODO: need to be specify
    ratio_max = 10  # TODO: need to be specify
    print(ratio)
    if not(ratio <= ratio_max and ratio_min <= ratio):
        print("rect isn't valid")
        return False

    cv2.rectangle(frame, (x, y), (w+x, h+y), (255, 0, 0), 2)
    
    return True


