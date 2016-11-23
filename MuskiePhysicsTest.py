from MuskiePhysics import *

window("My Window", 400, 300)
gravity(0.0, 500.0)

b1 = ball(100, 10, 30, 1)
b1.color = Color('green')

b2 = ball(98, 100, 30, 1, True)
b2.color = Color('blue')

run()
