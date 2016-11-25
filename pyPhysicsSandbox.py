# The idea here is to provide an interface to pymunk that is similar to Processing in Calico,
# but also exposing the more interesting features that Calico Graphics does not, such as pins
# and joints.
#
# Dependencies
#
#   pymunk http://www.pymunk.org/en/latest/
#   pygame http://www.pygame.org
#   py2d   http://sseemayer.github.io/Py2D  Must use version in github that has Python 3 compatibility

# TODO: Need to allow tying two objects together so they move as one

from pygame import Color
from py2d.Math.Polygon import *

import pygame
import pymunk
import math

pygame.init()

space = pymunk.Space()
win_title = "Untitled"
win_width = 500
win_height = 500
observer = None
pressed = False

shapes = []

class BaseShape:
    _color = Color('black')
    _wrap = False
    active = True

    def hit(self, x, y):
        self.body.apply_impulse_at_world_point((x,y))

    @property
    def elasticity(self):
        if type(self.shape) is list:
            return self.shape[0].elasticity

        return self.shape.elasticity

    @elasticity.setter
    def elasticity(self, value):
        if type(value) == float:
            if type(self.shape) is list:
                for shape in self.shape:
                    shape.elasticity = value
            else:
                self.shape.elasticity = value
        else:
            print("Elasticity value must be a floating point value")

    @property
    def friction(self):
        if type(self.shape) is list:
            return self.shape[0].friction

        return self.shape.friction

    @friction.setter
    def friction(self, value):
        if type(value) == float:
            if type(self.shape) is list:
                for shape in self.shape:
                    shape.friction = value
            else:
                self.shape.friction = value
        else:
            print("Friction value must be a floating point value")

    @property
    def wrap(self):
        return self._wrap

    @wrap.setter
    def wrap(self, value):
        if type(value) == bool:
            self._wrap = value
        else:
            print("Wrap value must be a bool value")

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if type(value) == Color:
            self._color = value
        else:
            print("Color value must be a Color instance")


class Ball(BaseShape):
    def __init__(self, x, y, radius, mass, static):
        moment = pymunk.moment_for_circle(mass, 0, radius)

        if static:
            self.body = pymunk.Body(mass, moment, pymunk.Body.STATIC)
        else:
            self.body = pymunk.Body(mass, moment)

        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius)
        self.elasticity = 0.90
        self.friction = 0.6
        space.add(self.body, self.shape)

    def draw(self, screen):
        p = to_pygame(self.body.position)
        pygame.draw.circle(screen, self.color, p, int(self.shape.radius), 0)


class Box(BaseShape):
    def __init__(self, x, y, width, height, radius, mass, static):
        moment = pymunk.moment_for_box(mass, (width, height))

        if static:
            self.body = pymunk.Body(mass, moment, pymunk.Body.STATIC)
        else:
            self.body = pymunk.Body(mass, moment)

        self.body.position = x, y
        self.shape = pymunk.Poly.create_box(self.body, (width, height), radius)
        self.elasticity = 0.9
        self.friction = 0.6
        space.add(self.body, self.shape)
        self.width = width
        self.height = height
        self.radius = radius

    def draw(self, screen):
        ps = [self.body.local_to_world(v) for v in self.shape.get_vertices()]
        ps += [ps[0]]

        pygame.draw.polygon(screen, self.color, ps)
        pygame.draw.lines(screen, self.color, False, ps, self.radius)


class Text(Box):
    def __init__(self, x, y, caption, font_name, font_size, mass, static):
        font = pygame.font.SysFont(font_name, font_size)
        width, height = font.size(caption)
        height -= font.get_ascent()

        self.x = x
        self.y = y
        self.caption = caption
        self.label = font.render(self.caption, True, self.color)

        box_x = x + width / 2
        box_y = y + height / 2

        super(Text,self).__init__(box_x, box_y, width, height, 3, mass, static)

    def draw(self, screen):
        body_angle = self.body.angle
        degrees = body_angle * 180 / math.pi
        rotated = pygame.transform.rotate(self.label, -degrees)

        size = rotated.get_rect()
        screen.blit(rotated, (self.body.position.x-(size.width/2), self.body.position.y-(size.height/2)))


class Poly(BaseShape):
    def __init__(self, x, y, vertices, radius, mass, static):
        moment = pymunk.moment_for_poly(mass, vertices, (0, 0), radius)

        if static:
            self.body = pymunk.Body(mass, moment, pymunk.Body.STATIC)
        else:
            self.body = pymunk.Body(mass, moment)

        self.body.position = x, y

        temp = Polygon.from_tuples(vertices)
        polys = Polygon.convex_decompose(temp)

        shapes = []

        for poly in polys:
            shapes.append(pymunk.Poly(self.body, poly.as_tuple_list(), None, radius))

        self.shape = shapes
        self.elasticity = 0.9
        self.friction = 0.6
        space.add(self.body, self.shape)
        self.radius = radius

    def draw(self, screen):
        for shape in self.shape:
            ps = [self.body.local_to_world(v) for v in shape.get_vertices()]

            pygame.draw.polygon(screen, self.color, ps)


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


def set_observer(hook):
    global observer

    observer = hook


def gravity(x, y):
    space.gravity = (x, y)


def mouse_pressed ():
    global pressed

    if not pressed and pygame.mouse.get_pressed()[0]:
        pressed = True
        return True

    if pressed and not pygame.mouse.get_pressed()[0]:
        pressed = False

    return False


def static_ball(p, radius, mass=1):
    return ball(p, radius, mass, True)


def ball(p, radius, mass=1, static=False):
    ball = Ball(p[0], p[1], radius, mass, static)
    shapes.append(ball)

    return ball


def static_box(p, width, height, mass=1):
    return box(p, width, height, mass, True)


def box(p, width, height, mass=1, static=False):
    # Polygons expect x,y to be the center point
    x = p[0] + width/2
    y = p[1] + height/2

    box = Box(x, y, width, height, 0, mass, static)
    shapes.append(box)

    return box


def static_rounded_box(p, width, height, radius, mass=1):
    return rounded_box(p, width, height, radius, mass, True)


def rounded_box(p, width, height, radius, mass=1, static=False):
    # Polygons expect x,y to be the center point
    x = p[0] + width/2
    y = p[1] + height/2

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


def static_text(p, caption, mass=1):
    return text(p, caption, mass, True)


def text(p, caption, mass=1, static=False):
    text = Text(p[0], p[1], caption, "Arial", 12, mass, static)
    shapes.append(text)

    return text


def static_text_with_font(p, caption, font, size, mass=1):
    return text_with_font(p, caption, font, size, mass, True)


def text_with_font(p, caption, font, size, mass=1, static=False):
    text = Text(p[0], p[1], caption, font, size, mass, static)
    shapes.append(text)

    return text


def run(do_physics=True):
    screen = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption(win_title)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if observer:
            observer ()

        screen.fill((255, 255, 255))

        # Should automatically remove any shapes that are
        # far enough below the bottom edge of the window
        # that they won't be involved in anything visible
        shapes_to_remove = []
        for shape in shapes:
            if shape.body.position.y > win_height*2:
                shapes_to_remove.append(shape)

        for shape in shapes_to_remove:
            shape.active = False
            space.remove(shape.shape, shape.body)
            shapes.remove(shape)

        # Also adjust positions for any shapes that are supposed
        # to wrap and have gone off an edge of the screen.
        for shape in shapes:
            if shape.wrap:
                if shape.body.position.x < 0:
                    shape.body.position = (win_width-1, shape.body.position.y)

                if shape.body.position.x >= win_width:
                    shape.body.position = (0, shape.body.position.y)

                if shape.body.position.y < 0:
                    shape.body.position = (shape.body.position.x, win_height-1)

                if shape.body.position.y >= win_height:
                    shape.body.position = (shape.body.position.x, 0)

        # Now draw the shapes that are left
        for shape in shapes:
            shape.draw(screen)

        if do_physics:
            space.step(1/50.0)

        pygame.display.flip()
        clock.tick(50)

    pygame.quit()


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

