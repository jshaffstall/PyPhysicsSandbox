# The idea here is to provide an interface to pymunk that is similar to Processing in Calico,
# but also exposing the more interesting features that Calico Graphics does not, such as pins
# and joints.

import sys
import pygame
import pymunk

space = pymunk.Space()

def to_pygame(p):
    # pymunk origin is lower left, pygame origin is upper left
    # this converts pymunk coordinates to pygame coordinates
    # for drawing shapes.
    return int(p.x), int(-p.y+win_height)

def window(title, width, height):
    global win_title
    global win_width
    global win_height

    win_title = title
    win_width = width
    win_height = height

def gravity (x, y):
    space.gravity = (x, -y)

def ball (x, y, radius, mass):
    # What is the shape that's returned?  To do anything
    # else with this object, I probably need to wrap it
    # in an object of my creation that knows how to draw
    # the shape in pygame and can allow color changes, etc.
    #
    # That shape should get added to a list of shapes in
    # the simulation for drawing purposes, along with
    # being returned to the user so they can further
    # modify the shape.
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = x, y
    shape = pymunk.Circle(body, radius)
    space.add(body, shape)
    return shape

def run():
    pygame.init()
    screen = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption(win_title)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

