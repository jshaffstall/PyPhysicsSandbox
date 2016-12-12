import pygame
import pymunk

from .base_shape import BaseShape
from .util import to_pygame


class Ball(BaseShape):
    def __init__(self, space, x, y, radius, mass, static, cosmetic=False):
        if not cosmetic:
            moment = pymunk.moment_for_circle(mass, 0, radius)

            if static:
                self.body = pymunk.Body(mass, moment, pymunk.Body.STATIC)
            else:
                self.body = pymunk.Body(mass, moment)

            self.body.position = x, y
            self.shape = pymunk.Circle(self.body, radius)
            space.add(self.body, self.shape)

        self.static = static
        self._draw_radius_line = False
        self._x = x
        self._y = y
        self._radius = radius

        super().__init__(cosmetic)

    def _draw(self, screen):
        if self._cosmetic:
            p = (self._x, self._y)
        else:
            p = to_pygame(self.body.position)

        pygame.draw.circle(screen, self.color, p, int(self._radius), 0)

        if self.draw_radius_line:
            if self._cosmetic:
                p2 = (self._x+self._radius, self._y)
            else:
                circle_edge = self.body.position + pymunk.Vec2d(self.shape.radius, 0).rotated(self.body.angle)
                p2 = to_pygame(circle_edge)

            pygame.draw.lines(screen, pygame.Color('black'), False, [p, p2], 1)

    def _pin_points(self):
        x1 = self.body.position.x - self.shape.radius
        y1 = self.body.position.y
        x2 = self.body.position.x + self.shape.radius
        y2 = y1

        return (x1, y1), (x2, y2)

    def __repr__(self):
        prefix = 'ball'

        if self.static:
            prefix = 'static_ball'

        if self._cosmetic:
            prefix = 'cosmetic_ball'

        return prefix+': p(' + str(self.body.position.x) + ',' + str(self.body.position.y) + '), radius: ' + \
            str(self.shape.radius)

    @property
    def draw_radius_line(self):
        return self._draw_radius_line

    @draw_radius_line.setter
    def draw_radius_line(self, value):
        if type(value) == bool:
            self._draw_radius_line = value
        else:
            print("draw_radius_line value must be a True or False")
