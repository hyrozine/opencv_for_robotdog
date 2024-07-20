#!/usr/bin/python3
import cv2

def cv_show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# #Greyscale only
# img = cv2.imread('/home/hyrozine/test_pic.jpg',cv2.IMREAD_GRAYSCALE)
# cv2.imshow('img',img) 
# key = cv2.waitKey(0)
# if(key & 0xff == ord('q')):   
#     cv2.destroyAllWindows()

# # save pictures
# img = cv2.imread('/home/hyrozine/test_pic.jpg',cv2.IMREAD_GRAYSCALE)
# cv2.imshow('img',img) 
# while True:

#     key = cv2.waitKey(0)
#     if(key & 0xff == ord('q')):
#         print("quit")   
#         break
#     elif(key & 0xff == ord('s')):
#         print("the picture has been saved, press q to quit")
#         cv2.imwrite('/home/hyrozine/grey_version.jpg',img)
#     else:
#         print("invalid input")
# cv2.destroyAllWindows()


# #read a video
# cv2.namedWindow('video',cv2.WINDOW_AUTOSIZE)
# cv2.resizeWindow('video',640,480)

# vc = cv2.VideoCapture('/home/hyrozine/test_video.mp4')
# while vc.isOpened():
#     ret,frame = vc.read()
#     if frame is None:
#         break
#     if ret == True:
#         gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#         cv2.imshow('video',gray)
#         key = cv2.waitKey(1)
#         if(key & 0xFF == ord('q')) :
#             break
# vc.release()
# cv2.destroyAllWindows()

# # write a video
# # create a video writer
# fourcc = cv2.VideoWriter_fourcc(*'MJPG')
# vw = cv2.VideoWriter('/home/hyrozine/output.mp4',fourcc,25,(1280,720))
# # if use a real camera, the setting resolution should match the resolution of the camera

# # create the window
# cv2.namedWindow('video',cv2.WINDOW_NORMAL)
# cv2.resizeWindow('video',640,480)

# vc = cv2.VideoCapture(0)

# while vc.isOpened():
#     ret,frame = vc.read()
#     if frame is None:
#         break
#     if ret == True:
#         cv2.imshow('video',frame)

#         # put the frame into the window, avoiding the window being dialted by the video, which may be considered as a bug
#         cv2.resizeWindow('video',640,480)

#         vw.write(frame)

#         key = cv2.waitKey(1)
#         if(key & 0xFF == ord('q')) :
#             break
# vc.release()
# cv2.destroyAllWindows()


# boundary fill
# top_size,bottom_size,left_size,right_size = (50,50,50,50)
# replicate = cv2.copyMakeBorder(img,top_size,bottom_size,left_size,right_size,borderType=cv2.BORDER_REPLICATE)
# reflect = cv2.copyMakeBorder(img,top_size,bottom_size,left_size,right_size,cv2.BORDER_REFLECT)
# reflect101 = cv2.copyMakeBorder(img,top_size,bottom_size,left_size,right_size,cv2.BORDER_REFLECT_101)
# wrap = cv2.copyMakeBorder(img,top_size,bottom_size,left_size,right_size,cv2.BORDER_WRAP)
# constant = cv2.copyMakeBorder(img,top_size,bottom_size,left_size,right_size,cv2.BORDER_CONSTANT,value=0)



