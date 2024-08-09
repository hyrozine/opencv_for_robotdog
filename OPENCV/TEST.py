import cv2
import numpy as np
from utils import COLOR_THRESHOLD, img_size
import color_detect
import ball_detect
from line_detect import line_track

video = cv2.VideoCapture(0, cv2.CAP_V4L2)
video.set(cv2.CAP_PROP_FRAME_WIDTH, img_size[0])
video.set(cv2.CAP_PROP_FRAME_HEIGHT, img_size[1])

while video.isOpened():
        ret,frame = video.read()
        video.set(6, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        if frame is None:
            break
        if ret == True:
            # _, result = ball_detect.detect_ball(frame, 'BROWN')
            # _, result = ball_detect.detect_ball(frame, 'PURPLE')
            # _ = color_detect.detect_red_divpath(frame)
            # _ = color_detect.detect_user(frame, 1)    # brown user
            # _ = color_detect.detect_user(frame, 2)    # purple user
            # _ = color_detect.detect_orange_end(frame)
            track_flag = line_track(frame)
            cv2.imshow('video',frame)
            key = cv2.waitKey(1)
            if(key & 0xFF == ord('q')) :
                break

video.release()
cv2.destroyAllWindows()
