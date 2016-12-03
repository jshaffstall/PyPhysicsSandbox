import pygame
import math

from .box import Box


class Text(Box):
    def __init__(self, space, x, y, caption, font_name, font_size, mass, static):
        font = pygame.font.SysFont(font_name, font_size)
        width, height = font.size(caption)
        height -= font.get_ascent()

        self.x = x
        self.y = y
        self.caption = caption

        box_x = x + width / 2
        box_y = y + height / 2

        super().__init__(space, box_x, box_y, width, height, 3, mass, static)

        self.label = font.render(self.caption, True, self.color)

    def _draw(self, screen):
        degrees = math.degrees(self.body.angle)
        rotated = pygame.transform.rotate(self.label, -degrees)

        size = rotated.get_rect()
        screen.blit(rotated, (self.body.position.x-(size.width/2), self.body.position.y-(size.height/2)))
