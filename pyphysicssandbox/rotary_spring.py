import pymunk
import math

from .base_shape import BaseShape


class RotarySpring(BaseShape):
    def __init__(self, space, shape1, shape2, angle, stiffness, damping):
        # Associate the joint with the location of one of the bodies so
        # it is removed when that body is out of the simulation
        self.body = shape1.body
        self.shape = pymunk.DampedRotarySpring(shape1.body, shape2.body, math.radians(-angle), stiffness, damping)
        super().__init__()

        space.add(self.shape)

    def has_own_body(self):
        return False

    def _draw(self, screen):
        pass

    def _pin_points(self):
        raise Exception('Do not use draw_on for rotary springs')

    def __repr__(self):
        return 'rotary_spring: p(' + str(self.body.position.x) + ',' + str(self.body.position.y) + '), rest angle: ' + \
               str(-math.degrees(self.shape.rest_angle))


