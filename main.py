from key_io import *
from controller_vjoy import controller_vjoy
from screen_grabber import screen_grabber
from img_processing import img_processor_v001
import cv2
import time

img_size = (1280, 720)



def set_tsb_from_image(img):
    pass

if __name__ == "__main__":
    ctrler = controller_vjoy(1)

    #ctrler.pulse('t', 0.0, 0.5, delay = 2, hold = 3)

    ctrler.pulse('t', 0.0, 1.0, delay = 3, hold = 2)
    ctrler.pulse('s', 0.0, 0.4, delay = 0, hold = 2)
    ctrler.pulse('b', 0.0, 1.0, delay = 0, hold = 5)

    exit()

    sg = screen_grabber(img_size)
    while(True):
        img = sg.get_img()
        set_tsb_from_image(img)

        cv2.imshow("original capture", img)
        if cv2.waitKey(1) == 27:
            break

        time.sleep(0.05)    #control processing rate
    
    cv2.destroyAllWindows()

    exit()

    
    #ctrler.pulse_btn(5, delay = 5, hold = 1)
    
    ctrler.pulse('b', 0.0, 1.0, delay = 1, hold = 1)

    ctrler.pulse('s', 0.0, 0.25, delay = 0, hold = 1)
    ctrler.pulse('s', 0.0, -0.25, delay = 0, hold = 1)
    
    ctrler.pulse('b', 0.0, 1.0, delay = 5, hold = 10)
    #ctrler.pulse('t', 0.0, 1.0, delay = 0, hold = 5)
    #ctrler.pulse('b', 0.0, 1.0, delay = 0, hold = 10)
    