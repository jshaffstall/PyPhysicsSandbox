"""
An example of using gears.  The screencast developing this code can be found
here: http://youtu.be/uYDVxDHjjxc?hd=1
"""

from pyphysicssandbox import *

def my_observer(keys):
    if constants.K_b in keys:
        ball1 = ball((125, 50), 10, 100)
        ball1.color = Color('green')

window('Gears', 300, 300)

arm1 = box((100, 90), 100, 10, 100)
arm1.color = Color("yellow")

pivot1 = pivot((150, 95))
pivot1.connect(arm1)

arm2 = box((100, 200), 100, 10, 100)
arm2.color = Color("blue")

pivot2 = pivot((150, 205))
pivot2.connect(arm2)

add_observer(my_observer)

gear(arm1, arm2)

run()
