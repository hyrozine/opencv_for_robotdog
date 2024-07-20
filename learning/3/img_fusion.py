import cv2
import numpy as np

# two imgs property need to be the same.

img1 = cv2.imread('/home/hyrozine/test_pic.jpg',)
img2 = cv2.imread('/home/hyrozine/test_pic.jpg')

subtraction = cv2.subtract(img1,img2)

# alpha * x1 + beta * x2 + b 
res = cv2.addWeighted(img1,0.4,subtraction,0.6,0)

cv2.imshow('img1_subtraction',res)
cv2.waitKey(0)