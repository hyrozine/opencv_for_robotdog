import cv2
import numpy as np

# 1. 5*5 kernal gaussian fiter
# 2. sobel to calculate the direction of the image gradient
# 3. take local maximum
# 4. threshold calculation

img = cv2.imread('/home/hyrozine/test_pic.jpg')

# Canny(img, minVal, maxVal, ...)
canny = cv2.Canny(img, 50, 200)

cv2.imshow('img',img)
cv2.imshow('canny',canny)
cv2.waitKey(0)
