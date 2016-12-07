## Synopsis

pyPhysicsSandbox is a simple wrapper around Pymunk that makes it easy to write code to explore physics simulations.  It's intended for use in introductory programming classrooms.

Caution! The simulation does not behave well if you start out with objects overlapping each other, especially if overlapping objects are connected with joints.  To have overlapping objects connected by joints, set the group on each object to the same number to disable collision detection between those objects.

Objects far enough outside the simulation window (generally, above or below by the height of the window, or to either side by the width of the window) are automatically removed from the simulation and their active property set to False.

## Code Example

```python
from pyPhysicsSandbox import *

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

The Calico IDE had a nice physics simulation built into it I used for a lab in my introductory programming classes.  Students wanted to use features that were reasonable to think about in a physics simulation (joints and pins, for example), but were not exposed by Calico.  This wrapper keeps the simplicity of the Calico physics API but exposes more advanced tools.

Efficiency was also a goal.  This library handles more objects than the Calico IDE before slowing down, allowing students to create a thousand objects in a for loop and still be able to run the simulation in a reasonable time.

Also, being IDE agnostic, this library can be used with your favorite IDE.

## Installation

The code is written for Python 3, and uses pygame, pymunk, and py2d.  You must install all of those packages before you can use this library.  I have not made use of requirements.txt since py2d and pygame particularly you cannot install using the standard pip repositories.

###Python 3

https://www.python.org/

This library was written with Python 3.5, but should run on any Python 3.

###pygame

http://www.pygame.org/

This library was written with pygame 1.9.  I specifically used the Windows 64-bit versions available at http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame , but any 1.9 or later version that supports Python 3 should work.  

###pymunk

http://www.pymunk.org/

This library was written with pymunk 5.1.0.  This you can safely install using pip.

###py2d

https://github.com/sseemayer/Py2D

This library was written with the version of py2d on github, since the pip package at the time did not support Python 3.  To get a quick and dirty install from github, use pip to install the older version and then download a zip from github and copy the py2d directory over top of the same directory in your Python site-packages.

###pyPhysicsSandbox

Once the dependencies are installed, install this library using:

```
pip install pyPhysicsSandbox
```

## API Reference

```python
window(caption, width, height)
```

Specifies the width and height and caption of the simulation window.  Multiple calls to this overwrite the old values.  You only get one window regardless.

```python
gravity(x, y)
```

Sets the gravity of the simulation.  Positive y is downward, positive x is rightward.  Default is (0, 500).

```python
damping(v)
```

Sets how much velocity each object in the simulation keeps each second.  Must be a floating point number.  Default is 0.95.  Values higher than 1.0 cause objects to increase in speed rather than lose it.  A value of 1.0 means objects will not lose any velocity artificially.   

```python
add_observer(observer_func)
```

Provide a function of yours that will get called once per frame.  In this function you can use the various objects you've created to either affect the simulation or simply measure something.

You may call add_observer multiple times to add different observer functions.

The function should be defined like this:

```python
        def function_name(keys):
            # do something each time step
```

The observer function must take a single parameter which is a
list of keys pressed this step.  To see if a particular key has
been pressed, use something like this:
    
```python
            if constants.K_UP in keys:
                # do something based on the up arrow being pressed
```

```python
mouse_clicked ()
```

Returns True if the mouse has been clicked this time step. Usable only in an observer function.

```python
mouse_point ()
```

Returns the current location of the mouse pointer as an (x, y) tuple.

If the mouse is out of the simulation window, this will return the last location of the mouse that was in the simulation window.

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
line(p1, p2, thickness)
static_line(p1, p2, thickness)
```

Creates a line from coordinates p1 to coordinates p2 of the given thickness.  The static line version does not move.  

```python
pivot1 = pivot(p)
pivot1.connect(other_shape)
```

Create a pivot joint at point p in the world.  The other_shape should be a shape whose coordinates intersect the location of the pivot joint.  

The pivot joint pins the other shape to the background, not allowing it to fall.  The other shape can rotate around the pivot joint.
 
```python
gear1 = gear(shape1, shape2)
```

Creates a gear joint connecting the two shapes.  A gear joint keeps the angle of the two shapes constant.  As one shape rotates, the other rotates to match automatically.

Note that the gear has no visible representation in the simulation.

```python
motor(shape1, radians)
```

Creates a motor to give the shape a constant rotation.  If you want other shapes to also rotate at the same rate, use a gear joint to connect them to the shape with the motor.

The motor displays as a semicircle with a dot in the direction of rotation.

```python
pin((100, 580), ball1, (150, 580), ball2)
```

Creates a pin joint between the two shapes at the given points.  A pin joint creates a fixed separation between the two bodies (as if there were a metal pin connecting them).  You'll get strange effects when wrapping these shapes.

```python
num_shapes()
```

Returns the number of active shapes in the simulation.  Mostly useful for debugging.

```python
deactivate(shape)
```

Removes the given shape from the simulation.

```python
reactivate(shape)
```

Adds the given shape back to the simulation.

```python
run(do_physics=True)
```

Call this after you have created all your shapes to actually run the simulation.  This function returns only when the user has closed the simulation window.

Pass False to this method to do the drawing but not activate physics.  Useful for getting the scene right before running the simulation.

```python
draw()
```

Call this after you have created all your shapes to draw the shapes.  This function returns only when the user has closed the window.

This is an alias for run(False).

###Shape Methods

Each shape object that gets returned has some methods and properties that can be called to adjust the shape.  

```python
shape.hit(direction, position)
```

Hits the shape at the given position in the given direction.  This is an instantaneous impulse.

Direction is a tuple containing the x direction and y direction (in the same orientation as the gravity tuple).

Position is a tuple containing the x and y position of the spot on the shape to hit.

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
 
This is a convenience function for setting wrap_x and wrap_y at the same time. 

```python
shape.wrap_x
```

Sets whether the shape should wrap when going off the sides of the screen or not. 

```python
shape.wrap_y
```

Sets whether the shape should wrap when going off the top or bottom of the screen or not. 

```python
shape.visible
```

Sets whether the shape draws itself or not.  Defaults to True.  Most useful to set this to False for joints you don't want shown on screen. 

```python
shape.group
```

Set to an integer.  Shapes that share the same group number will not collide with each other.  Useful to have overlapping objects connected by joints that do not make the physics crazy. 

```python
shape.gravity
```

Set to an (x, y) vector in the same format as the overall gravity vector.  This overrides the overall gravity for this shape only.

```python
shape.damping
```

Set a damping value specific for this shape.  This overrides the overall damping value for this shape only.

```python
shape.paste_on(other_shape)
```

Paste one shape onto another shape.  The coordinates for the shape must be inside that of the other_shape and their group must be set to the same value to disable collision detection between them.
  
This can be used, for example, to draw some text inside a shape. 

This is only suitable for calling on actual shapes!  The various joints already attach themselves to objects.

```python
shape.inside(p)
```

Returns True is the given point is inside the given shape.  Does not care if the shape is visible or not or active or not.

```python
shape.draw_radius_line
```

Only for balls, this sets whether a line from the center of the ball to the 0 degree point on the outer edge is drawn.  Defaults to False.  Can be set to True to gauge rotation of the ball. 

```python
shape.text
```

Only for text, this sets the text to be displayed.  This will modify the box shape around the text for collision detection. 

## Tests

Describe and show how to run the tests with code examples.

## Contributors

Let people know how they can dive into the project, include important links to things like issue trackers, irc, twitter accounts if applicable.

## License

A short snippet describing the license (MIT, Apache, etc.)