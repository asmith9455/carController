pyjoy_path = sys.path[0] + '\\pyvjoy'
site.addsitedir(pyjoy_path)       # from https://github.com/tidzo/pyvjoy
import pyvjoy

MAX_VJOY = 32767    #max value for analog inputs (min value is 1 (or 0?))

class controller_sim:
    def __init__ (self, devId):
        self.vj = pyvjoy.VJoyDevice(devId)

    def set_t(self, t):
        #throttle
        self.vj.data.wAxisXRot = int(t * MAX_VJOY)

    def set_s(self, s):     #-1.0 for full left, +1.0 for full right
        tmp_s = (s + 1.0) / 2.0
        self.vj.data.wAxisX = int(tmp_s * MAX_VJOY)

    def set_b(self, b):
        self.vj.data.wAxisYRot = int(b * MAX_VJOY)

    def reset(self):
        self.vj.reset()
        self.set_tsb(0.0, 0.0, 0.0)

    def set_tsb(self, t, s, b):
        self.set_t(t)       #throttle
        self.set_s(s)       #steering
        self.set_b(b)       #braking



        
        