"""
A simple example that shows how shapes initially placed overlapping will
try to move so they are not overlapping.  In this case we put too many
balls into a very small area and let them find their way out.

Note that we need to shift placement of the balls around a small area to
get uniform expansion when the simulation starts.  Putting them all on the
exact same spot expands them only in a horizontal line.

The screencast developing this code can be found here:
http://youtu.be/F8qSSoBz_o8?hd=1
"""
from pyphysicssandbox import *
import random

window("A tiny volcano", 400, 400)

static_line((225, 400), (175, 400), 15).color=Color('grey')
static_line((225, 400), (225, 300), 15).color=Color('grey')
static_line((175, 300), (175, 400), 15).color=Color('grey')
static_line((220, 275), (225, 300), 15).color=Color('grey')
static_line((175, 300), (180, 275), 15).color=Color('grey')

# We have to spread the balls out a bit to get uniform expansion,
# otherwise they all expand horizontally.
for i in range(500):
    ball1 = ball((200+random.randint(-1,1), 350+random.randint(-1,1)), 5)
    #ball1.color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    ball1.color = Color('red')

run()



