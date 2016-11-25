from pyPhysicsSandbox import *
import random

WIN_WIDTH = 600
WIN_HT = 600
window("Amelia's Test", WIN_WIDTH, WIN_HT)
gravity(0.0, 500.0)

# floor
base = static_box((0, 590), WIN_WIDTH, 10)
base.color = Color("black")
#
# # fulcrum
# triangle = poly(((250, 450), (275, 500), (225, 500)))
# triangle.color = Color("green")
#
# # lever
# lever = poly(((50, 425), (65, 425), (65, 440), (450, 440), (450, 450), (50, 450)))
# #lever = poly(((50, 200), (50, 450), (450, 450), (450, 440), (65, 440), (65, 200)))
# lever.color = Color("darkblue")
# lever.elasticity = 0.90
#
ball1 = ball((90, 425), 10)
ball1.color = Color("green")
ball1.wrap = True

left = static_triangle((10, 10), (285, 300), (10, 590))
#left.friction = 0

right = static_triangle((590, 10), (315, 300), (590, 590))
#right.friction = 0

for y in range(10, 250, 10):
    for x in range(10+y,590-y,10):
        ball2 = ball((x, y), 5)
        ball2.color = Color(random.randint(0,255),random.randint (0,255),random.randint (0,255))

# for x in range(10, 590, 2):
#     ball2 = ball((x, 10), 1)
#     ball2.color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# for x in range(0,600,60):
#     tri1 = static_triangle((x+25, 450), (x, 400), (x+50, 400))
#     tri1.color = Color(random.randint (0,255),random.randint (0,255), random.randint (0,255))
#     tri1.elasticity = 1.0


#
# # bigger ball, initially off the top of the screen
# ball2 = ball((425, -1000), 20)
# ball2.color = Color("darkgreen")
#
# # bigger ball, farther off the top of the screen
# ball3 = ball((325, -5000), 20)
# ball3.color = Color("blue")
#
# text = text((90, 250), "Catapult")

run(True)



