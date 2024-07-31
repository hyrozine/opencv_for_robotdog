import cv2
from matplotlib.pyplot import flag
import numpy as np
from utils import COLOR_THRESHOLD
import color_detect
import ball_detect
from line_detect import line_track



# def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
#     print(x,y)
        

cv2.namedWindow('video',cv2.WINDOW_AUTOSIZE)
cv2.resizeWindow('video',640,480)

video = cv2.VideoCapture(0)

# cv2.setMouseCallback("videoo", on_EVENT_LBUTTONDOWN)

while video.isOpened():
        ret,frame = video.read()
        video.set(cv2.CAP_PROP_FRAME_WIDTH, img_size[0])
        video.set(cv2.CAP_PROP_FRAME_HEIGHT, img_size[1])
        video.set(cv2.CAP_PROP_FPS, 30)
        if frame is None:
            break
        if ret == True:
            # _, result = ball_detect.detect_ball(frame, 'BROWN')
            # _, result = ball_detect.detect_ball(frame, 'PURPLE')
            # _ = color_detect.detect_red_divpath(frame)
            # _ = color_detect.detect_user(frame, 1)    # brown user
            # _ = color_detect.detect_user(frame, 2)    # purple user
            # _ = color_detect.detect_orange_end(frame)
            # track_flag = line_track(frame)
            cv2.imshow('video',frame)
            key = cv2.waitKey(1)
            if(key & 0xFF == ord('q')) :
                break

video.release()
cv2.destroyAllWindows()
