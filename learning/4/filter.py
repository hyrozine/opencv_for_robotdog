import cv2
import numpy as np

img = cv2.imread('/home/hyrozine/test_pic.jpg')

kernal = np.ones((5,5),np.float32) / 25 

# filter2D(src,ddepth,kernel,anchor,delta,borderTiype)
# if not be defined   ddepth = src , anchor = the core of kernal, delta = 0
filter2D = cv2.filter2D(img, -1, kernal)  # ddepth = -1
# in this case, filter2D and blur have the same effect

# box filter
# boxFilter(src, ddepth, ksize, anchor, normalize, borderType)
# normalize == true -> a = 1/ w*h  The box filter degenerates to the average filter
# normalize == flase -> a = 1

# average filter
# blur(src, kernel, anchor, borderType)
blur = cv2.blur(img, (5, 5))

# gaussian filter   reduce guassion noise
# GaussianBlur(img, kernel, sigmaX, sigmaY, ...)
gaussian = cv2.GaussianBlur(img, (5, 5), sigmaX = 1)

# median filter     reduce pepper noise
# medianBlur(src, ksize)
median = cv2.medianBlur(img, 5) 

# bilateral filter
# bilateralFilter(src, ksize, sigmaColor, sigmaSpace, ...)
bilateral = cv2.bilateralFilter(img, 5, 20, 50)

# #high-pass filtering

# Sobel operator
# Sobel(src, ddepth, dx,dy, ksize = 3, scale = 1, delta = 0, borderType = BORDER_DEFUALT)
# if set ksize = -1, sobel change to scharr
# sobel operator can take the derivative of both x and y at the same time,
# but the result could not be good; recommend to take the derivative at twice.
sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize = 5)
sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize = 5)
sobel = cv2.add(sobel_x,sobel_y)

# scharr operator     define the ksize = 3
# Scharr(src, ddepth, dx, dy, scale = 1, delta = 0, borderType)
# sobel operator can not take the derivative of both x and y at the same time
Scharr_x = cv2.Scharr(img, cv2.CV_64F, 1, 0)

# it's better to filter before using the laplacian operator, because it's sensative to noise
# Laplacian(src, ddepth, ksize = 1, scale = 1, borderType)
laplacian = cv2.Laplacian(img, cv2.CV_64F, ksize = 5)

cv2.imshow('img',img)
cv2.imshow('dst1',filter2D)
cv2.imshow('blur',blur)
cv2.imshow('gaussian',gaussian)
cv2.imshow('median',median)
cv2.imshow('bilateral',bilateral)

cv2.imshow('sobel_x',sobel_x)
cv2.imshow('sobel_y',sobel_y)
cv2.imshow('sobel',sobel)
cv2.imshow('Scharr_x',Scharr_x)
cv2.imshow('laplacian',laplacian)


cv2.waitKey(0)