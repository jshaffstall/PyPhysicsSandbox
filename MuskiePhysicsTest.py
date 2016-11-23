from MuskiePhysics import *

old_active = True


def look_for_ball ():
    global b1
    global old_active

    if old_active != b1.active and not b1.active:
        print ("Goodbye ball!")

    old_active = b1.active

step_function(look_for_ball)

window("My Window", 400, 300)
gravity(0.0, 500.0)

b1 = ball(100, 10, 30)
b1.color = Color('green')
b1.friction = 0.25

b2 = static_ball(98, 100, 30)
b2.color = Color('blue')

box1 = static_rounded_box(0, 290, 400, 10, 3)
box1.color = Color('red')

#tri1 = triangle((195, 35), (245, 35), (220, -15))
#tri1.color = Color('blue')

poly1 = poly(((195, 35), (245, 35), (220, -15)))
poly1.color = Color('blue')
poly1.wrap = True

run()
