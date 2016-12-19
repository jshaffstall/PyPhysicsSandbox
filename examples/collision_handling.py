"""
An example of collision handling.  The screencast developing this code can be found
here: http://youtu.be/k3BR0qsB30E?hd=1
"""

from pyphysicssandbox import *
import random

def ball_hits_floor(ball1, floor, p):
    global count

    ball1.color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    #count += 1
    #if count > 10:
    #    return False

    return True

window('Collision Handling', 300, 300)
count = 0

floor = static_box((0, 290), 300, 10)
floor.color = Color('blue')

ball1 = ball((125, 100), 10, 100)
ball1.color = Color('green')

add_collision(ball1, floor, ball_hits_floor)

run()
