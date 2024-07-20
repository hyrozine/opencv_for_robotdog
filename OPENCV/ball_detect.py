import cv2
import numpy as np
from utils import COLOR_THRESHOLD

def detect_ball(frame, threshold):
    hsv = COLOR_THRESHOLD[threshold]
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

    mask = filtered_mask

    kernel = np.ones((3, 3), np.uint8)
    dilation = cv2.dilate(mask, kernel, iterations=3)
    erode = cv2.erode(dilation, kernel, iterations=1)

    edges = cv2.Canny(erode, 0, 0)
    cv2.imshow('edges', edges)

    

    cv2.imshow('frame', frame)

    key = cv2.waitKey(0)
    cv2.destroyAllWindows()