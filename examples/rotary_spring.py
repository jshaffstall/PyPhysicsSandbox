"""
An example of using rotary springs.  The screencast developing this code can be found
here: http://youtu.be/4Fpp8Y5g-dQ?hd=1
"""

from pyphysicssandbox import *

def my_observer(keys):
    if constants.K_b in keys:
        ball1 = ball((125, 50), 10, 100)
        ball1.color = Color('green')

window('Rotary Springs', 300, 300)

arm1 = box((100, 150), 100, 10, 100)
arm1.color = Color("yellow")

pivot1 = pivot((150, 155))
pivot1.connect(arm1)

add_observer(my_observer)

rotary_spring(arm1, pivot1, 0, 50000, 50000)
#rotary_spring(arm1, pivot1, 0, 20000000, 900000

run()
