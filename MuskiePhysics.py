# The idea here is to provide an interface to pymunk that is similar to Processing in Calico,
# but also exposing the more interesting features that Calico Graphics does not, such as pins
# and joints.
#
# Dependencies
#
#   pymunk http://www.pymunk.org/en/latest/
#   shapely http://toblerity.org/shapely/project.html#installation

# TODO: Need to allow tying two objects together so they move as one
# TODO: Expose friction and set some reasonable default

from pygame import Color

import sys
import pygame
import pymunk

space = pymunk.Space()
win_title = "Untitled"
win_width = 500
win_height = 500
frame_hook = None

shapes = []


class Ball:
    color = Color('black')
    wrap = False

    def __init__(self, x, y, radius, mass, static):
        moment = pymunk.moment_for_circle(mass, 0, radius)

        if static:
            body = pymunk.Body(mass, moment, pymunk.Body.STATIC)
        else:
            body = pymunk.Body(mass, moment)

        body.position = x, y
        self.shape = pymunk.Circle(body, radius)
        self.shape.elasticity = 0.90
        space.add(body, self.shape)

    def draw(self, screen):
        p = to_pygame(self.shape.body.position)
        pygame.draw.circle(screen, self.color, p, int(self.shape.radius), 0)

    @property
    def elasticity(self):
        return self.shape.elasticity

    @elasticity.setter
    def elasticity(self, value):
        if type(value) == float:
            self.shape.elasticity=value
        else:
            print("Elasticity value must be a floating point value")

class Text:
    color = Color('black')
    wrap = False

    def __init__(self, x, y, text, static):
        # How to create a rectangular shape in pymunk that matches the
        # bounding box of the text in pygame?
        #
        # pymunk.Poly.create_box(body, size_tuple, radius)
        #
        # This creates the shape to go with a body
        self.shape.elasticity = 0.9

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

    @property
    def elasticity(self):
        return self.shape.elasticity

    @elasticity.setter
    def elasticity(self, value):
        if type(value) == float:
            self.shape.elasticity = value
        else:
            print("Elasticity value must be a floating point value")


class Box:
    color = Color('black')
    wrap = False

    def __init__(self, x, y, width, height, radius, mass, static):
        moment = pymunk.moment_for_box(mass, (width, height))

        if static:
            body = pymunk.Body(mass, moment, pymunk.Body.STATIC)
        else:
            body = pymunk.Body(mass, moment)

        body.position = x, y
        self.shape = pymunk.Poly.create_box(body, (width, height), radius)
        self.shape.elasticity = 0.9
        space.add(body, self.shape)
        self.width = width
        self.height = height
        self.radius = radius

    def draw(self, screen):
        ps = [self.shape.body.local_to_world(v) for v in self.shape.get_vertices()]
        ps += [ps[0]]

        pygame.draw.polygon(screen, self.color, ps)
        pygame.draw.lines(screen, self.color, False, ps, self.radius)

    @property
    def elasticity(self):
        return self.shape.elasticity

    @elasticity.setter
    def elasticity(self, value):
        if type(value) == float:
            self.shape.elasticity=value
        else:
            print("Elasticity value must be a floating point value")


class Poly:
    color = Color('black')
    wrap = False

    def __init__(self, x, y, vertices, radius, mass, static):
        moment = pymunk.moment_for_poly(mass, vertices, (0, 0), radius)

        if static:
            body = pymunk.Body(mass, moment, pymunk.Body.STATIC)
        else:
            body = pymunk.Body(mass, moment)

        body.position = x, y
        self.shape = pymunk.Poly(body, vertices, None, radius)
        self.shape.elasticity = 0.9
        space.add(body, self.shape)
        self.radius = radius

    def draw(self, screen):
        ps = [self.shape.body.local_to_world(v) for v in self.shape.get_vertices()]
        ps += [ps[0]]

        pygame.draw.polygon(screen, self.color, ps)
        pygame.draw.lines(screen, self.color, False, ps, self.radius)

    @property
    def elasticity(self):
        return self.shape.elasticity

    @elasticity.setter
    def elasticity(self, value):
        if type(value) == float:
            self.shape.elasticity=value
        else:
            print("Elasticity value must be a floating point value")


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


def step_function(hook):
    global frame_hook

    frame_hook = hook


def gravity(x, y):
    space.gravity = (x, y)


def static_ball(x, y, radius, mass=1):
    return ball(x, y, radius, mass, True)


def ball(x, y, radius, mass=1, static=False):
    ball = Ball(x, y, radius, mass, static)
    shapes.append(ball)

    return ball


def static_box(x, y, width, height, mass=1):
    return box(x, y, width, height, mass, True)


def box(x, y, width, height, mass=1, static=False):
    # Polygons expect x,y to be the center point
    x += width/2
    y += height/2

    box = Box(x, y, width, height, 0, mass, static)
    shapes.append(box)

    return box


def static_rounded_box(x, y, width, height, radius, mass=1):
    return rounded_box(x, y, width, height, radius, mass, True)


def rounded_box(x, y, width, height, radius, mass=1, static=False):
    # Polygons expect x,y to be the center point
    x += width/2
    y += height/2

    box = Box(x, y, width, height, radius, mass, static)
    shapes.append(box)

    return box


def static_poly(vertices, mass=1):
    return poly(vertices, mass, True)


def poly(vertices, mass=1, static=False):
    x, y = poly_centroid(vertices)

    vertices = [(v[0]-x, v[1]-y) for v in vertices]
    poly = Poly(x, y, vertices, 0, mass, static)
    shapes.append(poly)

    return poly


def static_triangle(p1, p2, p3, mass=1):
    return triangle(p1, p2, p3, mass, True)


def triangle(p1, p2, p3, mass=1, static=False):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    x = (x1+x2+x3)/3
    y = (y1+y2+y3)/3
    vertices = ((x1-x, y1-y), (x2-x, y2-y), (x3-x, y3-y))

    triangle = Poly(x, y, vertices, 0, mass, static)
    shapes.append(triangle)

    return triangle


def run():
    pygame.init()
    screen = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption(win_title)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        if frame_hook:
            frame_hook ()

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

        # Also adjust positions for any shapes that are supposed
        # to wrap and have gone off an edge of the screen.
        for shape in shapes:
            if shape.wrap:
                if shape.shape.body.position.x < 0:
                    shape.shape.body.position = (win_width-1, shape.shape.body.position.y)

                if shape.shape.body.position.x >= win_width:
                    shape.shape.body.position = (0, shape.shape.body.position.y)

                if shape.shape.body.position.y < 0:
                    shape.shape.body.position = (shape.shape.body.position.x, win_height-1)

                if shape.shape.body.position.y >= win_height:
                    shape.shape.body.position = (shape.shape.body.position.x, 0)

        # Now draw the shapes that are left
        for shape in shapes:
            shape.draw(screen)

        space.step(1/50.0)

        pygame.display.flip()
        clock.tick(50)


def poly_centroid(vertices):
    centroid = [0, 0]
    area = 0.0

    for i in range(len(vertices)):
        x0, y0 = vertices[i]

        if i == len(vertices)-1:
            x1, y1 = vertices[0]
        else:
            x1, y1 = vertices[i+1]

        a = (x0*y1 - x1*y0)
        area += a
        centroid[0] += (x0 + x1) * a
        centroid[1] += (y0 + y1) * a

    area *= 0.5
    centroid[0] /= (6.0 * area)
    centroid[1] /= (6.0 * area)

    return centroid

