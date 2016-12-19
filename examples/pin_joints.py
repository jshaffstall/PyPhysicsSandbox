"""
An example of using pin joints.  A screencast showing the development
of this example can be found at: http://youtu.be/Hq3y-ah6Lk0?hd=1
"""

from pyphysicssandbox import *

window("Pin Joints", 690, 300)

# floor
base = static_line((-100, 300), (1000, 220), 5)
base.color = Color("black")
base.friction = 1.0
base.elasticity = 0.0

wheel1 = ball((45, 200), 25, 100)
wheel1.color = Color(52, 219, 119)
wheel1.friction = 1.5
wheel1.elasticity = 0.0
wheel1.draw_radius_line = True

wheel2 = ball((155, 200), 25, 100)
wheel2.color = Color(52, 219, 119)
wheel2.friction = 1.5
wheel2.elasticity = 0.0
wheel2.draw_radius_line = True

chassis = box((75, 160), 50, 30, 100)
chassis.elasticity = 0.0

# The pin joints must connect to the center of the wheel or
# the car will flip as the wheels rotate.
pin((45, 200), wheel1, (75, 160), chassis)
pin((45, 200), wheel1, (75, 190), chassis)
pin((155, 200), wheel2, (125, 160), chassis)
pin((155, 200), wheel2, (125, 190), chassis)

motor(wheel1, 4)
motor(wheel2, 4)

run(True)
