"""
A simple example that shows how shapes initially placed overlapping will
try to move so they are not overlapping.  In this case we put too many
balls into a very small area and let them find their way out.
"""
from pyphysicssandbox import *
import random

window("A tiny volcano", 400, 400)

static_line((225, 400), (175, 400), 5)
static_line((225, 400), (225, 300), 5)
static_line((175, 300), (175, 400), 5)
static_line((210, 275), (225, 300), 5)
static_line((175, 300), (190, 275), 5)

# We have to spread the balls out a bit to get uniform expansion,
# otherwise they all expand horizontally.
for i in range(150):
    ball1 = ball((200+random.randint(-1,1), 350+random.randint(-1,1)), 5)
    ball1.color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

run()



