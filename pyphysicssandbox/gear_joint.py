import pymunk

from .base_shape import BaseShape


class Gear(BaseShape):
    def __init__(self, space, shape1, shape2, angle=0):
        # Associate the gear joint with the location of one of the bodies so
        # it is removed when that body is out of the simulation
        self.body = shape1.body
        self.shape = pymunk.GearJoint(shape1.body, shape2.body, angle, 1)
        super().__init__()

        space.add(self.shape)

    def has_own_body(self):
        return False

    def _draw(self, screen):
        pass

    def _pin_points(self):
        raise Exception('Do not use paste_on for gears')

    def __repr__(self):
        return 'gear: p(' + str(self.body.position.x) + ',' + str(self.body.position.y) + ')'

