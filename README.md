## Synopsis

pyPhysicsSandbox is a simple wrapper around Pymunk that makes it easy to write code to explore 2D physics simulations. It's intended for use in introductory programming classrooms.

Caution! The simulation does not behave well if you start out with shapes overlapping each other, especially if overlapping shapes are connected with joints.  To have overlapping shapes connected by joints, set the group on each shape to the same number to disable collision detection between those shape.

On the other hand, see the volcano example for a situation where overlapping shapes that collide with each other are useful.

Shapes far enough outside the simulation window (generally, above or below by the height of the window, or to either side by the width of the window) are automatically removed from the simulation and their active property set to False.  The distance can be modified, but be wary of making it too large...this keeps shapes that are not visible in the simulation and can slow the simulation down if the number of shapes grows too large.

## Code Example

```python
from pyphysicssandbox import *

window("My Window", 400, 300)
gravity(0.0, 500.0)

b1          = ball((100, 10), 30)
b1.color    = Color('green')
b1.friction = 0.25

b2       = static_ball((98, 100), 30)
b2.color = Color('blue')

box1       = static_rounded_box((0, 290), 400, 10, 3)
box1.color = Color('red')

tri1       = triangle((260, 35), (250, 35), (240, -15))
tri1.color = Color('red')

poly1       = polygon(((195, 35), (245, 35), (220, -15)))
poly1.color = Color('blue')
poly1.wrap  = True

run()

print('Done!')
```

## Motivation

My introductory programming students love writing physics simulations, but the previous physics engine we used did not expose enough features (pins and motors, for example) to be interesting enough to more advanced students.  PyPhysicsSandbox retains the simplicity needed for intro programming students, but exposes more advanced tools.

Also, being IDE agnostic, this library can be used with your favorite IDE.

## In Use At

If you use PyPhysicsSandbox, let me know where and I'll add you here.

[Muskingum University](http://muskingum.edu/) for their Intro to Computer Science course

John Glenn High School for their after school coding club

## Summary of Features

pyPhysicsSandbox provides an easy Python interface to a rigid-body physics sandbox.  Features include:

### Shapes

* Circles
* Rectangles
* Triangles
* Solid Polygons (both convex and concave)
* Line Segments
* Text

### Constraints

* Pivot Joints
* Pin Joints
* Motors
* Slip Motors
* Springs
* Gears

### Other

* User Specified Collision Handlers
* User Specified Observer Functions
* Disable Collisions Between Specific Objects
* Custom Shape Properties - color, friction, gravity, damping, elasticity
* Set shapes to constant velocities
* Allow Shapes to Wrap Around the Screen
* Conveyor Belt Like Behavior
* Pasting One Shape Onto Another - so they behave as one shape
* Hit shapes in a specific direction with a given force
* Handles Thousands of Shapes
* Built in debug output that can be turned on for individual shapes

## Tutorials

Screencasts highlighting various features of the sandbox are available on the [PyPhysicsSandbox YouTube channel](https://www.youtube.com/channel/UCybNk1XwGtiPyiLVitMFmsQ)

## Installation

### Python 3

https://www.python.org/

This library was written with Python 3.5, but should run on any Python 3.  Python 3 must be installed first.

### pyPhysicsSandbox

Given a suitable Python 3 installation, you should be able to install pyPhysicsSandbox by opening a command prompt in the Scripts folder of your Python installation and typing:

```
pip install pyphysicssandbox
```

### Dependencies

http://www.pygame.org/
http://www.pymunk.org/

Both pygame and pymunk should be automatically installed when you install pyPhysicsSandbox.  If something goes wrong and you need to install them manually, see their respective sites for directions.

## API Reference

### Simulation-wide functions

```python
window(caption, width, height)
```

Specifies the width and height and caption of the simulation window.  Multiple calls to this overwrite the old values.  You only get one window regardless.

```python
set_margins(x, y)
```

Sets the minimum distance outside the visible window a shape can be and still be in the simulation.  Outside of this distance the shape is deactivated.  The default x margin is the window's width and the default y margin is the window's height.

Note that if you create a shape and give it an initial position outside these margins, the simulation will expand the margins to include the shape.

Use set_margins to increase the y margin particularly if you expect a shape on screen to be fired high above the top of the screen.

```python
color(v)
```

Sets the default color for shapes drawn after this function is called.  Color must be a string containing a valid color name.

See https://sites.google.com/site/meticulosslacker/pygame-thecolors for a list of colors. Hover your mouse over a color to see its name.

```python
gravity(x, y)
```

Sets the gravity of the simulation.  Positive y is downward, positive x is rightward.  Default is (0, 500).

```python
resistance(v)
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
add_collision(shape1, shape2, handler)
```

Tells the sandbox to call a function when the two given shapes collide. The handler function is called once per collision, at the very start of the collision.

The handler function is passed three parameters. The first two are the colliding shapes, the third is the point of the collision, e.g.:

```python
        handler(shape1, shape2, p)
```

The handler function must return True to allow the collision to happen.  If the handler returns False, then the collision will not happen.

Note that you will never have a collision with a deactivated object or with a cosmetic object.

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

### Shape creation functions

All the shapes have both a static and cosmetic variation shown.

Static shapes will interact with the physics simulation but will never move.  Other shapes will collide with the static shapes, but the static shapes are immovable objects.

Cosmetic shapes also will never move, but they also do not interact with the physics simulation in any way.  Other shapes will fall through the cosmetic shapes.  This means you may not also use a cosmetic shape as part of a paste_on call.

```python
ball(p, radius, mass)
static_ball(p, radius)
cosmetic_ball(p, radius)
```

Create a ball object and return its instance.

p is a tuple containing the x and y coordinates of the center of the ball.  

You can omit the mass parameter and the mass will be set proportional to the area of the shape.

```python
box(p, width, height, mass)
static_box(p, width, height)
cosmetic_box(p, width, height)
```

Create a box object and return its instance.

p is a tuple containing the x and  y coordinates of the upper left corner of the box.

You can omit the mass parameter and the mass will be set proportional to the area of the shape.

```python
rounded_box(p, width, height, radius, mass)
static_rounded_box(p, width, height, radius)
cosmetic_rounded_box(p, width, height, radius)
```

Create a box object and returns its instance. These boxes are drawn with rounded corners.

p is a tuple containing the x and  y coordinates of the upper left corner of the box.
radius is the radius of the corner curve.  3 works well, but you can pass any integer.

You can omit the mass parameter and the mass will be set proportional to the area of the shape.

```python
triangle(p1, p2, p3, mass)
static_triangle(p1, p2, p3)
cosmetic_triangle(p1, p2, p3)
```

Creates a triangle out of the given points and returns its instance.

You can omit the mass parameter and the mass will be set proportional to the area of the shape.

```python
polygon(vertices, mass)
static_polygon(vertices)
cosmetic_polygon(vertices)
```

Creates a closed polygon out of the given points and returns its instance.  The last point is automatically connected back to the first point.

vertices is a tuple of points, where each point is a tuple of x and y coordinates.  The order of these points matters!

You can omit the mass parameter and the mass will be set proportional to the area of the shape.

```python
text(p, caption, mass)
static_text(p, caption)
cosmetic_text(p, caption)
text_with_font(p, caption, font, size, mass)
static_text_with_font(p, caption, font, size)
cosmetic_text_with_font(p, caption, font, size)
```

Creates text that will interact with the world as if it were a rectangle.

p is a tuple containing the x and  y coordinates of the upper left corner of the text.

You can omit the mass parameter and the mass will be set proportional to the area of the shape.

```python
line(p1, p2, thickness, mass)
static_line(p1, p2, thickness)
cosmetic_line(p1, p2, thickness)
```

Creates a line from coordinates p1 to coordinates p2 of the given thickness.

You can omit the mass parameter and the mass will be set proportional to the area of the shape.

### Constraints

Constraints will limit or control the motion of other shapes in some fashion.

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
motor(shape1, speed)
```

Creates a motor to give the shape a constant rotation. The direction of rotation is controlled by the sign of the speed.  Positive speed is clockwise, negative speed is counter-clockwise.

If you want other shapes to also rotate at the same rate, use a gear joint to connect them to the shape with the motor.

The motor displays as a semicircle with a dot in the direction of rotation.

```python
spring(p1, shape1, p2, shape2, length, stiffness, damping)
```

Creates a spring that connects two shapes at the given points.  The spring wants to remain at the given length, but forces can make it be longer or shorter temporarily. 

```python
rotary_spring(shape1, shape2, angle, stiffness, damping)
```

Creates a spring that constrains the rotations of the given shapes. The angle between the two shapes prefers to be at the given angle, but may be varied by forces on the objects. The spring will bring the objects back to the desired angle.  The initial positioning of the shapes is considered to be at an angle of 0.

A normal scenario for this is for shape1 to be a shape rotating around shape2, which is a pivot joint or other static object, but play around with different ways of using rotary springs.

```python
slip_motor(shape1, shape2, rest_angle, stiffness, damping, slip_angle, speed)
```

Creates a combination spring and motor.  The motor will rotate shape1 around shape2 at the given speed.  When shape1 reaches the slip angle it will spring back to the rest_angle.  Then the motor will start to rotate the object again.
 
```python
pin((100, 580), ball1, (150, 580), ball2)
```

Creates a pin joint between the two shapes at the given points.  A pin joint creates a fixed separation between the two bodies (as if there were a metal pin connecting them).  You'll get strange effects when wrapping these shapes.

###Shape Methods and Properties

Each shape object that gets returned has some methods and properties that can be called to adjust the shape.  

```python
shape.debug=True
```

Turns on debug output for the given shape.  Each time step the shape will print out information about its current location and other pertinent characteristics.

```python
shape.hit(direction, position)
```

Hits the shape at the given position in the given direction.  This is an instantaneous impulse.

Direction is a tuple containing the x direction and y direction (in the same orientation as the gravity tuple).

Position is a tuple containing the x and y position of the spot on the shape to hit.

```python
shape.color=Color('blue')
```

Sets the color for the shape.  The value must be a pygame Color instance.  The default color is black.

```python
shape.angle=90
```

Sets the angle for the shape.  Can be used to start shapes off rotated.

```python
shape.elasticity=0.0
```

Sets how bouncy the object is.  The default is 0.9.

```python
shape.friction=0.95
```

Sets how much friction the object should have.  The default is 0.6.  The Wikipedia article on friction has examples of values for different materials: https://en.wikipedia.org/wiki/Friction

```python
shape.velocity=(200,0)
```

Sets a constant velocity for the shape.  The shape will still interact with other shapes, but will always move in the given direction.

To disable a constant velocity and return the shape to reacting to gravity normally, set the velocity to None.

```python
shape.surface_velocity=(200,0)
```

Sets how much surface velocity the object should have.  The default is (0, 0).  
 
This is the amount of movement objects touching this surface will have imparted to them.  You can use this to set up a conveyor belt.  

```python
shape.wrap=True
```

Sets whether the shape should wrap when going off the edges of the screen or not.  A True value means the shape can never be off screen, and if it starts off screen it's immediately brought on as if it were wrapping.
 
This is a convenience function for setting wrap_x and wrap_y at the same time. 

```python
shape.wrap_x=True
```

Sets whether the shape should wrap when going off the sides of the screen or not. 

```python
shape.wrap_y+True
```

Sets whether the shape should wrap when going off the top or bottom of the screen or not. 

```python
shape.visible=False
```

Sets whether the shape draws itself or not.  Defaults to True.  Most useful to set this to False for joints you don't want shown on screen. 

```python
shape.group=1
```

Set to an integer.  Shapes that share the same group number will not collide with each other.  Useful to have overlapping objects connected by joints that do not make the physics crazy. 

```python
shape.gravity=(0,-300)
```

Set to an (x, y) vector in the same format as the overall gravity vector.  This overrides the overall gravity for this shape only.

```python
shape.damping=0.9
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
shape.draw_radius_line=True
```

Only for balls, this sets whether a line from the center of the ball to the 0 degree point on the outer edge is drawn.  Defaults to False.  Can be set to True to gauge rotation of the ball. 

```python
shape.text='Some text"
```

Only for text, this sets the text to be displayed.  This will modify the box shape around the text for collision detection. 

## Contributors

See CONTRIBUTING.md

## License

See LICENSE.md
