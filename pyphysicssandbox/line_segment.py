import pygame
import pymunk

from .base_shape import BaseShape


class Line(BaseShape):
    def __init__(self, space, p1, p2, thickness, mass, static, cosmetic=False):
        x = (p1[0] + p2[0]) / 2
        y = (p1[1] + p2[1]) / 2

        if not cosmetic:
            moment = pymunk.moment_for_segment(mass, (p1[0]-x, p1[1]-y), (p2[0]-x, p2[1]-y), thickness)

            if static:
                self.body = pymunk.Body(mass, moment, pymunk.Body.STATIC)
            else:
                self.body = pymunk.Body(mass, moment)

            self.body.position = x, y
            self.shape = pymunk.Segment(self.body, (p1[0]-x, p1[1]-y), (p2[0]-x, p2[1]-y), thickness)
            space.add(self.body, self.shape)

        self.radius = thickness
        self.static = static
        self._p1 = p1
        self._p2 = p2
        self._x = x;
        self._y = y

        super().__init__(cosmetic)

    def _draw(self, screen):
        if self._cosmetic:
            p1 = self._p1
            p2 = self._p2
        else:
            p1 = self.body.local_to_world(self.shape.a)
            p2 = self.body.local_to_world(self.shape.b)

        pygame.draw.line(screen, self.color, p1, p2, self.radius)

    def _pin_points(self):
        p1 = self.body.local_to_world(self.shape.a)
        p2 = self.body.local_to_world(self.shape.b)

        return p1, p2

    def __repr__(self):
        prefix = 'line'

        if self.static:
            prefix = 'static_line'

        if self._cosmetic:
            prefix = 'cosmetic_line'

        p1 = self.body.local_to_world(self.shape.a)
        p2 = self.body.local_to_world(self.shape.b)

        return prefix + ': p1(' + str(p1.x) + ',' + str(p1.y) + '), p2(' + str(p2.x) + ',' + str(p2.y) + ')'



