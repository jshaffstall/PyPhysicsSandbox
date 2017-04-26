from pyphysicssandbox import *
import random

window('Pinball', 600, 600)
gravity(0, 900)

lines = []
lines.append(static_line((450, 500), (550, 50), 3))
lines.append(static_line((150, 500), (50, 50), 3))
lines.append(static_line((550, 50), (300, 0), 3))
lines.append(static_line((300, 0), (50, 50), 3))
#lines.append(static_line((300, 180), (200, 200), 1))

for line in lines:
    line.elasticity = 0.7
    line.group = 1

tri1 = static_triangle((300, 180), (200, 200), (200, 100))
tri1.elasticity = 1.5

r_pos_x = 150
r_pos_y = 500

r_flipper = polygon(((r_pos_x-20, r_pos_y-20), (r_pos_x+140, r_pos_y), (r_pos_x-20, r_pos_y+20)), 100)
r_flipper.color = Color('blue')
r_flipper.group = 1

l_pos_x = 450
l_pos_y = 500

l_flipper = polygon(((l_pos_x+20, l_pos_y-20), (l_pos_x-140, l_pos_y), (l_pos_x+20, l_pos_y+20)), 100)
l_flipper.color = Color('blue')
l_flipper.group = 1

r_pivot = pivot((r_pos_x, r_pos_y))
r_pivot.connect(r_flipper)
rotary_spring(r_flipper, r_pivot, -0.15, 20000000, 900000)

l_pivot = pivot((l_pos_x, l_pos_y))
l_pivot.connect(l_flipper)
rotary_spring(l_flipper, l_pivot, 0.15, 20000000, 900000)


def flipper_hit(keys):
    if mouse_clicked():
        r_flipper.hit((0, -20000), (r_pos_x+120, r_pos_y))
        l_flipper.hit((0, -20000), (l_pos_x-120, l_pos_y))

    if constants.K_b in keys:
        ball1 = ball((250, 100), 25, 1)
        ball1.elasticity = 0.95
        add_collision(r_flipper, ball1, ball_flipped)

    if constants.K_t in keys:
        if tri1.active:
            deactivate(tri1)
        else:
            reactivate(tri1)

    if mouse_clicked() and tri1.inside(mouse_point()):
        if tri1.active:
            deactivate(tri1)
        else:
            reactivate(tri1)


add_observer(flipper_hit)


def ball_flipped(shape1, shape2, p):
    print('Collision')

    return True

run()

