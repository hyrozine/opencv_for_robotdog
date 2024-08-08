import cv2
import numpy as np
from utils import img_size

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

video = cv2.VideoCapture(0)

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)

cv2.createTrackbar('HUE MIN',"TrackBars", 0, 179, trackbarcb)
cv2.createTrackbar('HUE MAX',"TrackBars", 179, 179, trackbarcb)
cv2.createTrackbar('SAT MIN',"TrackBars", 0, 255, trackbarcb)
cv2.createTrackbar('SAT MAX',"TrackBars", 255, 255, trackbarcb)
cv2.createTrackbar('VAL MIN',"TrackBars", 0, 255, trackbarcb)
cv2.createTrackbar('VAL MAX',"TrackBars", 255, 255, trackbarcb)

cv2.namedWindow('video', cv2.WINDOW_AUTOSIZE)
cv2.resizeWindow('video', img_size[0], img_size[1])

while True:
    ret, frame = video.read()
    # video.set(cv2.CAP_PROP_FRAME_WIDTH, img_size[0])
    # video.set(cv2.CAP_PROP_FRAME_HEIGHT, img_size[1])
    # video.set(cv2.CAP_PROP_FPS, 30)
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hue_min = cv2.getTrackbarPos("HUE MIN","TrackBars")
    hue_max = cv2.getTrackbarPos("HUE MAX","TrackBars")
    sat_min = cv2.getTrackbarPos('SAT MIN',"TrackBars")
    sat_max = cv2.getTrackbarPos('SAT MAX',"TrackBars")
    val_min = cv2.getTrackbarPos("VAL MIN","TrackBars")
    val_max = cv2.getTrackbarPos("VAL MAX","TrackBars")

    lower = np.array([hue_min, sat_min,val_min])
    upper = np.array([hue_max, sat_max,val_max])

    mask = cv2.inRange(imgHSV, lower, upper)

    imgResult = cv2.bitwise_and(frame, frame, mask = mask)

    imgStack = stackImages(0.9, [[frame,imgHSV],[mask,imgResult]])
    cv2.imshow('video',imgStack)

    key = cv2.waitKey(1)
    if(key & 0xFF == ord('q')) :
        break

video.release()
cv2.destroyAllWindows()


