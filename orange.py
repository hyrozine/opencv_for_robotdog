import cv2
import numpy as np

path = '/home/hyrozine/imgs/orange.jpg'
hsv_low = [6, 136, 171]
hsv_high = [26, 255, 255]
img = cv2.imread(path)

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def trackbarcb(void):
    pass

while True:
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array(hsv_low)
    upper = np.array(hsv_high)

    mask = cv2.inRange(imgHSV, lower, upper)

    imgResult = cv2.bitwise_and(img, img, mask = mask)

    min_area = 50
    cnts, hier = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = [cnt for cnt in cnts if cv2.contourArea(cnt) > min_area]
    filtered_mask = np.zeros_like(mask)
    cv2.drawContours(filtered_mask, filtered_contours, -1, 255, cv2.FILLED)
    
    mask = filtered_mask
    kernel = np.ones((3, 3), np.uint8)
    dilation = cv2.dilate(mask, kernel, iterations=3)
    erode = cv2.erode(dilation, kernel, iterations=1)

    edges = cv2.Canny(erode, 0, 0, apertureSize=3)
    cv2.imshow('mask', edges)



    # cv2.imshow('img',img)
    # cv2.imshow('imgHSV',imgHSV)
    # cv2.imshow('mask',mask)
    # cv2.imshow('filtered_mask',filtered_mask)
    imgStack = stackImages(0.9, [[img,imgHSV],[mask,imgResult]])
    cv2.imshow('imgStack',imgStack)
    key = cv2.waitKey(1)
    if(key & 0xFF == ord('q')) :
        break

cv2.destroyAllWindows()


