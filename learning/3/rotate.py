import cv2
import numpy as np

img = cv2.imread('/home/hyrozine/pic1.jpg')

r_90_n = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)

r_90_p = cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE)

r_180 = cv2.rotate(img,cv2.ROTATE_180)

cv2.imshow('img',img)
cv2.imshow('r_90_n',r_90_n)
cv2.imshow('r_90_p',r_90_p)
cv2.imshow('r_180',r_180)

cv2.waitKey(0)