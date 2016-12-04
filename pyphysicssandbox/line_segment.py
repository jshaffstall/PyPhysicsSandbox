import pygame
import pymunk

from .base_shape import BaseShape


class Line(BaseShape):
    def __init__(self, space, p1, p2, thickness, mass, static):
        x = (p1[0]+p2[0])/2
        y = (p1[1]+p2[1])/2

        moment = pymunk.moment_for_segment(mass, (p1[0]-x, p1[1]-y), (p2[0]-x, p2[1]-y), thickness)

        if static:
            self.body = pymunk.Body(mass, moment, pymunk.Body.STATIC)
        else:
            self.body = pymunk.Body(mass, moment)

        self.body.position = x, y
        self.shape = pymunk.Segment(self.body, (p1[0]-x, p1[1]-y), (p2[0]-x, p2[1]-y), thickness)
        self.radius = thickness
        self.static = static

        super().__init__()

        space.add(self.body, self.shape)

    def _draw(self, screen):
        p1 = self.body.local_to_world(self.shape.a)
        p2 = self.body.local_to_world(self.shape.b)

        pygame.draw.line(screen, self.color, p1, p2, self.radius)

    def __repr__(self):
        prefix = 'line'

        if self.static:
            prefix = 'static_line'

        p1 = self.body.local_to_world(self.shape.a)
        p2 = self.body.local_to_world(self.shape.b)

        return prefix + ': p1(' + str(p1.x) + ',' + str(p1.y) + '), p2(' + str(p2.x) + ',' + str(p2.y) + ')'



