import cv2
import numpy as np
import line_detect

def ordinate_xy(event, x, y, flags, param):
    print(x,y)

pic = cv2.imread('/home/hyrozine/Camera_Roll/WIN_20240808_15_05_44_Pro.jpg')
cv2.setMouseCallback("pic", ordinate_xy)

# /home/hyrozine/图片
# ~/Camera_Roll/WIN_20240808_15_05_44_Pro.jpg

_, __ = line_detect.mid_line_detect(pic)
print(_ , __)

cv2.imshow('pic',pic)

cv2.waitKey(0)
