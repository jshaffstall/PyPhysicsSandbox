from pyPhysicsSandbox import *
import random

WIN_WIDTH = 600
WIN_HT = 600
window("Amelia's Test", WIN_WIDTH, WIN_HT)

# floor
base = static_box((0, 590), WIN_WIDTH, 10)
base.color = Color("black")

# arm1 = box((200, 200), 95, 10)
# arm1.color = Color("yellow")
#
# arm2 = box((300, 100), 10, 95)
# arm2.color = Color("yellow")
#
# arm3 = box((315, 200), 90, 10)
# arm3.color = Color("yellow")
#
# arm4 = box((300, 215), 10, 90)
# arm4.color = Color("yellow")
#
# pin = pin((305, 205))
# pin.connect(arm1)
# pin.connect(arm2)
# pin.connect(arm2)
# pin.connect(arm3)
#
# gear1 = gear(arm1, arm2, 90)
# gear2 = gear(arm2, arm3, 90)
# gear3 = gear(arm3, arm4, 90)

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

ball2 = ball((350, 0), 5)
ball2.color = Color("green")
ball2.draw_radius_line = True
ball2.wrap = True

gear(arm1, arm3)
motor = motor(arm1, -3)

def switch_gravity():
    if mouse_pressed():
        gravity(0, -900)

add_observer(switch_gravity)

# # # fulcrum
# # triangle = poly(((250, 450), (275, 500), (225, 500)))
# # triangle.color = Color("green")
# #
# # # lever
# # lever = poly(((50, 425), (65, 425), (65, 440), (450, 440), (450, 450), (50, 450)))
# # #lever = poly(((50, 200), (50, 450), (450, 450), (450, 440), (65, 440), (65, 200)))
# # lever.color = Color("darkblue")
# # lever.elasticity = 0.90
# #
# ball1 = ball((90, 425), 10)
# ball1.color = Color("green")
# ball1.wrap = True
#
# left = static_triangle((10, 10), (295, 300), (10, 590))
#
# right = static_triangle((590, 10), (305, 300), (590, 590))
#
# for y in range(10, 250, 4):
#     for x in range(10+y,590-y,4):
#         ball2 = ball((x, y), 2)
#         ball2.color = Color(random.randint(0,255),random.randint (0,255),random.randint (0,255))
#         ball2.elasticity = 0.0
#         ball2.friction = 0.3
#
# # for x in range(10, 590, 2):
# #     ball2 = ball((x, 10), 1)
# #     ball2.color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#
# # for x in range(0,600,60):
# #     tri1 = static_triangle((x+25, 450), (x, 400), (x+50, 400))
# #     tri1.color = Color(random.randint (0,255),random.randint (0,255), random.randint (0,255))
# #     tri1.elasticity = 1.0
#
#
# #
# # # bigger ball, initially off the top of the screen
# # ball2 = ball((425, -1000), 20)
# # ball2.color = Color("darkgreen")
# #
# # # bigger ball, farther off the top of the screen
# # ball3 = ball((325, -5000), 20)
# # ball3.color = Color("blue")
# #
# # text = text((90, 250), "Catapult")

# def look_for_ball():
#     global ball1
#
#     if mouse_pressed():
#         ball1.hit(0,-100)
#
# set_observer(look_for_ball)
#
# ball1 = ball((110, 580), 10)
# ball1.color = Color("blue")
# ball1.wrap = True
#
# ball2 = ball((150, 580), 10)
# ball2.color = Color("green")
#
# pin((100, 580), ball1, (150, 580), ball2)

run()



