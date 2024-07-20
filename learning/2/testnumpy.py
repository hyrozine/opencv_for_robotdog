import numpy as np
import cv2
# a = np.array([1,2,3])
# print(a)

# b = np.array([[1,2,3],[3,4,5]])
# print(b)

# #  in opencv: row col channel     same as np.ones()     
# #  in python: print() -> channel row col
# c = np.zeros((480,640,4),np.uint8)
# print(c)

# # fill with the same number
# d = np.full((480,640),10,np.uint8)
# print(d)

# e = np.identity(8)
# print(e)

# f = np.eye(5,7,k = 3)  # k : to specify the 1 start from which col
# print(f)

# # search matrix
# img = np.zeros((480,640,3),np.uint8)

# count = 0
# while count < 200:
#     img[count,100, 0] = 255  # the '0' specifies which channel to change. Here is the 'B' channel.
#     # an another way same as above
#     # img[count, 100] = [255, 0, 0]
#     count = count + 1

# cv2.imshow('img',img)

# key = cv2.waitKey(0)
# if key & 0xff == ord('q'):
#     cv2.destryAllWindows()

# obtain submatrix
img = np.zeros((480,640,3),np.uint8)
roi = img[100:400, 100:600]
roi[:,:] = [0, 0, 255]    # roi[:,:] <==> roi[:] 
roi[10:200,10:200] = [0,255,0]
roi[5:200,5:200,0] = 255

cv2.imshow('img',img)
key = cv2.waitKey(0)
if key & 0xff == ord('q'):
    cv2.destroyAllWindows()