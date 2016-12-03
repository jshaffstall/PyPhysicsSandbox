import pygame
import pymunk

from .base_shape import BaseShape


class Box(BaseShape):
    def __init__(self, space, x, y, width, height, radius, mass, static):
        moment = pymunk.moment_for_box(mass, (width, height))

        if static:
            self.body = pymunk.Body(mass, moment, pymunk.Body.STATIC)
        else:
            self.body = pymunk.Body(mass, moment)

        self.body.position = x, y
        self.shape = pymunk.Poly.create_box(self.body, (width, height), radius)
        self.width = width
        self.height = height
        self.radius = radius
        super().__init__()

        space.add(self.body, self.shape)

    def _draw(self, screen):
        ps = [self.body.local_to_world(v) for v in self.shape.get_vertices()]
        ps += [ps[0]]

        pygame.draw.polygon(screen, self.color, ps)
        pygame.draw.lines(screen, self.color, False, ps, self.radius)
