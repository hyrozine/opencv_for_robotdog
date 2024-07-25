import cv2
from matplotlib.pyplot import flag
import numpy as np
from utils import COLOR_THRESHOLD
import color_detect
import ball_detect
from line_detect import line_track

# # path = '/home/hyrozine/imgs/oranges.jpg'

# # img = cv2.imread(path)

# # _, frame = ball_detect.detect_ball(img, 'ORANGE')
# # cv2.imshow('frame', frame)        
# # key = cv2.waitKey(0)
# # cv2.destroyAllWindows()

# def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
#     # if event == cv2.EVENT_LBUTTONDOWN:
#         # xy = "%d,%d" % (x, y)
#         # cv2.circle(img, (x, y), 1, (255, 0, 0), thickness=-1)
#         # cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
#         # 1.0, (0, 0, 0), thickness=1)
#         print(x,y)
        

# path = '/home/hyrozine/imgs/orange.jpg'

# # cv2.namedWindow("image")
# # cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)

# img = cv2.imread(path)

# # line_track(img)
# color_detect.detect_blue_upstair(img)
# print(img.shape)
# cv2.imshow('img', img)        
# key = cv2.waitKey(0)
# cv2.destroyAllWindows()

video = cv2.VideoCapture(0)

while video.isOpened():
        ret,frame = video.read()
        if frame is None:
            break
        if ret == True:
            # _, result = ball_detect.detect_ball(frame, 'ORANGE')
            track_flag = line_track(frame)
            cv2.imshow('video',frame)
            key = cv2.waitKey(1)
            if(key & 0xFF == ord('q')) :
                break

video.release()
cv2.destroyAllWindows()
