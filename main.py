from key_io import *
import sys,site

import time

MAX_VJOY = 32767
j = pyvjoy.VJoyDevice(1)

def play_function(X,Y,Z,XRot):
    j.data.wAxisX = int(X * MAX_VJOY)
    j.data.wAxisY = int(Y * MAX_VJOY)
    j.data.wAxisZ = int(Z * MAX_VJOY)
    j.data.wAxisXRot = int(XRot * MAX_VJOY)
    
    j.update()

def set_tsb(t, s, b):

    #steering
    tmp_s = (s + 1.0) / 2.0
    j.data.wAxisX = int(tmp_s * MAX_VJOY)
    
    #throttle
    j.data.wAxisXRot = int(t * MAX_VJOY)
    
    #braking
    j.data.wAxisYRot = int(b * MAX_VJOY)




def x_ax_left():
    #Set X axis to fully left
    j.set_axis(pyvjoy.HID_USAGE_X, 0x1)

def x_ax_middle():
    #Set X axis to fully right
    j.set_axis(pyvjoy.HID_USAGE_X, 0x4000)

def x_ax_right():
    #Set X axis to fully right
    j.set_axis(pyvjoy.HID_USAGE_X, 0x8000)

def set_btn_15():
    j.set_button(5,1)

def reset_btn_15():
    j.set_button(5,0)


def pulse_left():
    


if __name__ == "__main__":
    print("resetting controller")
    #play_function(0.5, 0.5, 0, 0)
    x_ax_middle()
    #goLeft()
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    
    #steer left, steer right, throttle, brake

    #play_function(0, 0.5, 0, 0)
    x_ax_right()
    print("set value, holding for 1 second")
    time.sleep(2)


    #play_function(0.5, 0.5, 0, 0)
    x_ax_middle()
    print("releasing value")