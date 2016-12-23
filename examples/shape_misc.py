"""
An example of using shape methods and properties.  The screencast developing this code can be found
here: http://youtu.be/_eyE4xX_Gi8?hd=1
"""

from pyphysicssandbox import *

def hit_ball(keys):
    if mouse_clicked():
        ball1.hit((0, -400000), ball1.position)

    if constants.K_RIGHT in keys:
        floor.surface_velocity = (100, 0)
    elif constants.K_LEFT in keys:
        floor.surface_velocity = (-100, 0)

window('Shape Methods & Properties', 300, 300)

ball1 = ball((100, 100), 25)
ball1.color = Color('blue')
ball1.group = 1
ball1.elasticity = 0.0

text1 = text((85, 90), 'Hello')
text1.group = 1
text1.paste_on(ball1)

#text1.debug=True

floor = static_box((0, 290), 300, 10)
floor.elasticity = 0.0

add_observer(hit_ball)

run()
