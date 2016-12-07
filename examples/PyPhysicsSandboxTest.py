from pyphysicssandbox import *

# old_active = True
#
# def look_for_ball():
#     global b1
#     global old_active
#
#     if old_active != b1.active and not b1.active:
#         print ("Goodbye ball!")
#
#     old_active = b1.active
#
# set_observer(look_for_ball)

# step = 50
#
#
# def look_for_ball():
#     global step
#
#     if step == 0:
#         marble = ball((390,380),5)
#         marble.color = Color('black')
#         marble.hit(-800,-900)
#         step = 50
#     else:
#         step -= 1

# def look_for_ball():
#     global poly1
#
#     if mouse_pressed():
#         poly1.hit(0,-50)
#

#set_observer(look_for_ball)

window("My Window", 400, 300)
gravity(0.0, 500.0)

b1 = ball((100, 10), 30)
b1.color = Color('green')
b1.friction = 0.25
b1.group = 1

# poly2 = triangle((100, 5), (105, 15), (105, 0))
# poly2.color = Color('blue')
# poly2.group = 1
# poly2.paste_on(b1)

text2 = text((100, 10), "Hi")
text2.color = Color('green')
text2.group = 1
text2.paste_on(b1)

# line1 = line((100,5), (100,15), 1)
# line1.group = 1
# line1.paste_on(b1)

b2 = static_ball((98, 100), 30)
b2.color = Color('blue')

box1 = static_rounded_box((0, 290), 400, 10, 3)
box1.color = Color('red')
box1.surface_velocity = (-20, 0)

tri1 = triangle((260, 35), (250, 35), (240, -15))
tri1.color = Color('red')

poly1 = polygon(((195, 35), (245, 35), (220, -15)))
poly1.color = Color('blue')
poly1.wrap = True

text1 = text((200, 200), "Hello World")
text1.color = Color('green')
text1.wrap = True

box1 = box((150,20), 30, 30)

run()


