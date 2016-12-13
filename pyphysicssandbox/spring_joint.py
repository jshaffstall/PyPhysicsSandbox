import pymunk
import math

from .base_shape import BaseShape


class Spring(BaseShape):
    def __init__(self, space, p1, shape1, p2, shape2, length, stiffness, damping):
        # Associate the joint with the location of one of the bodies so
        # it is removed when that body is out of the simulation
        self.body = shape1.body
        self.shape = pymunk.DampedSpring(shape1.body, shape2.body, p1, p2, length, stiffness, damping)
        super().__init__()

        space.add(self.shape)

    def has_own_body(self):
        return False

    def _draw(self, screen):
        pass

    def _pin_points(self):
        raise Exception('Do not use draw_on for springs')

    def __repr__(self):
        p1 = (self.shape.anchor_a[0] + self.shape.a.position[0], self.shape.anchor_a[1] + self.shape.a.position[1])
        p2 = (self.shape.anchor_b[0] + self.shape.b.position[0], self.shape.anchor_b[1] + self.shape.b.position[1])

        return 'spring: p1(' + str(p1[0]) + ',' + str(p1[1]) + '), p2(' + str(p2[0]) + ',' + str(p2[1]) + \
               '), length: ' + str(math.sqrt(math.pow(p1[0]-p2[0], 2)+math.pow(p1[1]-p2[1], 2)))
