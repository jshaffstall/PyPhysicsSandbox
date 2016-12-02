# The idea here is to provide an interface to pymunk that is similar to Processing in Calico,
# but also exposing the more interesting features that Calico Graphics does not, such as pins
# and joints.
#
# Dependencies
#
#   pymunk http://www.pymunk.org (can install this with pip)
#   pygame http://www.pygame.org (need a version of this that supports Python 3)
#   py2d   http://sseemayer.github.io/Py2D  Must use version in github that has Python 3 compatibility

# TODO: Need to allow tying two objects together so they move as one
# Specifically putting text inside of another object would be nice if I need to special case it

# TODO: create this as an open source library for distribution
# https://jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/

# TODO: create __repr__ functions in the shape classes to show info during debugging

# TODO: Expose motor's max torque

# TODO: Figure out how to do a slip gear

# TODO: look at difference between dynamic bodies and kinematic bodies.
# Implement kinematic bodies?  They're controlled by code and not by physics.  Useful
# for things like elevators and doors.

# TODO: allow damping and gravity to be specified for each body


from pygame import Color
from py2d.Math.Polygon import *

import pygame
import pymunk
import math

pygame.init()

space = pymunk.Space()
space.gravity = (0.0, 500.0)
space.damping = 0.95

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
    _visible = True

    def hit(self, x, y):
        self.body.apply_impulse_at_world_point((x,y))

    def has_own_body(self):
        return True

    def draw(self, screen):
        if self.visible:
            self._draw(screen)

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
            print("Wrap value must be True or False")

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        if type(value) == bool:
            self._visible = value
        else:
            print("Visible value must be True or False")

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if type(value) == Color:
            self._color = value
        else:
            print("Color value must be a Color instance")

    @property
    def group(self):
        if type(self.shape) is list:
            return self.shape[0].filter.group

        return self.shape.filter.group

    @group.setter
    def group(self, value):
        if type(value) == int:
            if type(self.shape) is list:
                for shape in self.shape:
                    shape.filter = pymunk.ShapeFilter(group=value)
            else:
                self.shape.filter = pymunk.ShapeFilter(group=value)
        else:
            print("Group value must be an integer")


class Ball(BaseShape):
    _draw_radius_line = False

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

    def _draw(self, screen):
        p = to_pygame(self.body.position)
        pygame.draw.circle(screen, self.color, p, int(self.shape.radius), 0)

        if self.draw_radius_line:
            circle_edge = self.body.position + pymunk.Vec2d(self.shape.radius, 0).rotated(self.body.angle)
            p2 = to_pygame(circle_edge)
            pygame.draw.lines(screen, Color('black'), False, [p, p2], 1)

    @property
    def draw_radius_line(self):
        return self._draw_radius_line

    @draw_radius_line.setter
    def draw_radius_line(self, value):
        if type(value) == bool:
            self._draw_radius_line = value
        else:
            print("draw_radius_line value must be a True or False")



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

    def _draw(self, screen):
        ps = [self.body.local_to_world(v) for v in self.shape.get_vertices()]
        ps += [ps[0]]

        pygame.draw.polygon(screen, self.color, ps)
        pygame.draw.lines(screen, self.color, False, ps, self.radius)


class Line(BaseShape):
    def __init__(self, p1, p2, thickness, mass, static):
        x = (p1[0]+p2[0])/2
        y = (p1[1]+p2[1])/2

        moment = pymunk.moment_for_segment(mass, (p1[0]-x, p1[1]-y), (p2[0]-x, p2[1]-y), thickness)

        if static:
            self.body = pymunk.Body(mass, moment, pymunk.Body.STATIC)
        else:
            self.body = pymunk.Body(mass, moment)

        self.body.position = x, y
        self.shape = pymunk.Segment(self.body, (p1[0]-x, p1[1]-y), (p2[0]-x, p2[1]-y), thickness)
        self.elasticity = 0.9
        self.friction = 0.6
        space.add(self.body, self.shape)
        self.radius = thickness

    def _draw(self, screen):
        p1 = self.body.local_to_world(self.shape.a)
        p2 = self.body.local_to_world(self.shape.b)

        pygame.draw.line(screen, self.color, p1, p2, self.radius)


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

    def _draw(self, screen):
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

    def _draw(self, screen):
        for shape in self.shape:
            ps = [self.body.local_to_world(v) for v in shape.get_vertices()]

            pygame.draw.polygon(screen, self.color, ps)


class PivotJoint(BaseShape):
    def __init__(self, x, y):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = x, y
        self.shape = []
        space.add(self.body)

    def connect(self, shape):
        join = pymunk.PivotJoint(shape.body, self.body, self.body.position)
        self.shape.append(join)
        space.add(join)

    def _draw(self, screen):
        p = to_pygame(self.body.position)
        pygame.draw.circle(screen, self.color, p, 5, 0)


class PinJoint(BaseShape):
    def __init__(self, p1, shape1, p2, shape2):
        # Associate the pin with the location of one of the bodies so
        # it is removed when that body is out of the simulation
        self.body = shape1.body

        ax = p1[0]-shape1.body.position.x
        ay = p1[1]-shape1.body.position.y
        bx = p2[0]-shape2.body.position.x
        by = p2[1]-shape2.body.position.y

        self.shape = pymunk.PinJoint(shape1.body, shape2.body, (ax, ay), (bx, by))
        space.add(self.shape)

    def has_own_body(self):
        return False
    
    def _draw(self, screen):
        p1 = self.shape.a.local_to_world(self.shape.anchor_a)
        p2 = self.shape.b.local_to_world(self.shape.anchor_b)

        pygame.draw.line(screen, self.color, p1, p2, 1)


class GearJoint(BaseShape):
    def __init__(self, shape1, shape2, angle=0):
        # Associate the gear joint with the location of one of the bodies so
        # it is removed when that body is out of the simulation
        self.body = shape1.body
        self.shape = pymunk.GearJoint(shape1.body, shape2.body, angle, 1)
        space.add(self.shape)

    def has_own_body(self):
        return False

    def _draw(self, screen):
        pass


class Motor(BaseShape):
    def __init__(self, shape1, speed):
        # Associate the motor with the location of one of the bodies so
        # it is removed when that body is out of the simulation
        self.body = shape1.body
        self.shape = pymunk.SimpleMotor(shape1.body, space.static_body, speed)
        space.add(self.shape)

    def has_own_body(self):
        return False

    def _draw(self, screen):
        p = to_pygame(self.body.position)
        radius = 10
        rect = pygame.Rect(p[0] - radius/2, p[1] - radius/2, radius, radius)

        pygame.draw.arc(screen, self.color, rect, 1, 6)

        if self.shape.rate > 0:
            pygame.draw.circle(screen, self.color, rect.topright, 2, 0)
        else:
            pygame.draw.circle(screen, self.color, rect.bottomright, 2, 0)


class RotarySpring(BaseShape):
    def __init__(self, shape1, shape2, angle, stiffness, damping):
        # Associate the joint with the location of one of the bodies so
        # it is removed when that body is out of the simulation
        self.body = shape1.body
        self.shape = pymunk.DampedRotarySpring(shape1.body, shape2.body, math.radians(angle), stiffness, damping)
        space.add(self.shape)

    def has_own_body(self):
        return False

    def _draw(self, screen):
        pass


# I couldn't get this to work the way I wanted, so needs more investigation
#
# class AngleLimitJoint(BaseShape):
#     def __init__(self, shape1, min_angle, max_angle):
#         # Associate the joint with the location of one of the bodies so
#         # it is removed when that body is out of the simulation
#         self.body = shape1.body
#         self.shape = pymunk.RotaryLimitJoint(shape1.body, space.static_body, math.radians(min_angle), math.radians(max_angle))
#         space.add(self.shape)
#
#     def has_own_body(self):
#         return False
#
#     def _draw(self, screen):
#         pass


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


def damping(v):
    """Sets the amount of velocity that all objects lose over time.
    This can be used to simulate air resistance.  Damping value
    defaults to 1.0.  Values less than 1.0 cause objects to lose
    velocity over time, values greater than 1.0 cause objects to
    gain velocity over time.

    :param v: The damping value
    :type v: float

    """
    space.damping = v


def mouse_pressed ():
    """Returns True if the mouse has been pressed this time step.
    The method ensures that you only get one True result for a given
    click and release of the mouse.

    :rtype: bool

    """
    global pressed

    if not pressed and pygame.mouse.get_pressed()[0]:
        pressed = True
        return True

    if pressed and not pygame.mouse.get_pressed()[0]:
        pressed = False

    return False


def static_ball(p, radius):
    """Creates a ball that remains fixed in place.

    :param p: The center point of the ball
    :type p: (int, int)
    :param radius: The radius of the ball
    :type radius: int
    :rtype: shape

    """
    return ball(p, radius, pymunk.inf, True)


def ball(p, radius, mass=1, static=False):
    """Creates a ball that reacts to gravity.

    :param p: The center point of the ball
    :type p: (int, int)
    :param radius: The radius of the ball
    :type radius: int
    :param mass: The mass of the shape (defaults to 1)
    :type mass: int
    :rtype: shape

    """
    ball = Ball(p[0], p[1], radius, mass, static)
    shapes.append(ball)

    return ball


def static_box(p, width, height):
    """Creates a box that remains fixed in place.

    :param p: The upper left corner of the box
    :type p: (int, int)
    :param width: The width of the box
    :type width: int
    :param height: The height of the box
    :type height: int
    :rtype: shape

    """
    return box(p, width, height, pymunk.inf, True)


def box(p, width, height, mass=1, static=False):
    """Creates a box that reacts to gravity.

    :param p: The upper left corner of the box
    :type p: (int, int)
    :param width: The width of the box
    :type width: int
    :param height: The height of the box
    :type height: int
    :param mass: The mass of the shape (defaults to 1)
    :type mass: int
    :rtype: shape

    """
    # Polygons expect x,y to be the center point
    x = p[0] + width/2
    y = p[1] + height/2

    box = Box(x, y, width, height, 0, mass, static)
    shapes.append(box)

    return box


def static_rounded_box(p, width, height, radius):
    """Creates a box with rounded corners that remains fixed in place.

    :param p: The upper left corner of the box
    :type p: (int, int)
    :param width: The width of the box
    :type width: int
    :param height: The height of the box
    :type height: int
    :param radius: The radius of the rounded corners
    :type radius: int
    :rtype: shape

    """
    return rounded_box(p, width, height, radius, pymunk.inf, True)


def rounded_box(p, width, height, radius, mass=1, static=False):
    """Creates a box with rounded corners that reacts to gravity.

    :param p: The upper left corner of the box
    :type p: (int, int)
    :param width: The width of the box
    :type width: int
    :param height: The height of the box
    :type height: int
    :param radius: The radius of the rounded corners
    :type radius: int
    :param mass: The mass of the shape (defaults to 1)
    :type mass: int
    :rtype: shape

    """
    # Polygons expect x,y to be the center point
    x = p[0] + width/2
    y = p[1] + height/2

    box = Box(x, y, width, height, radius, mass, static)
    shapes.append(box)

    return box


def static_poly(vertices):
    """Creates a polygon that remains fixed in place.

    :param vertices: A tuple of points on the polygon
    :type vertices: ((int, int), (int, int), ...)
    :rtype: shape

    """
    return poly(vertices, pymunk.inf, True)


def poly(vertices, mass=1, static=False):
    """Creates a polygon that reacts to gravity.

    :param vertices: A tuple of points on the polygon
    :type vertices: ((int, int), (int, int), ...)
    :param mass: The mass of the shape (defaults to 1)
    :type mass: int
    :rtype: shape

    """
    x, y = poly_centroid(vertices)

    vertices = [(v[0]-x, v[1]-y) for v in vertices]
    poly = Poly(x, y, vertices, 0, mass, static)
    shapes.append(poly)

    return poly


def static_triangle(p1, p2, p3):
    """Creates a triangle that remains fixed in place.

    :param p1: The first point of the triangle
    :type p1: (int, int)
    :param p2: The second point of the triangle
    :type p2: (int, int)
    :param p3: The third point of the triangle
    :type p3: (int, int)
    :rtype: shape

    """
    return triangle(p1, p2, p3, pymunk.inf, True)


def triangle(p1, p2, p3, mass=1, static=False):
    """Creates a triangle that reacts to gravity.

    :param p1: The first point of the triangle
    :type p1: (int, int)
    :param p2: The second point of the triangle
    :type p2: (int, int)
    :param p3: The third point of the triangle
    :type p3: (int, int)
    :param mass: The mass of the shape (defaults to 1)
    :type mass: int
    :rtype: shape

    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    x = (x1+x2+x3)/3
    y = (y1+y2+y3)/3
    vertices = ((x1-x, y1-y), (x2-x, y2-y), (x3-x, y3-y))

    triangle = Poly(x, y, vertices, 0, mass, static)
    shapes.append(triangle)

    return triangle


def static_text(p, caption):
    """Creates a text rectangle that remains fixed in place, using
    Arial 12 point font.

    :param p: The upper left corner of the text rectangle
    :type p: (int, int)
    :param caption: The text to display
    :type caption: string
    :rtype: shape

    """
    return text(p, caption, pymunk.inf, True)


def text(p, caption, mass=1, static=False):
    """Creates a text rectangle that reacts to gravity, using
    Arial 12 point font.

    :param p: The upper left corner of the text rectangle
    :type p: (int, int)
    :param caption: The text to display
    :type caption: string
    :param mass: The mass of the shape (defaults to 1)
    :type mass: int
    :rtype: shape

    """
    text = Text(p[0], p[1], caption, "Arial", 12, mass, static)
    shapes.append(text)

    return text


def static_text_with_font(p, caption, font, size):
    """Creates a text rectangle that remains fixed in place.

    :param p: The upper left corner of the text rectangle
    :type p: (int, int)
    :param caption: The text to display
    :type caption: string
    :param font: The font family to use
    :type font: string
    :param size: The point size of the font
    :type size: int
    :rtype: shape

    """
    return text_with_font(p, caption, font, size, pymunk.inf, True)


def text_with_font(p, caption, font, size, mass=1, static=False):
    """Creates a text rectangle that reacts to gravity.

    :param p: The upper left corner of the text rectangle
    :type p: (int, int)
    :param caption: The text to display
    :type caption: string
    :param font: The font family to use
    :type font: string
    :param size: The point size of the font
    :type size: int
    :param mass: The mass of the shape (defaults to 1)
    :type mass: int
    :rtype: shape

    """
    text = Text(p[0], p[1], caption, font, size, mass, static)
    shapes.append(text)

    return text


def static_line(p1, p2, thickness):
    """Creates a line segment that remains fixed in place.

    :param p1: The starting point of the line segement
    :type p1: (int, int)
    :param p2: The ending point of the line segement
    :type p2: (int, int)
    :param thickness: The thickness of the line segement
    :type thickness: int
    :rtype: shape

    """
    return line(p1, p2, thickness, pymunk.inf, True)


def line(p1, p2, thickness, mass=1, static=False):
    """Creates a line segment that will react to gravity.

    :param p1: The starting point of the line segement
    :type p1: (int, int)
    :param p2: The ending point of the line segement
    :type p2: (int, int)
    :param thickness: The thickness of the line segement
    :type thickness: int
    :param mass: The mass of the shape (defaults to 1)
    :type mass: int
    :rtype: shape

    """
    line = Line(p1, p2, thickness, mass, static)
    shapes.append(line)

    return line


def pivot(p):
    """Creates a pivot joint around which shapes can freely rotate.
    Shapes must be connected to the pivot using the connect method
    on the returned shape.  The pivot joint remains fixed in place.

    :param p: The point at which to place the pivot
    :type p: (int, int)
    :rtype: shape

    """
    pivot = PivotJoint(p[0], p[1])
    shapes.append(pivot)

    return pivot


def gear(shape1, shape2):
    """Connects two objects such that their rotations become the same.
    Can be used in conjunction with a motor on one shape to ensure the
    second shape rotates at the same speed as the first.

    :param shape1: The first shape to connect
    :type shape1: shape
    :param shape2: The second shape to connect
    :type shape2: shape
    :rtype: shape

    """
    gear = GearJoint(shape1, shape2)
    shapes.append(gear)

    return gear


def motor(shape1, speed=5):
    """Creates a constant rotation of the given shape around its
    center point.  The direction of rotation is controlled by the
    sign of the speed.  Positive speed is clockwise, negative speed
    is counter-clockwise.

    :param shape1: The shape to connect to the motor
    :type shape1: shape
    :param speed: The speed at which to rotate the shape
    :type speed: int
    :rtype: shape

    """
    motor = Motor(shape1, speed)
    shapes.append(motor)

    return motor


def pin(p1, shape1, p2, shape2):
    """Creates a connection between the shapes at the given positions.
    Those points on the shapes will remain that same distance apart,
    regardless of movement or rotation.

    :param p1: The point on the first shape
    :type p1: (int, int)
    :param shape1: The first shape to connect via the pin
    :type shape1: shape
    :param p2: The point on the second shape
    :type p2: (int, int)
    :param shape2: The second shape to connect via the pin
    :type shape2: shape
    :rtype: shape

    """
    pin = PinJoint(p1, shape1, p2, shape2)
    shapes.append(pin)

    return pin


def rotary_spring(shape1, shape2, angle, stiffness, damping):
    """Creates a spring that constrains the rotations of the given shapes.
    The angle between the two shapes prefers to be at the given angle, but
    may be varied by forces on the objects.  The spring will bring the objects
    back to the desired angle.  The initial positioning of the shapes is considered
    to be at an angle of 0.

    :param shape1: The first shape to connect via the spring
    :type shape1: shape
    :param shape2: The second shape to connect via the spring
    :type shape2: shape
    :param angle: The desired angle between the two objects
    :type angle: float
    :param stiffness: the spring constant (Young's modulus)
    :type stiffness: float
    :param damping: the softness of the spring damping
    :type damping: float
    :rtype: shape

    """
    spring = RotarySpring(shape1, shape2, angle, stiffness, damping)
    shapes.append(spring)

    return spring


# def limit_angle(shape, min_angle, max_angle):
#     limit = AngleLimitJoint(shape, min_angle, max_angle)
#     shapes.append(limit)
#
#     return limit


def run(do_physics=True):
    """Call this after you have created all your shapes to actually run the simulation.
    This function returns only when the user has closed the simulation window.

    Pass False to this method to do the drawing but not activate physics.
    Useful for getting the scene right before running the simulation.

    :param do_physics: Should physics be activated or not
    :type do_physics: bool
    """

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

            if type(shape.shape) is list:
                for s in shape.shape:
                    space.remove(s)
        
                if shape.has_own_body():
                    space.remove(shape.body)
            else:
                if shape.has_own_body():
                    space.remove(shape.shape, shape.body)
                else:
                    space.remove(shape.shape)

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

