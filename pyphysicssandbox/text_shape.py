import pygame
import pymunk
import math

from .box_shape import Box


class Text(Box):
    def __init__(self, space, x, y, caption, font_name, font_size, mass, static):
        self.font = pygame.font.SysFont(font_name, font_size)
        width, height = self.font.size(caption)
        height -= self.font.get_ascent()

        self.x = x
        self.y = y
        self.caption = caption
        self.space = space
        self.static = static

        box_x = x + width / 2
        box_y = y + height / 2

        super().__init__(space, box_x, box_y, width, height, 3, mass, static)

        self.label = self.font.render(self.caption, True, self.color)

    def _draw(self, screen):
        degrees = math.degrees(self.body.angle)
        rotated = pygame.transform.rotate(self.label, -degrees)

        size = rotated.get_rect()
        screen.blit(rotated, (self.body.position.x-(size.width/2), self.body.position.y-(size.height/2)))

    @property
    def text(self):
        return self.caption

    @text.setter
    def text(self, value):
        if type(value) == str:
            self.caption = value
            width, height = self.font.size(value)
            height -= self.font.get_ascent()

            box_x = self.x + width / 2
            box_y = self.y + height / 2

            moment = pymunk.moment_for_box(self.body.mass, (width, height))

            if self.static:
                body = pymunk.Body(self.body.mass, moment, pymunk.Body.STATIC)
            else:
                body = pymunk.Body(self.body.mass, moment)

            body.position = box_x, box_y
            shape = pymunk.Poly.create_box(self.body, (width, height), self.radius)
            self.width = width
            self.height = height

            self.space.remove(self.body, self.shape)
            self.body = body
            self.shape = shape
            self.space.add(self.body, self.shape)

            self.label = self.font.render(self.caption, True, self.color)
        else:
            print("Text value must be a string")

