import pygame
import pymunk
import math

from .base_shape import BaseShape


class Box(BaseShape):
    def __init__(self, space, x, y, width, height, radius, mass, static, cosmetic=False):

        if not cosmetic:
            moment = pymunk.moment_for_box(mass, (width, height))

            if static:
                self.body = pymunk.Body(mass, moment, pymunk.Body.STATIC)
            else:
                self.body = pymunk.Body(mass, moment)

            self.body.position = x, y
            self.shape = pymunk.Poly.create_box(self.body, (width, height), radius)
            space.add(self.body, self.shape)

        self.width = width
        self.height = height
        self.radius = radius
        self.static = static
        self._x = x
        self._y = y

        super().__init__(cosmetic)

    def _draw(self, screen):
        if self._cosmetic:
            x = self._x-self.width/2
            y = self._y-self.height/2

            ps = [(x, y), (x+self.width, y), (x+self.width, y+self.height), (x,y+self.height), (x, y)]
        else:
            ps = [self.body.local_to_world(v) for v in self.shape.get_vertices()]
            ps += [ps[0]]

        pygame.draw.polygon(screen, self.color, ps)
        pygame.draw.lines(screen, self.color, False, ps, self.radius)

    def _pin_points(self):
        x1 = self.body.position.x - (self.width/2)
        y1 = self.body.position.y + (self.height/2)
        x2 = x1 + self.width
        y2 = y1

        return (x1, y1), (x2, y2)

    def __repr__(self):
        prefix = 'box'

        if self.static:
            prefix = 'static_box'

        if self._cosmetic:
            prefix = 'cosmetic_box'

        return prefix+': p(' + str(self.body.position.x) + ',' + str(self.body.position.y) + '), width: ' + \
            str(self.width) + ', height: ' + str(self.height) + ', angle: ' + str(self.angle)
