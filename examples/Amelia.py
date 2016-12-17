from pyphysicssandbox import *
import random

WIN_WIDTH = 600
WIN_HT = 600
window("Amelia's Test", WIN_WIDTH, WIN_HT)

# floor
base = static_box((0, 590), WIN_WIDTH, 10)
base.color = Color("black")

base2 = cosmetic_rounded_box((20, 550), WIN_WIDTH, 10, 5)
base2.color = Color("black")

arm1 = box((100, 200), 100, 10, 100)
arm1.color = Color("yellow")
arm1.friction = 1.0

arm3 = box((345, 150), 10, 100)
arm3.color = Color("yellow")
arm3.friction = .90

pivot1 = pivot((105, 205))
pivot1.connect(arm1)

pivot2 = pivot((350, 200))
pivot2.connect(arm3)

ball1 = ball((110, 100), 5)
ball1.color = Color("blue")
ball1.wrap = True

# def ball_and_base(shape1, shape2, p):
#     return False
#
# add_collision(ball1, base, ball_and_base)

ball2 = ball((350, 0), 5)
ball2.color = Color("green")
ball2.draw_radius_line = True
ball2.wrap = True

for i in range(9000):
    ball3 = ball((random.randint(0, WIN_WIDTH), random.randint(0, WIN_HT)), 5)
    ball3.color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    #ball3.wrap = True

gear(arm1, arm3)
motor = motor(arm1, -3)


def switch_gravity(keys):
    if mouse_clicked():
        gravity(0, -100)

add_observer(switch_gravity)

run()



