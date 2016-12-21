import pygame
import pymunk

from .base_shape import BaseShape


class Pin(BaseShape):
    def __init__(self, space, p1, shape1, p2, shape2):
        # Associate the pin with the location of one of the bodies so
        # it is removed when that body is out of the simulation
        self.body = shape1.body

        ax = p1[0] - shape1.body.position.x
        ay = p1[1] - shape1.body.position.y
        bx = p2[0] - shape2.body.position.x
        by = p2[1] - shape2.body.position.y

        self.shape = pymunk.PinJoint(shape1.body, shape2.body, (ax, ay), (bx, by))
        super().__init__()

        space.add(self.shape)

    def has_own_body(self):
        return False

    def _draw(self, screen):
        p1 = self.shape.a.local_to_world(self.shape.anchor_a)
        p2 = self.shape.b.local_to_world(self.shape.anchor_b)

        pygame.draw.line(screen, self.color, p1, p2, 1)
        pygame.draw.circle(screen, self.color, (int(p1[0]), int(p1[1])), 2)
        pygame.draw.circle(screen, self.color, (int(p2[0]), int(p2[1])), 2)

    def _pin_points(self):
        raise Exception('Do not use paste_on for pins')

    def __repr__(self):
        p1 = self.body.local_to_world(self.shape.a)
        p2 = self.body.local_to_world(self.shape.b)

        return 'pin: p1(' + str(p1.x) + ',' + str(p1.y) + '), p2(' + str(p2.x) + ',' + str(p2.y) + ')'

