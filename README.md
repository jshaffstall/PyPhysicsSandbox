## Synopsis

PyPhysicsSandbox is a simple wrapper around Pymunk that makes it easy to write code to explore physics simulations.  It's intended for use in introductory programming classrooms.

## Code Example

```python
from PyPhysicsSandbox import *

window("My Window", 400, 300)
gravity(0.0, 500.0)

b1 = ball((100, 10), 30)
b1.color = Color('green')
b1.friction = 0.25

b2 = static_ball((98, 100), 30)
b2.color = Color('blue')

box1 = static_rounded_box((0, 290), 400, 10, 3)
box1.color = Color('red')

tri1 = triangle((260, 35), (250, 35), (240, -15))
tri1.color = Color('red')

poly1 = poly(((195, 35), (245, 35), (220, -15)))
poly1.color = Color('blue')
poly1.wrap = True

run()

print('Done!')
```

## Motivation

The Calico IDE had a simple but limited physics simulation built into it I used for a lab in my introductory programming classes.  Students wanted to use features that were reasonable to think about in a physics simulation (joints and pins, for example), but were not supported in Calico.  This wrapper keeps the simplicity of the Calico physics API but exposes more advanced tools.

## Installation

The code is written for Python 3, and uses pygame and pymunk.  You must install both of those packages before you can use this library.

TODO: how to install easily?

## API Reference

```python
window(caption, width, height)
```

Specifies the width and height and caption of the simulation window.  Multiple calls to this overwrite the old values.  You only get one window regardless.

```python
gravity(x, y)
```

Sets the gravity of the simulation.  Positive y is downward, positive x is rightward.

```python
set_observer(observer_func)
```

Provide a function of yours that will get called once per frame.  In this function you can use the various objects you've created to either affect the simulation or simply measure something.

```python
mouse_pressed ()
```

Returns True if the mouse is currently pressed.  Only returns True once per mouse press, regardless of how often you poll.  Usable only in an observer function.

```python
ball(p, radius, mass=1)
static_ball(p, radius, mass=1)
```

Create a ball object and return its instance.  The static version creates a ball that does not move.

p is a tuple containing the x and y coordinates of the center of the ball.  

```python
box(p, width, height, mass=1)
static_box(p, width, height, mass=1)
```

Create a box object and return its instance.  The static version creates a box that does not move.

p is a tuple containing the x and  y coordinates of the upper left corner of the box.

```python
rounded_box(p, width, height, radius, mass=1)
static_rounded_box(p, width, height, radius, mass=1)
```

Create a box object and returns its instance.  The static version creates a box that does not move.  These boxes are drawn with rounded corners.

p is a tuple containing the x and  y coordinates of the upper left corner of the box.
radius is the radius of the corner curve.  3 works well, but you can pass any integer.

```python
triangle(p1, p2, p3, mass=1)
static_triangle(p1, p2, p3, mass=1)
```

Creates a triangle out of the given points and returns its instance.  The static version creates a triangle that does not move.

```python
poly(vertices, mass=1)
static_poly(vertices, mass=1)
```

Creates a closed polygon out of the given points and returns its instance.  The last point is automatically connected back to the first point.  The static version does not move.

vertices is a tuple of points, where each point is a tuple of x and y coordinates.  The order of these points matters!

```python
text(p, caption)
static_text(p, caption)
```

Creates text that will interact with the world as if it were a rectangle.  The static text version does not move.

p is a tuple containing the x and  y coordinates of the upper left corner of the text.

```python
run()
```

Call this after you have created all your shapes to actually run the simulation.  This function returns only when the user has closed the simulation window.

###Shape Methods

Each shape object that gets returned has some methods and properties that can be called to adjust the shape.  

```python
shape.hit(x, y)
```

Hits the shape in the given direction.  This is an instantaneous impulse.

```python
shape.color
```

Sets the color for the shape.  The value must be a pygame Color instance.  The default color is black.

```python
shape.elasticity
```

Sets how bouncy the object is.  The default is 0.9.

```python
shape.friction
```

Sets how much friction the object should have.  The default is 0.6.  The Wikipedia article on friction has examples of values for different materials: https://en.wikipedia.org/wiki/Friction

```python
shape.wrap
```

Sets whether the shape should wrap when going off the edges of the screen or not.  A True value means the shape can never be off screen, and if it starts off screen it's immediately brought on as if it were wrapping. 

## Tests

Describe and show how to run the tests with code examples.

## Contributors

Let people know how they can dive into the project, include important links to things like issue trackers, irc, twitter accounts if applicable.

## License

A short snippet describing the license (MIT, Apache, etc.)