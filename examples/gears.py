"""
An example of using gears.  The screencast developing this code can be found
here:
"""

from pyphysicssandbox import *

def my_observer(keys):
    global ball_point

    if constants.K_b in keys:
        ball1 = ball(ball_point, 10, 100)
        ball1.color = Color('green')

window('Gears', 300, 300)

arm1 = box((100, 90), 100, 10, 100)
arm1.color = Color("yellow")

pivot1 = pivot((150, 95))
pivot1.connect(arm1)

ball_point = (125, 50)
add_observer(my_observer)

arm2 = box((100, 200), 100, 10, 100)
arm2.color = Color("blue")

pivot2 = pivot((150, 205))
pivot2.connect(arm2)

gear(arm1, arm2)

run()
