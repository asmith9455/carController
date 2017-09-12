from key_io import *
from controller_vjoy import controller_vjoy


if __name__ == "__main__":
    ctrler = controller_vjoy(1)
    #ctrler.pulse_btn(5, delay = 5, hold = 1)
    
    ctrler.pulse('b', 0.0, 1.0, delay = 5, hold = 1)

    ctrler.pulse('s', 0.0, 0.25, delay = 0, hold = 1)
    ctrler.pulse('s', 0.0, -0.25, delay = 0, hold = 1)
    
    ctrler.pulse('b', 0.0, 1.0, delay = 5, hold = 10)
    #ctrler.pulse('t', 0.0, 1.0, delay = 0, hold = 5)
    #ctrler.pulse('b', 0.0, 1.0, delay = 0, hold = 10)
    