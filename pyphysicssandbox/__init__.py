"""
pyPhysicsSandbox is a simple wrapper around Pymunk that makes it easy to write code to explore physics simulations.
It's intended for use in introductory programming classrooms.

Caution! The simulation does not behave well if you start out with shapes overlapping each other, especially if
overlapping shapes are connected with joints.  To have overlapping shapes connected by joints, set the group on
each shape to the same number to disable collision detection between those shape.

Shapes far enough outside the simulation window (generally, above or below by the height of the window, or to
either side by the width of the window) are automatically removed from the simulation and their active property
set to False.  The distance can be modified, but be wary of making it too large...this keeps shapes that are not
visible in the simulation and can slow the simulation down if the number of shapes grows too large.

"""

import pygame
import pymunk
import math

from pygame import Color
from pygame import constants

__docformat__ = "reStructuredText"


__all__ = ['window', 'add_observer', 'gravity', 'resistance', 'mouse_clicked',
           'static_ball', 'ball', 'static_box', 'box', 'static_rounded_box',
           'rounded_box', 'static_polygon', 'polygon', 'static_triangle',
           'triangle', 'static_text', 'text', 'static_text_with_font',
           'text_with_font', 'static_line', 'line', 'pivot', 'gear',
           'motor', 'pin', 'rotary_spring', 'run', 'draw', 'Color',
           'cosmetic_text', 'cosmetic_text_with_font', 'num_shapes',
           'constants', 'deactivate', 'reactivate', 'mouse_point',
           'add_collision', 'slip_motor', 'set_margins', 'cosmetic_box',
           'cosmetic_rounded_box', 'cosmetic_ball', 'cosmetic_line',
           'cosmetic_polygon', 'cosmetic_triangle', 'spring',
           'color'
           ]


pygame.init()

space = pymunk.Space()
space.gravity = (0.0, 500.0)
space.damping = 0.95

win_title = "Untitled"
win_width = 500
win_height = 500
x_margin = win_width
y_margin = win_height
observers = []
clicked = False
default_color = Color('black')

shapes = {}


def window(title, width, height):
    """Sets the caption, width, and height of the window that will
    appear when run () is executed.

    :param title: the caption of the window
    :type title: string
    :param width: the width of the window in pixels
    :type width: int
    :param height: the height of the window in pixels
    :type height: int

    """
    global win_title
    global win_width
    global win_height
    global x_margin
    global y_margin

    win_title = title
    win_width = width
    win_height = height
    x_margin = win_width
    y_margin = win_height


def add_observer(hook):
    """Adds an observer function to the simulation.  Every observer
    function is called once per time step of the simulation (roughly
    50 times a second).  The function should be defined like this:

        def function_name(keys):
            # do something each time step

    To pass a function in use the name of the function without the
    parenthesis after it.

    The observer function must take a single parameter which is a
    list of keys pressed this step.  To see if a particular key has
    been pressed, use something like this:

            if constants.K_UP in keys:
                # do something based on the up arrow being pressed

    :param hook: the observer function
    :type hook: function

    """
    global observers

    observers.append(hook)


def set_margins(x, y):
    """Sets the distance outside the simulation that shapes can be and remain active.
    This defaults to the window width and height.  You can change it to either remove
    shapes more quickly when they're out of view, or to allow creating shapes farther
    outside the visible window.

    :param x: horizontal margin
    :param y: vertical margin
    """
    global x_margin
    global y_margin

    x_margin = x
    y_margin = y


def gravity(x, y):
    """Sets the direction and amount of gravity used by the simulation.
    Positive x is to the right, positive y is downward.  This value can
    be changed during the run of the simulation.

    :param x: The horizontal gravity
    :type x: int
    :param y: The vertical gravity
    :type y: int

    """
    space.gravity = (x, y)


def color(c):
    """Sets the default color to use for shapes created after this
    call.  The function may be called at any point to change the
    color for new shapes.

    To see available color names go to
    https://sites.google.com/site/meticulosslacker/pygame-thecolors
    and hover the mouse pointer over a color of interest.

    :param c: the color name as a string
    :type c: str
    """
    global default_color

    default_color = Color(c)


def resistance(v):
    """Sets the amount of velocity that all objects lose each second.
    This can be used to simulate air resistance.  Resistance value
    defaults to 1.0.  Values less than 1.0 cause objects to lose
    velocity over time, values greater than 1.0 cause objects to
    gain velocity over time.

    For example a value of .9 means the body will lose 10% of its
    velocity each second (.9 = 90% velocity retained each second).

    This value can be changed during the run of the simulation.

    :param v: The resistance value
    :type v: float

    """
    space.damping = v


def mouse_clicked():
    """Returns True if the mouse has been clicked this time step. Usable only in an observer function.

    :rtype: bool

    """
    return clicked


def mouse_point():
    """Returns the current location of the mouse pointer.

    If the mouse is out of the simulation window, this will return the last location of the mouse
    that was in the simulation window.

    :rtype: (x, y)
    """
    return pygame.mouse.get_pos()


def static_ball(p, radius):
    """Creates a ball that remains fixed in place.

    :param p: The center point of the ball
    :type p: (int, int)
    :param radius: The radius of the ball
    :type radius: int
    :rtype: shape

    """
    return _ball(p, radius, pymunk.inf, True)


def ball(p, radius, mass=-1):
    """Creates a ball that reacts to gravity.

    :param p: The center point of the ball
    :type p: (int, int)
    :param radius: The radius of the ball
    :type radius: int
    :param mass: The mass of the shape (defaults to 1)
    :type mass: int
    :rtype: shape

    """
    return _ball(p, radius, mass, False)


def cosmetic_ball(p, radius):
    """Creates a ball that does not interact with the simulation in any way.

    :param p: The center point of the ball
    :type p: (int, int)
    :param radius: The radius of the ball
    :type radius: int
    :rtype: shape

    """
    return _ball(p, radius, 0, False, True)


def _ball(p, radius, mass, static=False, cosmetic=False):
    from .ball_shape import Ball

    if mass == -1:
        mass = math.pi*radius*radius

    result = Ball(space, p[0], p[1], radius, mass, static, cosmetic)
    result.color = default_color
    shapes[result.collision_type] = result

    return result


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
    return _box(p, width, height, pymunk.inf, True)


def box(p, width, height, mass=-1):
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
    return _box(p, width, height, mass, False)


def cosmetic_box(p, width, height):
    """Creates a box that does not react with the simulation in any way.

    :param p: The upper left corner of the box
    :type p: (int, int)
    :param width: The width of the box
    :type width: int
    :param height: The height of the box
    :type height: int
    :rtype: shape

    """
    return _box(p, width, height, 0, False, 0, True)


def _box(p, width, height, mass, static, radius=0, cosmetic=False):
    from .box_shape import Box

    if mass == -1:
        mass = width * height

    # Polygons expect x,y to be the center point
    x = p[0] + width / 2
    y = p[1] + height / 2

    result = Box(space, x, y, width, height, radius, mass, static, cosmetic)
    result.color = default_color
    shapes[result.collision_type] = result

    return result


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
    return _box(p, width, height, pymunk.inf, True, radius)


def rounded_box(p, width, height, radius, mass=-1):
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
    return _box(p, width, height, mass, False, radius)


def cosmetic_rounded_box(p, width, height, radius):
    """Creates a box with rounded corners that does not interact with the simulation in any way.

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
    return _box(p, width, height, 0, False, radius, True)


def static_polygon(vertices):
    """Creates a polygon that remains fixed in place.

    :param vertices: A tuple of points on the polygon
    :type vertices: ((int, int), (int, int), ...)
    :rtype: shape

    """
    return _polygon(vertices, pymunk.inf, True)


def polygon(vertices, mass=-1):
    """Creates a polygon that reacts to gravity.

    :param vertices: A tuple of points on the polygon
    :type vertices: ((int, int), (int, int), ...)
    :param mass: The mass of the shape (defaults to 1)
    :type mass: int
    :rtype: shape

    """
    return _polygon(vertices, mass, False)


def cosmetic_polygon(vertices):
    """Creates a polygon that does not interact with the simulation in any way.

    :param vertices: A tuple of points on the polygon
    :type vertices: ((int, int), (int, int), ...)
    :rtype: shape

    """
    return _polygon(vertices, 0, False, True)


def _polygon(vertices, mass, static, cosmetic=False):
    from .poly_shape import Poly
    from .util import poly_centroid
    from .util import poly_area

    x, y = poly_centroid(vertices)

    if mass == -1:
        mass = poly_area(vertices)

    vertices = [(v[0] - x, v[1] - y) for v in vertices]
    result = Poly(space, x, y, vertices, 0, mass, static, cosmetic)
    result.color = default_color
    shapes[result.collision_type] = result

    return result


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
    return _triangle(p1, p2, p3, pymunk.inf, True)


def triangle(p1, p2, p3, mass=-1):
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
    return _triangle(p1, p2, p3, mass, False)


def cosmetic_triangle(p1, p2, p3):
    """Creates a triangle that does not interact with the simulation in any way.

    :param p1: The first point of the triangle
    :type p1: (int, int)
    :param p2: The second point of the triangle
    :type p2: (int, int)
    :param p3: The third point of the triangle
    :type p3: (int, int)
    :rtype: shape

    """
    return _triangle(p1, p2, p3, 0, False, True)


def _triangle(p1, p2, p3, mass, static, cosmetic=False):
    from .poly_shape import Poly
    from .util import poly_area

    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    x = (x1 + x2 + x3) / 3
    y = (y1 + y2 + y3) / 3
    vertices = ((x1 - x, y1 - y), (x2 - x, y2 - y), (x3 - x, y3 - y))

    if mass == -1:
        mass = poly_area(vertices)

    result = Poly(space, x, y, vertices, 0, mass, static, cosmetic)
    result.color = default_color
    shapes[result.collision_type] = result

    return result


def static_text(p, caption):
    """Creates a text rectangle that remains fixed in place, using
    Arial 12 point font.

    :param p: The upper left corner of the text rectangle
    :type p: (int, int)
    :param caption: The text to display
    :type caption: string
    :rtype: shape

    """
    return _text(p, caption, pymunk.inf, True)


def text(p, caption, mass=-1):
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
    return _text(p, caption, mass, False)


def cosmetic_text(p, caption):
    """Creates text that displays on the screen but does not interact
    with other objects in any way.

    :param p: The upper left corner of the text
    :type p: (int, int)
    :param caption: The text to display
    :type caption: string
    :rtype: shape

    """
    return _text(p, caption, 0, False, True)


def _text(p, caption, mass, static, cosmetic=False):
    from .text_shape import Text

    if mass == -1:
        mass = 10 * len(caption)

    result = Text(space, p[0], p[1], caption, "Arial", 12, mass, static, cosmetic)
    result.color = default_color
    shapes[result.collision_type] = result

    return result


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
    return _text_with_font(p, caption, font, size, pymunk.inf, True)


def text_with_font(p, caption, font, size, mass=-1):
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
    return _text_with_font(p, caption, font, size, mass, False)


def cosmetic_text_with_font(p, caption, font, size):
    """Creates text that displays on the screen but does not interact
    with other objects in any way.

    :param p: The upper left corner of the text
    :type p: (int, int)
    :param caption: The text to display
    :type caption: string
    :param font: The font family to use
    :type font: string
    :param size: The point size of the font
    :type size: int
    :rtype: shape

    """
    return _text_with_font(p, caption, font, size, 0, False, True)


def _text_with_font(p, caption, font, size, mass, static, cosmetic=False):
    from .text_shape import Text

    if mass == -1:
        mass = 10 * len(caption)

    result = Text(space, p[0], p[1], caption, font, size, mass, static, cosmetic)
    result.color = default_color
    shapes[result.collision_type] = result

    return result


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
    return _line(p1, p2, thickness, pymunk.inf, True)


def line(p1, p2, thickness, mass=-1):
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
    return _line(p1, p2, thickness, mass, False)


def cosmetic_line(p1, p2, thickness):
    """Creates a line segment that does not interact with the simulation in any way.

    :param p1: The starting point of the line segement
    :type p1: (int, int)
    :param p2: The ending point of the line segement
    :type p2: (int, int)
    :param thickness: The thickness of the line segement
    :type thickness: int
    :rtype: shape

    """
    return _line(p1, p2, thickness, 0, False, True)


def _line(p1, p2, thickness, mass, static, cosmetic=False):
    from .line_segment import Line

    if mass == -1:
        mass = math.sqrt(math.pow(p1[0]-p2[0], 2)+math.pow(p1[1]-p2[1], 2))*thickness

    result = Line(space, p1, p2, thickness, mass, static, cosmetic)
    result.color = default_color
    shapes[result.collision_type] = result

    return result


def pivot(p):
    """Creates a pivot joint around which shapes can freely rotate.
    Shapes must be connected to the pivot using the connect method
    on the returned shape.  The pivot joint remains fixed in place.

    :param p: The point at which to place the pivot
    :type p: (int, int)
    :rtype: shape

    """
    from .pivot_joint import Pivot

    result = Pivot(space, p[0], p[1])
    result.color = default_color
    shapes[result.collision_type] = result

    return result


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
    from .gear_joint import Gear

    result = Gear(space, shape1, shape2)
    result.color = default_color
    shapes[result.collision_type] = result

    return result


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
    from .motor_joint import Motor

    result = Motor(space, shape1, speed)
    result.color = default_color
    shapes[result.collision_type] = result

    return result


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
    from .pin_joint import Pin

    result = Pin(space, p1, shape1, p2, shape2)
    result.color = default_color
    shapes[result.collision_type] = result

    return result


def spring(p1, shape1, p2, shape2, length, stiffness, damping):
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
    :param length: The length the spring wants to be
    :type length: float
    :param stiffness: The spring constant (Young’s modulus)
    :type stiffness: float
    :param damping: How soft to make the damping of the spring
    :type damping: float
    :rtype: shape

    """
    from .spring_joint import Spring

    p1 = (p1[0]-shape1.position[0], p1[1]-shape1.position[1])
    p2 = (p2[0]-shape2.position[0], p2[1]-shape2.position[1])

    result = Spring(space, p1, shape1, p2, shape2, length, stiffness, damping)
    result.color = default_color
    shapes[result.collision_type] = result

    return result


def slip_motor(shape1, shape2, rest_angle, stiffness, damping, slip_angle, speed):
    """Creates a combination spring and motor.  The motor will rotate shape1
    around shape2 at the given speed.  When shape1 reaches the slip angle it
    will spring back to the rest_angle.  Then the motor will start to rotate
    the object again.

    :param shape1: The first shape to connect via the spring
    :type shape1: shape
    :param shape2: The second shape to connect via the spring
    :type shape2: shape
    :param rest_angle: The desired angle between the two objects
    :type rest_angle: float
    :param stiffness: the spring constant (Young's modulus)
    :type stiffness: float
    :param damping: the softness of the spring damping
    :type damping: float
    :param slip_angle: The angle at which to release the object
    :type slip_angle: float
    :param speed: The speed at which to rotate the shape
    :type speed: int
    :rtype: shape

    """
    from .slip_motor import SlipMotor

    result = SlipMotor(space, shape1, shape2, rest_angle, stiffness, damping, slip_angle, speed)
    result.color = default_color
    shapes[result.collision_type] = result

    return result


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
    from .rotary_spring import RotarySpring

    result = RotarySpring(space, shape1, shape2, angle, stiffness, damping)
    result.color = default_color
    shapes[result.collision_type] = result

    return result


def num_shapes():
    """Returns the number of active shapes in the simulation.

    :rtype int
    """
    return len(shapes)


def deactivate(shape):
    """Removes the given shape from the simulation.  The shape will no longer
    display or interact with other objects

    :param shape: the shape to deactivate
    """
    if not shape.active:
        return

    shape.deactivate()
    del shapes[shape.collision_type]


def reactivate(shape):
    """The given shape will be reactivated.  Its position and velocity will remain the same
    as it was when it was deactivated.

    :param shape: the shape to activate
    """
    if shape.active:
        return

    shape.reactivate()
    shapes[shape.collision_type] = shape


def add_collision(shape1, shape2, handler):
    """Tells the sandbox to call a function when the two given shapes collide.
    The handler function is called once per collision, at the very start of the
    collision.

    The handler function is passed three parameters.  The first two are the
    colliding shapes, the third is the point of the collision, e.g.:

        handler(shape1, shape2, p)

    :param shape1: the first shape in the collision
    :param shape2: the other shape in the collision
    :param handler: the function to call
    :return:
    """
    temp = space.add_collision_handler(shape1.collision_type, shape2.collision_type)
    temp.data['handler'] = handler
    temp.begin = handle_collision


def handle_collision(arbiter, space, data):
    shape1 = shapes[arbiter.shapes[0].collision_type]
    shape2 = shapes[arbiter.shapes[1].collision_type]
    p = arbiter.contact_point_set.points[0].point_a

    return data['handler'](shape1, shape2, p)

def _calc_margins():
    global x_margin
    global y_margin

    for shape in shapes:
        x, y = shapes[shape].position
        x = abs(x)
        y = abs(y)

        if x_margin < x:
            x_margin = x

        if y_margin < y:
            y_margin = y


def run(do_physics=True):
    """Call this after you have created all your shapes to actually run the simulation.
    This function returns only when the user has closed the simulation window.

    Pass False to this method to do the drawing but not activate physics.
    Useful for getting the scene right before running the simulation.

    :param do_physics: Should physics be activated or not
    :type do_physics: bool
    """
    global clicked

    _calc_margins()

    screen = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption(win_title)
    clock = pygame.time.Clock()
    running = True

    while running:
        keys = []
        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                keys.append(event.key)

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        for observer in observers:
            observer(keys)

        screen.fill((255, 255, 255))

        # Should automatically remove any shapes that are
        # far enough below the bottom edge of the window
        # that they won't be involved in anything visible
        shapes_to_remove = []
        for collision_type, shape in shapes.items():
            if shape.position.x > win_width + x_margin:
                shapes_to_remove.append(shape)

            if shape.position.x < -x_margin:
                shapes_to_remove.append(shape)

            if shape.position.y > win_height + y_margin:
                shapes_to_remove.append(shape)

            if shape.position.y < -y_margin:
                shapes_to_remove.append(shape)

        for shape in shapes_to_remove:
            deactivate(shape)

        # Also adjust positions for any shapes that are supposed
        # to wrap and have gone off an edge of the screen.
        for collision_type, shape in shapes.items():
            if shape.wrap_x:
                if shape.position.x < 0:
                    shape.position = (win_width - 1, shape.position.y)

                if shape.position.x >= win_width:
                    shape.position = (0, shape.position.y)

            if shape.wrap_y:
                if shape.position.y < 0:
                    shape.position = (shape.position.x, win_height - 1)

                if shape.position.y >= win_height:
                    shape.position = (shape.position.x, 0)

        # Now draw the shapes that are left
        for collision_type, shape in shapes.items():
            shape.draw(screen)

        if do_physics:
            space.step(1 / 50.0)

        pygame.display.flip()
        clock.tick(50)

    pygame.quit()


def draw():
    """Call this after you have created all your shapes to actually draw them.
    This function only returns after you close the window.

    This is an alias for run(False).
    """
    run(False)
