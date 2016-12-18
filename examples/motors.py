"""
An example of using motors on shapes.  The screencast developing this code can be found
here: http://youtu.be/VtyRKKQBjfI?hd=1
"""

from pyphysicssandbox import *

window('Motors', 300, 300)
gravity(0, 0)
#gravity(0, 200)

wheel = ball((100, 100), 25)
wheel.color = Color('blue')
wheel.draw_radius_line = True
motor(wheel, 5)

line1 = line((100, 150), (100, 200), 5)
motor(line1, 1)

tri1 = triangle((170, 75), (150, 100), (190, 100))
tri1.color = Color('red')
motor(tri1, -3)

odd_shape = polygon(((200, 200), (185, 210), (170, 180), (210, 150)))
odd_shape.color = Color('green')
motor(odd_shape, 8)

#floor = static_box((0, 290), 300, 10)

run()
