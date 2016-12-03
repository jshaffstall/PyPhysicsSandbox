import pygame
import pymunk

from pygame import Color

__docformat__ = "reStructuredText"


__all__ = ['window', 'add_observer', 'gravity', 'resistance', 'mouse_pressed',
           'static_ball', 'ball', 'static_box', 'box', 'static_rounded_box',
           'rounded_box', 'static_polygon', 'polygon', 'static_triangle',
           'triangle', 'static_text', 'text', 'static_text_with_font',
           'text_with_font', 'static_line', 'line', 'pivot', 'gear',
           'motor', 'pin', 'rotary_spring', 'run', 'draw', 'Color'
           ]


pygame.init()

space = pymunk.Space()
space.gravity = (0.0, 500.0)
space.damping = 0.95

win_title = "Untitled"
win_width = 500
win_height = 500
observers = []
pressed = False

shapes = []


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

    win_title = title
    win_width = width
    win_height = height


def add_observer(hook):
    """Adds an observer function to the simulation.  Every observer
    function is called once per time step of the simulation (roughly
    50 times a second).

    To pass a function in use the name of the function without the
    parenthesis after it.

    :param hook: the observer function
    :type hook: function

    """
    global observers

    observers.append(hook)


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


def mouse_pressed():
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
    return _ball(p, radius, pymunk.inf, True)


def ball(p, radius, mass=1):
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


def _ball(p, radius, mass=1, static=False):
    from .ball_shape import Ball

    result = Ball(space, p[0], p[1], radius, mass, static)
    shapes.append(result)

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


def box(p, width, height, mass=1):
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


def _box(p, width, height, mass, static):
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
    from .box_shape import Box

    # Polygons expect x,y to be the center point
    x = p[0] + width / 2
    y = p[1] + height / 2

    result = Box(space, x, y, width, height, 0, mass, static)
    shapes.append(result)

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
    return _rounded_box(p, width, height, radius, pymunk.inf, True)


def rounded_box(p, width, height, radius, mass=1):
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
    return _rounded_box(p, width, height, radius, mass, False)


def _rounded_box(p, width, height, radius, mass, static):
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
    from .box_shape import Box

    # Polygons expect x,y to be the center point
    x = p[0] + width / 2
    y = p[1] + height / 2

    result = Box(space, x, y, width, height, radius, mass, static)
    shapes.append(result)

    return result


def static_polygon(vertices):
    """Creates a polygon that remains fixed in place.

    :param vertices: A tuple of points on the polygon
    :type vertices: ((int, int), (int, int), ...)
    :rtype: shape

    """
    return _polygon(vertices, pymunk.inf, True)


def polygon(vertices, mass=1):
    """Creates a polygon that reacts to gravity.

    :param vertices: A tuple of points on the polygon
    :type vertices: ((int, int), (int, int), ...)
    :param mass: The mass of the shape (defaults to 1)
    :type mass: int
    :rtype: shape

    """
    return _polygon(vertices, mass, False)


def _polygon(vertices, mass, static):
    from .poly_shape import Poly
    from .util import poly_centroid

    x, y = poly_centroid(vertices)

    vertices = [(v[0] - x, v[1] - y) for v in vertices]
    result = Poly(space, x, y, vertices, 0, mass, static)
    shapes.append(result)

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


def triangle(p1, p2, p3, mass=1):
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


def _triangle(p1, p2, p3, mass, static):
    from .poly_shape import Poly

    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    x = (x1 + x2 + x3) / 3
    y = (y1 + y2 + y3) / 3
    vertices = ((x1 - x, y1 - y), (x2 - x, y2 - y), (x3 - x, y3 - y))

    result = Poly(space, x, y, vertices, 0, mass, static)
    shapes.append(result)

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


def text(p, caption, mass):
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


def _text(p, caption, mass, static):
    from .text_shape import Text

    result = Text(space, p[0], p[1], caption, "Arial", 12, mass, static)
    shapes.append(result)

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


def text_with_font(p, caption, font, size, mass=1):
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


def _text_with_font(p, caption, font, size, mass, static):
    from .text_shape import Text

    result = Text(space, p[0], p[1], caption, font, size, mass, static)
    shapes.append(result)

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


def line(p1, p2, thickness, mass=1):
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


def _line(p1, p2, thickness, mass, static):
    from .line_segment import Line

    result = Line(space, p1, p2, thickness, mass, static)
    shapes.append(result)

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
    shapes.append(result)

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
    shapes.append(result)

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
    shapes.append(result)

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
    shapes.append(result)

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
    shapes.append(result)

    return result


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

        for observer in observers:
            observer()

        screen.fill((255, 255, 255))

        # Should automatically remove any shapes that are
        # far enough below the bottom edge of the window
        # that they won't be involved in anything visible
        shapes_to_remove = []
        for shape in shapes:
            if shape.body.position.y > win_height * 2:
                shapes_to_remove.append(shape)

        for shape in shapes_to_remove:
            shape._active = False

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
                    shape.body.position = (win_width - 1, shape.body.position.y)

                if shape.body.position.x >= win_width:
                    shape.body.position = (0, shape.body.position.y)

                if shape.body.position.y < 0:
                    shape.body.position = (shape.body.position.x, win_height - 1)

                if shape.body.position.y >= win_height:
                    shape.body.position = (shape.body.position.x, 0)

        # Now draw the shapes that are left
        for shape in shapes:
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