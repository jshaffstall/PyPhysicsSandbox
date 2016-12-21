"""
An example of using springs on shapes.  The screencast developing this code can be found
here: http://youtu.be/ohSsodGpbj4?hd=1
"""

from pyphysicssandbox import *

window('Springs', 300, 300)

wheel = ball((50, 50), 25)
wheel.color = Color('blue')

pivot1 = pivot((100, 100))

spring((100, 100), pivot1, (50, 50), wheel, 25, 20000, 1000)

run()
