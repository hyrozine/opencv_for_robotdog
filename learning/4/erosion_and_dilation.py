import cv2
import numpy as np

img = cv2.imread('/home/hyrozine/test_pic.jpg')

cv2.imshow('img',img)

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# threshold(src, thresh, maxVal, type)
# type : THRESH_BINARY THRESH_BINARY_INV THRESH_TRUNC THRESH_TOZERO THRESH_TOZERO_INV
ret,img_bin = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY)

# adaptiveThreshold(img, maxVal, adaptiveMethod, type, blockSize, C)
# method: ADAPTIVE_THRESH_MEAN_C  ADAPTIVE_THRESH_GAUSSIAN_C
# type: THRESH_BINARY THRESH_BINARY_INV
img_adap = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 0)

cv2.imshow('img_gray',img_gray)
cv2.imshow('img_bin',img_bin)
cv2.imshow('img_adap',img_adap)

kernel = np.ones((3,3),np.uint8)

# getStructuringElement(type, size)
# type: MORPH_RECT MORPH_ELLIPSE MORPH_CROSS
# the effect is the same as above 
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))

#erosion
erosion = cv2.erode(img,kernel,iterations=2)
cv2.imshow('erosion',erosion)

#dilation
dilation = cv2.dilate(img,kernel,iterations=2)
cv2.imshow('dilation',dilation)

#opening operation : first erosion then dilation
opening = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)
cv2.imshow('opening',opening)

#closing operation : first dilation then erosion
closing = cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel)
cv2.imshow('closing',closing)

#gradient : origin - erosion
gradient = cv2.morphologyEx(img,cv2.MORPH_GRADIENT,kernel)
cv2.imshow('gradient',gradient)

#tophat : origin - opening 
tophat = cv2.morphologyEx(img,cv2.MORPH_TOPHAT,kernel)
cv2.imshow('tophat',tophat)

#blackhat : closing - origin
blackhat = cv2.morphologyEx(img,cv2.MORPH_BLACKHAT,kernel)
cv2.imshow('blackhat',blackhat)


cv2.waitKey(0)
cv2.destroyAllWindows()