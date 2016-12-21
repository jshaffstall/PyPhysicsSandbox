import pygame
import pymunk
import math

from .box_shape import Box
from .base_shape import BaseShape


class Text(Box):
    def __init__(self, space, x, y, caption, font_name, font_size, mass, static, cosmetic=False):
        self.font = pygame.font.SysFont(font_name, font_size)
        width, height = self.font.size(caption)
        height -= self.font.get_ascent()

        self.caption = caption
        self.space = space
        self.static = static

        box_x = x + width / 2
        box_y = y + height / 2
        self._x = box_x
        self._y = box_y

        super().__init__(space, box_x, box_y, width, height, 3, mass, static, cosmetic)

        self.label = self.font.render(self.caption, True, self.color)

    def _draw(self, screen):
        degrees = self.angle
        rotated = pygame.transform.rotate(self.label, degrees)

        size = rotated.get_rect()
        screen.blit(rotated, (self.position.x-(size.width/2), self.position.y-(size.height/2)))

    def __repr__(self):
        prefix = 'box'

        if self.static:
            prefix = 'static_box'

        if self._cosmetic:
            prefix = 'cosmetic_box'

        return prefix+': p(' + str(self.position[0]) + ',' + str(self.position[1]) + '), caption: ' + self.caption + \
                        ', angle: ' + str(self.angle)

    @BaseShape.color.setter
    def color(self, value):
        BaseShape.color.fset(self, value)
        self.label = self.font.render(self.caption, True, self.color)

    @property
    def text(self):
        return self.caption

    @text.setter
    def text(self, value):
        if type(value) == str:
            self.caption = value
            self.label = self.font.render(self.caption, True, self.color)

            if not self._cosmetic:
                width, height = self.font.size(value)
                height -= self.font.get_ascent()

                moment = pymunk.moment_for_box(self.body.mass, (width, height))

                if self.static:
                    body = pymunk.Body(self.body.mass, moment, pymunk.Body.STATIC)
                else:
                    body = pymunk.Body(self.body.mass, moment)

                body.position = self.position
                shape = pymunk.Poly.create_box(self.body, (width, height), self.radius)
                self.width = width
                self.height = height

                self.space.remove(self.body, self.shape)
                self.body = body
                self.shape = shape
                self.space.add(self.body, self.shape)
        else:
            print("Text value must be a string")

