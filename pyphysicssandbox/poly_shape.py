import pygame
import pymunk

from .base_shape import BaseShape
from py2d.Math.Polygon import *


class Poly(BaseShape):
    def __init__(self, space, x, y, vertices, radius, mass, static, cosmetic=False):
        if not cosmetic:
            moment = pymunk.moment_for_poly(mass, vertices, (0, 0), radius)

            if static:
                self.body = pymunk.Body(mass, moment, pymunk.Body.STATIC)
            else:
                self.body = pymunk.Body(mass, moment)

            self.body.position = x, y
            self.static = static

            temp = Polygon.from_tuples(vertices)
            polys = Polygon.convex_decompose(temp)

            shapes = []

            for poly in polys:
                shapes.append(pymunk.Poly(self.body, poly.as_tuple_list(), None, radius))

            self.shape = shapes
            space.add(self.body, self.shape)

        self.radius = radius
        self._x = x
        self._y = y
        self._vertices = vertices

        super().__init__(cosmetic)

    def _draw(self, screen):
        if self._cosmetic:
            pygame.draw.polygon(screen, self.color, [(v[0] + self._x, v[1] + self._y) for v in self._vertices])
        else:
            for shape in self.shape:
                ps = [self.body.local_to_world(v) for v in shape.get_vertices()]

                pygame.draw.polygon(screen, self.color, ps)

    def _pin_points(self):
        x1 = self.body.position.x-5
        y1 = self.body.position.y
        x2 = self.body.position.x+5
        y2 = y1

        return (x1, y1), (x2, y2)

    def __repr__(self):
        prefix = 'polygon'

        if self.static:
            prefix = 'static_polygon'

        if self._cosmetic:
            prefix = 'cosmetic_polygon'

        return prefix + ': center(' + str(self.body.position.x) + ',' + str(self.body.position.y) + ')'
