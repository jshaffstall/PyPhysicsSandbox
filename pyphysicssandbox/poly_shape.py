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
        self.static = static

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

        return prefix + ': center(' + str(self.body.position.x) + ',' + str(self.body.position.y) + ')'

    """
    To see if a point is inside the polygon, use something like this:
    (Modify this to be Python and work with an array of vertice tuples)

    int pnpoly(int nvert, float *vertx, float *verty, float testx, float testy)
    {
      int i, j, c = 0;
      for (i = 0, j = nvert-1; i < nvert; j = i++) {
        if ( ((verty[i]>testy) != (verty[j]>testy)) &&
         (testx < (vertx[j]-vertx[i]) * (testy-verty[i]) / (verty[j]-verty[i]) + vertx[i]) )
           c = !c;
      }
      return c;
    }
    """
