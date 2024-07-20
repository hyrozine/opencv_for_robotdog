import cv2
import numpy as np
from utils import COLOR_THRESHOLD


def detect_blue_upstair(frame):
    hsv = COLOR_THRESHOLD['BLUE']
    hsv_low =  np.array([hsv[0], hsv[1], hsv[2]])
    hsv_upper = np.array([hsv[3], hsv[4], hsv[5]])
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # print(hsv_low, hsv_upper)
    mask = cv2.inRange(imgHSV, hsv_low, hsv_upper)

    cnts, hier = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if cnts == []:
        print("color isn't detected")
        return False
    
    min_area = 50
    filtered_contours = [cnt for cnt in cnts if cv2.contourArea(cnt) > min_area]
    print(filtered_contours)
    
    if filtered_contours == []:
        print("rect isn't big enough")
        return False
    
    filtered_mask = np.zeros_like(mask)
    cv2.drawContours(filtered_mask, filtered_contours, -1, 255, cv2.FILLED)
    # cv2.imshow('filtered_mask', filtered_mask)

    # mask = filtered_mask

    # kernel = np.ones((3, 3), np.uint8)
    # dilation = cv2.dilate(mask, kernel, iterations=3)
    # erode = cv2.erode(dilation, kernel, iterations=1)

    # edges = cv2.Canny(erode, 0, 0, apertureSize=3)
    # cv2.imshow('edges', edges)

    x,y,w,h = cv2.boundingRect(filtered_contours[0])

    ratio = round(w/h, 2)
    ratio_min = 1  # TODO: need to be specify
    ratio_max = 2  # TODO: need to be specify
    print(ratio)
    if not(ratio <= ratio_max and ratio_min <= ratio):
        print("rect isn't valid")
        return False

    cv2.rectangle(frame, (x, y), (w+x, h+y), (255, 0, 0), 2)
    cv2.imshow('frame', frame)

    key = cv2.waitKey(0)
    cv2.destroyAllWindows()

def detect_green_divpath(frame):
    hsv = COLOR_THRESHOLD['GREEN']
    hsv_low =  np.array([hsv[0], hsv[1], hsv[2]])
    hsv_upper = np.array([hsv[3], hsv[4], hsv[5]])
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # print(hsv_low, hsv_upper)
    mask = cv2.inRange(imgHSV, hsv_low, hsv_upper)

    cnts, hier = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if cnts == []:
        print("color isn't detected")
        return False
    
    min_area = 50
    filtered_contours = [cnt for cnt in cnts if cv2.contourArea(cnt) > min_area]
    print(filtered_contours)
    
    if filtered_contours == []:
        print("rect isn't big enough")
        return False
    
    filtered_mask = np.zeros_like(mask)
    cv2.drawContours(filtered_mask, filtered_contours, -1, 255, cv2.FILLED)
    # cv2.imshow('filtered_mask', filtered_mask)

    x,y,w,h = cv2.boundingRect(filtered_contours[0])

    ratio = round(w/h, 2)
    ratio_min = 1  # TODO: need to be specify
    ratio_max = 2  # TODO: need to be specify
    print(ratio)
    if not(ratio <= ratio_max and ratio_min <= ratio):
        print("rect isn't valid")
        return False

    cv2.rectangle(frame, (x, y), (w+x, h+y), (255, 0, 0), 2)
    cv2.imshow('frame', frame)

    key = cv2.waitKey(0)
    cv2.destroyAllWindows()

def detect_user(frame, id: int):

    ID_dict = {'1': 'BROWN', '2': 'PRUPLE'}
    hsv = COLOR_THRESHOLD[ID_dict[str(id)]]
    hsv_low =  np.array([hsv[0], hsv[1], hsv[2]])
    hsv_upper = np.array([hsv[3], hsv[4], hsv[5]])
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # print(hsv_low, hsv_upper)
    mask = cv2.inRange(imgHSV, hsv_low, hsv_upper)

    cnts, hier = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if cnts == []:
        print("color isn't detected")
        return False
    
    min_area = 50
    filtered_contours = [cnt for cnt in cnts if cv2.contourArea(cnt) > min_area]
    print(filtered_contours)
    
    if filtered_contours == []:
        print("rect isn't big enough")
        return False
    
    filtered_mask = np.zeros_like(mask)
    cv2.drawContours(filtered_mask, filtered_contours, -1, 255, cv2.FILLED)
    # cv2.imshow('filtered_mask', filtered_mask)

    x,y,w,h = cv2.boundingRect(filtered_contours[0])

    ratio = round(w/h, 2)
    ratio_min = 1  # TODO: need to be specify
    ratio_max = 2  # TODO: need to be specify
    print(ratio)
    if not(ratio <= ratio_max and ratio_min <= ratio):
        print("rect isn't valid")
        return False

    cv2.rectangle(frame, (x, y), (w+x, h+y), (255, 0, 0), 2)
    cv2.imshow('frame', frame)

    key = cv2.waitKey(0)
    cv2.destroyAllWindows()

def detect_orange_end(frame):
    hsv = COLOR_THRESHOLD['ORANGE']
    hsv_low =  np.array([hsv[0], hsv[1], hsv[2]])
    hsv_upper = np.array([hsv[3], hsv[4], hsv[5]])
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # print(hsv_low, hsv_upper)
    mask = cv2.inRange(imgHSV, hsv_low, hsv_upper)

    cnts, hier = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if cnts == []:
        print("color isn't detected")
        return False
    
    min_area = 50
    filtered_contours = [cnt for cnt in cnts if cv2.contourArea(cnt) > min_area]
    print(filtered_contours)
    
    if filtered_contours == []:
        print("rect isn't big enough")
        return False
    
    filtered_mask = np.zeros_like(mask)
    cv2.drawContours(filtered_mask, filtered_contours, -1, 255, cv2.FILLED)
    # cv2.imshow('filtered_mask', filtered_mask)

    x,y,w,h = cv2.boundingRect(filtered_contours[0])

    ratio = round(w/h, 2)
    ratio_min = 1  # TODO: need to be specify
    ratio_max = 2  # TODO: need to be specify
    print(ratio)
    if not(ratio <= ratio_max and ratio_min <= ratio):
        print("rect isn't valid")
        return False

    cv2.rectangle(frame, (x, y), (w+x, h+y), (255, 0, 0), 2)
    cv2.imshow('frame', frame)

    key = cv2.waitKey(0)
    cv2.destroyAllWindows()


