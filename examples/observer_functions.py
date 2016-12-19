"""
An example of using observer functions.  The screencast developing this code can be found
here: http://youtu.be/XOQgwFivgR0?hd=1

Observer functions execute each time step.  The simulation runs at about 50 time steps per
second.
"""

from pyphysicssandbox import *

def my_observer(keys):
    global ball_point

    if constants.K_b in keys:
        ball1 = ball(ball_point, 10, 100)
        ball1.color = Color('green')

    if mouse_clicked():
        ball_point = mouse_point()

window('Observer Functions', 300, 300)

arm1 = box((100, 150), 100, 10, 100)
arm1.color = Color("yellow")

pivot1 = pivot((150, 155))
pivot1.connect(arm1)

ball_point = (125, 50)
add_observer(my_observer)

run()
