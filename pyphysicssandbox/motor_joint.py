import pygame
import pymunk

from .base_shape import BaseShape
from .util import to_pygame


class Motor(BaseShape):
    def __init__(self, space, shape1, speed):
        # Associate the motor with the location of one of the bodies so
        # it is removed when that body is out of the simulation
        self.body = shape1.body
        self.shape = pymunk.SimpleMotor(shape1.body, space.static_body, speed)
        super().__init__()

        space.add(self.shape)

    def has_own_body(self):
        return False

    def _draw(self, screen):
        p = to_pygame(self.body.position)
        radius = 10
        rect = pygame.Rect(p[0] - radius/2, p[1] - radius/2, radius, radius)

        pygame.draw.arc(screen, self.color, rect, 1, 6)

        if self.shape.rate > 0:
            pygame.draw.circle(screen, self.color, rect.topright, 2, 0)
        else:
            pygame.draw.circle(screen, self.color, rect.bottomright, 2, 0)

    def _pin_points(self):
        raise Exception('Do not use paste_on for motors')

    def __repr__(self):
        return 'motor: p(' + str(self.body.position.x) + ',' + str(self.body.position.y) + '), speed: ' + \
            str(self.shape.speed)

