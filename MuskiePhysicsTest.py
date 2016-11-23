from MuskiePhysics import *

window("My Window", 400, 300)
gravity(0.0, 500.0)

b1 = ball(100, 10, 30, 1)
b1.color = Color('green')

b2 = ball(98, 100, 30, 1, True)
b2.color = Color('blue')

box1 = static_rounded_box(0, 290, 400, 10, 3)
box1.color = Color('red')

#tri1 = triangle((195, 35), (245, 35), (220, -15))
#tri1.color = Color('blue')

poly1 = poly(((195, 35), (245, 35), (220, -15)))
poly1.color = Color('blue')
poly1.wrap = True

run()
