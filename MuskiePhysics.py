# The idea here is to provide an interface to pymunk that is similar to Processing in Calico,
# but also exposing the more interesting features that Calico Graphics does not, such as pins
# and joints.

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

    def __init__(self):
        # How to create a rectangular shape in pymunk that matches the
        # bounding box of the text in pygame?
        #
        # pymunk.Poly.create_box(body, size_tuple, radius)
        #
        # This creates the shape to go with a body

        # How to draw the shapes rotated to match the physics rotation?
        pass


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


def ball(x, y, radius, mass, static=False):
    # What is the shape that's returned?  To do anything
    # else with this object, I probably need to wrap it
    # in an object of my creation that knows how to draw
    # the shape in pygame and can allow color changes, etc.
    #
    # That shape should get added to a list of shapes in
    # the simulation for drawing purposes, along with
    # being returned to the user so they can further
    # modify the shape.
    ball = Ball(x, y, radius, mass, static)
    shapes.append(ball)

    return ball


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


