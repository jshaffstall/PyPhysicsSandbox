import pygame
import pymunk

from .base_shape import BaseShape
from .util import to_pygame


class Pivot(BaseShape):
    def __init__(self, space, x, y):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = x, y
        self.shape = []
        self.space = space
        super().__init__()

        space.add(self.body)

    def connect(self, shape):
        join = pymunk.PivotJoint(shape.body, self.body, self.body.position)
        self.shape.append(join)
        self.space.add(join)

    def _draw(self, screen):
        p = to_pygame(self.body.position)
        pygame.draw.circle(screen, self.color, p, 5, 0)
