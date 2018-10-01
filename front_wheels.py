#!/usr/bin/env python
from PCA9685 import Servo
import filedb


class Front_Wheels(object):
    """ Front wheels control class """
    FRONT_WHEEL_CHANNEL = 0

    _DEBUG = False
    _DEBUG_INFO = 'DEBUG "front_wheels.py":'

    def __init__(self, debug=False, db="config", bus_number=1, channel=FRONT_WHEEL_CHANNEL):
        """ setup channels and basic stuff """
        self.db = filedb.fileDB(db=db)
        self._channel = channel
        self._straight_angle = 90
        self.turning_max = 20
        self._turning_offset = int(self.db.get('turning_offset', default_value=0))

        self.wheel = Servo.Servo(self._channel, bus_number=bus_number, offset=self.turning_offset)

        self.debug = debug
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Front wheel PWM channel:', self._channel)
            print(self._DEBUG_INFO, 'Front wheel offset value:', self.turning_offset)

        self._angle = {"left": self._min_angle, "straight": self._straight_angle, "right": self._max_angle}
        if self._DEBUG:
            print(self._DEBUG_INFO, 'left angle: %s, straight angle: %s, right angle: %s' % (
            self._angle["left"], self._angle["straight"], self._angle["right"]))

    def turn_left(self):
        """ Turn the front wheels left """
        if self._DEBUG:
            print(self._DEBUG_INFO, "Turn left")
        self.wheel.write(self._angle["left"])

    def turn_straight(self):
        """ Turn the front wheels back straight """
        if self._DEBUG:
            print(self._DEBUG_INFO, "Turn straight")
        self.wheel.write(self._angle["straight"])

    def turn_right(self):
        """ Turn the front wheels right """
        if self._DEBUG:
            print(self._DEBUG_INFO, "Turn right")
        self.wheel.write(self._angle["right"])

    def turn(self, angle):
        """ Turn the front wheels to the giving angle """
        if self._DEBUG:
            print(self._DEBUG_INFO, "Turn to", angle)
        if angle < self._angle["left"]:
            angle = self._angle["left"]
        if angle > self._angle["right"]:
            angle = self._angle["right"]
        self.wheel.write(angle)

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, chn):
        self._channel = chn

    @property
    def turning_max(self):
        return self._turning_max

    @turning_max.setter
    def turning_max(self, angle):
        self._turning_max = angle
        self._min_angle = self._straight_angle - angle
        self._max_angle = self._straight_angle + angle
        self._angle = {"left": self._min_angle, "straight": self._straight_angle, "right": self._max_angle}

    @property
    def turning_offset(self):
        return self._turning_offset

    @turning_offset.setter
    def turning_offset(self, value):
        if not isinstance(value, int):
            raise TypeError('"turning_offset" must be "int"')
        self._turning_offset = value
        self.db.set('turning_offset', value)
        self.wheel.offset = value
        self.turn_straight()

    @property
    def debug(self):
        return self._DEBUG

    @debug.setter
    def debug(self, debug):
        """ Set if debug information shows """
        if debug in (True, False):
            self._DEBUG = debug
        else:
            raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

        if self._DEBUG:
            print(self._DEBUG_INFO, "Set debug on")
            print(self._DEBUG_INFO, "Set wheel debug on")
            self.wheel.debug = True
        else:
            print(self._DEBUG_INFO, "Set debug off")
            print(self._DEBUG_INFO, "Set wheel debug off")
            self.wheel.debug = False

    def ready(self):
        """ Get the front wheels to the ready position. """
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Turn to "Ready" position')
        self.wheel.offset = self.turning_offset
        self.turn_straight()

    def pwm_reset(self):
        """ Resetting the PCA9685 module """
        if self._DEBUG:
            print(self._DEBUG_INFO, 'TEST')
        self.wheel.reset()

    def calibration(self):
        """ Get the front wheels to the calibration position. """
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Turn to "Calibration" position')
        self.turn_straight()
        self.cali_turning_offset = self.turning_offset

    def cali_left(self):
        """ Calibrate the wheels to left """
        self.cali_turning_offset -= 10
        self.wheel.offset = self.cali_turning_offset
        self.turn_straight()

    def cali_right(self):
        """ Calibrate the wheels to right """
        self.cali_turning_offset += 10
        self.wheel.offset = self.cali_turning_offset
        self.turn_straight()
        
    def cali_accurate_left(self):
        """ Accurate Calibrate the wheels to left """
        self.cali_turning_offset -= 1
        self.wheel.offset = self.cali_turning_offset
        self.turn_straight()

    def cali_accurate_right(self):
        """ Accurate Calibrate the wheels to right """
        self.cali_turning_offset += 1
        self.wheel.offset = self.cali_turning_offset
        self.turn_straight()

    def return_cali_offset(self):
        """ Return the calibration value """
        return self.cali_turning_offset
