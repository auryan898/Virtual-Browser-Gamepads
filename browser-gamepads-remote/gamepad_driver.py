import pyautogui
import pydirectinput
import pyvjoy

AXES = {
    'lx':pyvjoy.HID_USAGE_X, # left stick x
    'ly':pyvjoy.HID_USAGE_Y, # left stick y
    'rx':pyvjoy.HID_USAGE_RX, # right stick x
    'ry':pyvjoy.HID_USAGE_RY, # right stick y
    't' :pyvjoy.HID_USAGE_Z, # both triggers combined (use -0x4000 to +0x4000)
    'lt':pyvjoy.HID_USAGE_Z, # also for left trigger
    'rt':pyvjoy.HID_USAGE_RZ, # can just be right trigger
    'hx':pyvjoy.HID_USAGE_SL0, # dpad (hat) x value
    'hy':pyvjoy.HID_USAGE_SL1, # dpad (hat) y value
}

BUTTONS = {
    'a':1,
    'b':2,
    'x':3,
    'y':4,
    'lb':5, # left bumper
    'rb':6, # right bumper
    'bk':7, # back
    'st':8, # start
    'lc':9, # left stick button
    'rc':10,# right stick button
    'gb':11,# center guide button
}

def flt_to_vjoy(flt_value): # 0x8000 = 32768
    return int(flt_value * 0x8000)

def vjoy_to_flt(vjoy_value): # 0x8000 = 32768
    return vjoy_value / 0x8000

def update_vjoy(stick_num, data):
    j = pyvjoy.VJoyDevice(stick_num)
    for key, value in data.items():
        if key in AXES:
            if key == 't':
                value += 0x4000
            j.set_axis(AXES[key], value)
        if key in BUTTONS:
            j.set_button(BUTTONS[key], value)

DEFAULT_VALUES = {
    'lx': 0x4000,
    'ly': 0x4000,
    'rx': 0x4000,
    'ry': 0x4000,
    # 't': 0, # It's normalized for this key, -0x4000 to +0x4000
    'lt': 0x0000, # Especially 0 for triggers
    'rt': 0x0000,
    'hx': 0x4000,
    'hy': 0x4000,
    'a': 0,
    'b': 0,
    'x': 0,
    'y': 0,
    'lb': 0,
    'rb': 0,
    'bk': 0,
    'st': 0,
    'lc': 0,
    'rc': 0,
    'gb': 0
}

def set_default_values_vjoy(stick_num):
    '''
    >>> import time
    >>> update_vjoy(1, {'lx':0x8000, 'hx': 0x8000})
    >>> time.sleep(2)
    >>> set_default_values_vjoy(1)
    '''
    update_vjoy(stick_num, DEFAULT_VALUES)

class GamepadAssigner(object):
    _assigner = None

    @classmethod
    def get_assigner(cls):
        '''
        >>> import time
        >>> a = GamepadAssigner.get_assigner()
        >>> a.set_vjoy_gamer('ryan', 2)
        >>> time.sleep(2)
        >>> print(a.vjoy_gamer_id['ryan'])
        2
        >>> print(a.vjoy_gamer_stick[1])
        ryan
        >>> a.update_vjoy_gamer_data('ryan', {'lx':0x8000})
        >>> time.sleep(2)
        >>> set_default_values_vjoy(2)
        '''
        if not cls._assigner:
            cls._assigner = GamepadAssigner()
        return cls._assigner

    def __init__(self):
        self.vjoy_gamer_id = {} # dictionary of gamer ID to vjoy number. 0 for unassigned.
        self.vjoy_gamer_stick = [None, None, None, None] # list matching stick_num to gamer ID
        for i in range(4):
            set_default_values_vjoy(i+1)

    def update_gamers_json(self, gamer_data):
        for gamer_id, data in gamer_data.items():
            self.update_vjoy_gamer_data(gamer_id, data)

    def set_vjoy_gamer(self, gamer_id, stick_num):
        '''
        >>> import time
        >>> a = GamepadAssigner()
        >>> a.set_vjoy_gamer('ryan', 2)
        >>> time.sleep(2)
        >>> print(a.vjoy_gamer_id['ryan'])
        2
        >>> print(a.vjoy_gamer_stick[1])
        ryan
        >>> a.update_vjoy_gamer_data('ryan', {'lx':0x8000})
        >>> time.sleep(2)
        >>> set_default_values_vjoy(2)
        '''
        if self._unassign_vjoy_stick(stick_num):
            set_default_values_vjoy(stick_num)
            self._assign_vjoy_gamer(gamer_id, stick_num)

    def update_vjoy_gamer_data(self, gamer_id, data):
        '''
        >>> import time
        >>> a = GamepadAssigner()
        >>> a.vjoy_gamer_id['bob'] = 3
        >>> time.sleep(1)
        >>> update_vjoy(3, {'x': 3})
        >>> time.sleep(1)
        >>> a.update_vjoy_gamer_data('bob', {'ly': 0x4000})
        >>> time.sleep(2)
        >>> set_default_values_vjoy(3)
        '''
        if gamer_id in self.vjoy_gamer_id:
            stick_num = self.vjoy_gamer_id[gamer_id]
            if stick_num >= 1 and stick_num <= 4: # valid id
                update_vjoy(stick_num, data) # stateless function

    def _assign_vjoy_gamer(self, gamer_id, stick_num):
        if stick_num >= 1 and stick_num <= 4:
            self.vjoy_gamer_id[gamer_id] = stick_num
            self.vjoy_gamer_stick[stick_num - 1] = gamer_id
    def _unassign_vjoy_stick(self, stick_num):
        i = stick_num - 1 # [1,4] -> [0,3]
        if i > 3 or i < 0:
            return False
        gamer_id = self.vjoy_gamer_stick[i]
        self.vjoy_gamer_stick[i] = None
        if gamer_id is not None and gamer_id in self.vjoy_gamer_id:
            self.vjoy_gamer_id[gamer_id] = 0
        return True

if __name__=='__main__':
    import doctest
    doctest.testmod()