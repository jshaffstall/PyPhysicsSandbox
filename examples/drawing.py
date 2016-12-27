"""
An example that shows how to use PyPhysicsSandbox for
early drawing assignments.

The screencast developing this code can be found here:

"""
from pyphysicssandbox import *
import random

window("A Bad Drawing Of A House", 400, 400)

color('red')
box((100, 200), 200, 200)
color('white')
box((190, 325), 25, 75)
box((150, 250), 25, 25)
box((250, 250), 25, 25)
color('green')
triangle((90, 200), (310, 200), (200, 25))

draw()



