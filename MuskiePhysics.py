# The idea here is to provide an interface to pymunk that is similar to Processing in Calico,
# but also exposing the more interesting features that Calico Graphics does not, such as pins
# and joints.

# TODO: Need to allow tying two objects together so they move as one

from pygame import Color

import sys
import pygame
import pymunk

space = pymunk.Space()
win_title = "Untitled"
win_width = 500
win_height = 500

shapes = []


class Ball:
    color = Color('black')

    def __init__(self, x, y, radius, mass, static):
        moment = pymunk.moment_for_circle(mass, 0, radius)

        if static:
            body = pymunk.Body(mass, moment, pymunk.Body.STATIC)
        else:
            body = pymunk.Body(mass, moment)

        body.position = x, y
        self.shape = pymunk.Circle(body, radius)
        space.add(body, self.shape)

    def draw(self, screen):
        p = to_pygame(self.shape.body.position)
        pygame.draw.circle(screen, self.color, p, int(self.shape.radius), 0)

class Text:
    color = Color('black')

    def __init__(self, x, y, text, static):
        # How to create a rectangular shape in pymunk that matches the
        # bounding box of the text in pygame?
        #
        # pymunk.Poly.create_box(body, size_tuple, radius)
        #
        # This creates the shape to go with a body

        pass

    def draw(self, screen):
        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        # myfont = pygame.font.SysFont("monospace", 15)
        #
        # # render text
        # label = myfont.render("Some text!", 1, (255, 255, 0))
        # screen.blit(label, (100, 100))

        # How to draw the shapes rotated to match the physics rotation?
        p = to_pygame(self.shape.body.position)
        pygame.draw.circle(screen, self.color, p, int(self.shape.radius), 0)


class Box:
    color = Color('black')

    def __init__(self, x, y, width, height, radius, mass, static):
        moment = pymunk.moment_for_box(mass, (width, height))

        if static:
            body = pymunk.Body(mass, moment, pymunk.Body.STATIC)
        else:
            body = pymunk.Body(mass, moment)

        body.position = x, y
        self.shape = pymunk.Poly.create_box(body, (width, height), radius)
        space.add(body, self.shape)
        self.width = width
        self.height = height

    def draw(self, screen):
        p = to_pygame(self.shape.body.position)


def to_pygame(p):
    # Converts pymunk body position into pygame coordinate tuple
    return int(p.x), int(p.y)


def window(title, width, height):
    global win_title
    global win_width
    global win_height

    win_title = title
    win_width = width
    win_height = height


def gravity(x, y):
    space.gravity = (x, y)


def ball(x, y, radius, mass=1, static=False):
    ball = Ball(x, y, radius, mass, static)
    shapes.append(ball)

    return ball


def box(x, y, width, height, mass=1, static=False):
    box = Box(x, y, width, height, 0, mass, static)
    shapes.append(box)

    return box


def rounded_box(x, y, width, height, radius, mass=1, static=False):
    box = Box(x, y, width, height, radius, mass, static)
    shapes.append(box)

    return box


def run():
    pygame.init()
    screen = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption(win_title)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        screen.fill((255, 255, 255))

        # Should automatically remove any shapes that are
        # far enough below the bottom edge of the window
        # that they won't be involved in anything visible
        shapes_to_remove = []
        for shape in shapes:
            if shape.shape.body.position.y > win_height*2:
                shapes_to_remove.append(shape)

        for shape in shapes_to_remove:
            space.remove(shape.shape, shape.shape.body)
            shapes.remove(shape)

        # Now draw the shapes that are left
        for shape in shapes:
            shape.draw(screen)

        space.step(1/50.0)

        pygame.display.flip()
        clock.tick(50)


