import cv2
import numpy as np
from utils import COLOR_THRESHOLD, img_size


def detect_ball(frame, threshold):
    roi = np.array([[[0, img_size[1]], [0, img_size[1] // 2], [img_size[0], img_size[1] // 2], [img_size[0], img_size[1]]]])

    hsv = COLOR_THRESHOLD[threshold]
    hsv_low =  np.array([hsv[0], hsv[1], hsv[2]])
    hsv_upper = np.array([hsv[3], hsv[4], hsv[5]])
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # print(hsv_low, hsv_upper)
    mask = cv2.inRange(imgHSV, hsv_low, hsv_upper)

    roi_mask = np.zeros_like(mask)
    roi_mask = cv2.fillPoly(roi_mask, roi, color = 255)
    mask = cv2.bitwise_and(mask, roi_mask)
    cv2.imshow('mask', mask)   

    cnts, hier = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if cnts == []:
        print("color isn't detected")
        return False
    
    min_area = 50
    filtered_contours = [cnt for cnt in cnts if cv2.contourArea(cnt) > min_area]
    # print(filtered_contours)
    
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
    # cv2.imshow('edges', edges)

    x,y,w,h = cv2.boundingRect(filtered_contours[0])
    cv2.rectangle(frame, (x, y), (w+x, h+y), (255, 0, 0), 2)

    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1.5, minDist=60, param1=50, param2=30, minRadius=15,
                               maxRadius=100)
    # print(circles)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            center = (circle[0], circle[1])
            radius = circle[2]
            cv2.circle(frame, center, radius, (0, 0, 255), 2)

        return True
    else:
        return False


    