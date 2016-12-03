import pygame
import pymunk

from .base_shape import BaseShape


class Ball(BaseShape):
    _draw_radius_line = False

    def __init__(self, space, x, y, radius, mass, static):
        moment = pymunk.moment_for_circle(mass, 0, radius)

        if static:
            self.body = pymunk.Body(mass, moment, pymunk.Body.STATIC)
        else:
            self.body = pymunk.Body(mass, moment)

        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius)

        super().__init__()

        space.add(self.body, self.shape)

    def _draw(self, screen):
        p = self.to_pygame(self.body.position)
        pygame.draw.circle(screen, self.color, p, int(self.shape.radius), 0)

        if self.draw_radius_line:
            circle_edge = self.body.position + pymunk.Vec2d(self.shape.radius, 0).rotated(self.body.angle)
            p2 = self.to_pygame(circle_edge)
            pygame.draw.lines(screen, pygame.Color('black'), False, [p, p2], 1)

    @property
    def draw_radius_line(self):
        return self._draw_radius_line

    @draw_radius_line.setter
    def draw_radius_line(self, value):
        if type(value) == bool:
            self._draw_radius_line = value
        else:
            print("draw_radius_line value must be a True or False")
