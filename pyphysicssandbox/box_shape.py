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
        self.static = static

        super().__init__()

        space.add(self.body, self.shape)

    def _draw(self, screen):
        ps = [self.body.local_to_world(v) for v in self.shape.get_vertices()]
        ps += [ps[0]]

        pygame.draw.polygon(screen, self.color, ps)
        pygame.draw.lines(screen, self.color, False, ps, self.radius)

    def _pin_points(self):
        x1 = self.body.position.x
        y1 = self.body.position.y + (self.height/2)
        x2 = x1 + self.width
        y2 = y1

        return (x1, y1), (x2, y2)

    def __repr__(self):
        prefix = 'box'

        if self.static:
            prefix = 'static_box'

        return prefix+': p(' + str(self.body.position.x) + ',' + str(self.body.position.y) + '), width: ' + \
            str(self.width) + ', height: ' + str(self.height)
