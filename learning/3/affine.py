import cv2
import numpy as np

img = cv2.imread('/home/hyrozine/pic1.jpg')

h, w, ch = img.shape

#M = np.float32([[0.7, 0.7, 10],[-0.7, 0.7, -10]])

# get M through API    cv2.getRotationMatrix2D(center, angle, scale)
# counterclockwise is positive
# M = cv2.getRotationMatrix2D((w/2, h/2), 45, 0.5)

# getAffineTransform(src[],dst[]) 
# get transform by 3 points
src = np.float32([[100, 50], [100, 300], [300, 50]])
dst = np.float32([[50, 100], [50, 350], [150, 150]])
M = cv2.getAffineTransform(src, dst)

print(M)

# cv2.warpAffine(src, M, dsize, flags, mode, value)
new = cv2.warpAffine(img, M, ((int)(w/1.1), (int)(h/1.1)))

cv2.imshow ('new',new)

cv2.waitKey(0)