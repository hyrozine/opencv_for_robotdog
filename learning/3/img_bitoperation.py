import cv2
import numpy as np


img = np.zeros((200,200),np.uint8)
img2 = np.zeros((200,200),np.uint8)

img[20:120,20:120] = 128
img2[80:180,80:180] = 128   # bitwise : value > 128 -> 1, value < 128 -> 0

not_img = cv2.bitwise_not(img)
and_img = cv2.bitwise_and(img, img2)
or_img = cv2.bitwise_or(img,img2)
xor_img = cv2.bitwise_xor(img,img2)

cv2.imshow('img',img) 
cv2.imshow('img2',img2)
cv2.imshow('not_img',not_img)
cv2.imshow('and_img',and_img)
cv2.imshow('or_img',or_img)
cv2.imshow('xor_img',xor_img)

cv2.waitKey(0)
