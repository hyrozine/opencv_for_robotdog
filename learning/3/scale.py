import cv2
import numpy as np

img = cv2.imread('/home/hyrozine/pic1.jpg')
#                     dsize(x,y)
#new = cv2.resize(img,(400,400))
new = cv2.resize(img, None, fx = 1.5, fy = 1.5, interpolation = cv2.INTER_AREA)

print(img.shape)

cv2.imshow('img',img)
cv2.imshow('new',new)

cv2.waitKey(0)