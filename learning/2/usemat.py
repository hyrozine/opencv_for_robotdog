import cv2
import numpy as np

img = cv2.imread('/home/hyrozine/test_pic.jpg')

# shallow copy: only copy the header of the struct
img2 = img

# deep copy : copy the total struct, including the data part
img3 = img.copy()

img[10:100,10:100] = [0,0,255]

cv2.imshow('img',img)
cv2.imshow('img2',img2)
cv2.imshow('img3',img3)

# shape: height, length and the number of channels
print(img.shape)

# calculate how much space the picture occupies
# size = height * length * channels
print(img.size)

# bit depth of every pixel
print(img.dtype)

cv2.waitKey(0)