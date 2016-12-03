import pygame
import pymunk

from .base_shape import BaseShape
from py2d.Math.Polygon import *


class Poly(BaseShape):
    def __init__(self, space, x, y, vertices, radius, mass, static):
        moment = pymunk.moment_for_poly(mass, vertices, (0, 0), radius)

        if static:
            self.body = pymunk.Body(mass, moment, pymunk.Body.STATIC)
        else:
            self.body = pymunk.Body(mass, moment)

        self.body.position = x, y

        temp = Polygon.from_tuples(vertices)
        polys = Polygon.convex_decompose(temp)

        shapes = []

        for poly in polys:
            shapes.append(pymunk.Poly(self.body, poly.as_tuple_list(), None, radius))

        self.shape = shapes
        self.radius = radius
        super().__init__()

        space.add(self.body, self.shape)

    def _draw(self, screen):
        for shape in self.shape:
            ps = [self.body.local_to_world(v) for v in shape.get_vertices()]

            pygame.draw.polygon(screen, self.color, ps)
