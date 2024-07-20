import cv2
import numpy as np

img = cv2.imread('/home/hyrozine/pic1.jpg')

# The operation of images are the same as for matrices, so the img shapes need to be the same
# print(img.shape)

img2 = np.ones((560,560,3),np.uint8) * 50

addition = cv2.add(img, img2)

subtraction = cv2.subtract(img,img2)

multiplication = cv2.multiply(img,img2)

division = cv2.divide(img,img2)

cv2.imshow('img',img)
cv2.imshow('addition',addition)
cv2.imshow('subtraction',subtraction)
cv2.imshow('multiplication',multiplication)
cv2.imshow('division',division)


cv2.waitKey(0)