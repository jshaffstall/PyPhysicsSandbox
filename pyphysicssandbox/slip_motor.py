import pygame
import pymunk
import math

from .rotary_spring import RotarySpring
from .motor_joint import Motor
from pyphysicssandbox import add_observer
from pyphysicssandbox import deactivate
from pyphysicssandbox import reactivate


class SlipMotor(Motor):
    def __init__(self, space, shape1, shape2, rest_angle, stiffness, damping, slip_angle, speed):
        super().__init__(space, shape1, speed)

        self._spring = RotarySpring(space, shape1, shape2, rest_angle, stiffness, damping)
        self._slip_angle = -slip_angle
        self._rest_angle = -rest_angle

    def observer(self, keys):
        super().observer(keys)

        degrees = math.degrees(self.body.angle)

        if self.active:
            if self.shape.rate < 0:
                if degrees <= self._slip_angle:
                    deactivate(self)
            else:
                if degrees >= self._slip_angle:
                    deactivate(self)
        else:
            if self.shape.rate > 0:
                if degrees <= self._rest_angle:
                    reactivate(self)
            else:
                if degrees >= self._rest_angle:
                    reactivate(self)

    def _pin_points(self):
        raise Exception('Do not use paste_on for slip motors')

    def __repr__(self):
        return 'slip motor: p(' + str(self.body.position.x) + ',' + str(self.body.position.y) + '), rest angle: ' + \
               str(-self._rest_angle) + ' slip angle ' + str(-self._slip_angle)
