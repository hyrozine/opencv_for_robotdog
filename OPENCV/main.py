import cv2
from utils import COLOR_THRESHOLD, img_size
from state import state_machine

if __name__ == '__main__':
     
    video = cv2.VideoCapture(0, cv2.CAP_V4L2)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, img_size[0])
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, img_size[1])
    video.set(6, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
    
    while video.isOpened():
            ret,frame = video.read()
            if frame is None:
                break
            if ret == True:
                state_machine.state_machine_exe(frame)
                # cv2.imshow('video',frame)
                key = cv2.waitKey(1)
                if(key & 0xFF == ord('q')) :
                    break
video.release()
cv2.destroyAllWindows()
