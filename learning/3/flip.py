import cv2 
import numpy as np
 
img = cv2.imread('/home/hyrozine/pic1.jpg')

up_down = cv2.flip(img, 0)

#                         >0
left_right = cv2.flip(img, 1)

#                       <0
u_d_l_r = cv2.flip(img, -1)

cv2.imshow('img',img)
cv2.imshow('up_down',up_down)
cv2.imshow('left_right',left_right)
cv2.imshow('u_d_l_r',u_d_l_r)

cv2.waitKey(0)