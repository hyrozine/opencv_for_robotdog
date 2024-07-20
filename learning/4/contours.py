import cv2
import numpy as np 

def drawShape(src, points,color):
    i = 0
    while i < len(points):
        if(i == len(points)-1):
            x, y = points[i][0]
            x1, y1 = points[0][0]
            cv2.line(src, (x,y), (x1,y1),color,1)
        else:
            x, y = points[i][0]
            x1, y1 = points[i+1][0]
            cv2.line(src, (x,y), (x1,y1),color,1)
        i = i + 1

# img = cv2.imread('/home/hyrozine/hand.jpg')
img = cv2.imread('/home/hyrozine/hello.png')

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

ret, binary = cv2.threshold(gray, 180,255,cv2.THRESH_BINARY_INV)
# findContours(img, mode, ApproximationMode ...)
# return contours and hierarchy
# mode : RETR_EXTERNAL = 0, RETR_LIST = 1, RETR_CCOMP = 2 \
# RETR_TREE = 3
# ApproximationMode : CHAIN_APPROX_NONE, CHAIN_APPROX_SIMPLE
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
print(contours)

# drawContours(img, contours, contourIdx, color, thickness)
cv2.drawContours(img, contours, -1, (255,100,1), 1)

# contourArea(contours)        
# arcLength(curves, closed)
# area = cv2.contourArea(contours[0])
# print("area=%d"%(area))
# length = cv2.arcLength(contours[0], True)
# print("length=%d"%(length))

# e = 0.1
# # approxPolyDP(curve, epsilon, closed)
# approx = cv2.approxPolyDP(contours[1], e, True)
# drawShape(img, approx,(0,0,255))

# #convexHull(points, clockwise, ...)
# hull = cv2.convexHull(contours[1])
# drawShape(img, hull,(0,255,0))

# minAreaRect(points) 
# return RotatedRect : x, y   width, height  angle
min_rect = cv2.minAreaRect(contours[2])
# only get the points, don't need angle
box = cv2.boxPoints(min_rect)
box = np.int0(box)
cv2.drawContours(img,[box], 0, (0, 0, 255), 2)

# boundingRect(array)
# return rect
x,y,w,h = cv2.boundingRect(contours[2])

cv2.rectangle(img, (x, y), (w+x, h+y), (255, 0, 0), 2)

cv2.imshow('binary',binary)
cv2.imshow('img',img)

cv2.waitKey(0)