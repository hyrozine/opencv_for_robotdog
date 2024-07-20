import cv2
from state import state_machine
img_size = (640, 480)

if __name__ == '__main__':
    video = cv2.VideoCapture(0)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, img_size[0])
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, img_size[1])
    video.set(cv2.CAP_PROP_FPS, 30)
    while video.isOpened():
        ret,frame = video.read()
        if frame is None:
            break
        if ret == True:
            state_machine.state_machine_exe(frame)

            key = cv2.waitKey(1)
            if(key & 0xFF == ord('q')) :
                break
video.release()
cv2.destroyAllWindows()