from PIL import ImageGrab
import numpy as np
import cv2


class screen_grabber:

    def __init__(self, return_size):
        self.bbox = (0,0,1920,1080)
        self.return_size = return_size

    def get_img(self):
        #from ibininja at https://stackoverflow.com/questions/35097837/capture-video-data-from-screen-in-python
        img_og = ImageGrab.grab(bbox=self.bbox) #bbox specifies specific region (bbox= x,y,width,height)
        img_np = np.array(img_og)
        img = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, self.return_size)
        return img
        