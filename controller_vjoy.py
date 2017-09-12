import sys,site
pyjoy_path = sys.path[0] + '\\pyvjoy'
site.addsitedir(pyjoy_path)       # from https://github.com/tidzo/pyvjoy
import pyvjoy
import time


MAX_VJOY = 32767    #max value for analog inputs (min value is 1 (or 0?))

class controller_vjoy:

    last_t = 0.0
    last_s = 0.0
    last_b = 0.0

    def __init__ (self, devId):
        self.vj = pyvjoy.VJoyDevice(1)
        self.set_tsb(0.0,0.0,0.0)

    def set_t(self, t):
        #throttle
        self.vj.data.wAxisXRot = int(t * MAX_VJOY)
        self.vj.update()
        if t != self.last_t:
            print("throttle changed from ", self.last_t, " to ", t)
            self.last_t = t

    def set_s(self, s):     #-1.0 for full left, +1.0 for full right
        tmp_s = (s + 1.0) / 2.0
        self.vj.data.wAxisX = int(tmp_s * MAX_VJOY)
        self.vj.update()
        if s != self.last_s:
            print("steering changed from ", self.last_s, " to ", s)
            self.last_s = s

    def set_b(self, b):
        self.vj.data.wAxisYRot = int(b * MAX_VJOY)
        self.vj.update()
        if b != self.last_b:
            print("braking changed from ", self.last_b, " to ", b)
            self.last_b = b

    def reset(self):
        self.vj.reset()
        self.set_tsb(0.0, 0.0, 0.0)
        self.vj.update()

    def set_tsb(self, t, s, b):
        self.set_t(t)       #throttle
        self.set_s(s)       #steering
        self.set_b(b)       #braking

    def delay(self, delayTime, countdownText):
       for i in range(delayTime)[::-1]:
            print(countdownText,": ", i+1)
            time.sleep(1)

    def pulse_btn(self, btnNum, delay = 3, hold = 1):
        self.vj.set_button(btnNum, 0)
        self.delay(delay, "delay")
        self.vj.set_button(btnNum, 1)
        self.delay(hold, "hold")
        self.vj.set_button(btnNum, 0)

    def pulse(self, tsb_char, start_and_end_val, pulse_val, delay = 3, hold = 1):

        set_fcn = None

        if tsb_char == 't':
            set_fcn = self.set_t
            print("pulsing throttle")
        elif tsb_char == 's':
            set_fcn = self.set_s
            print("pulsing steering")
        elif tsb_char == 'b':
            set_fcn = self.set_b
            print("pulsing braking")

        set_fcn(start_and_end_val)

        self.delay(delay, "delay")
        
        set_fcn(pulse_val)
        print("pulsing signal and holding")
        self.delay(hold, "hold")
        

        set_fcn(start_and_end_val)
        print("releasing value")