from pyPhysicsSandbox import *

WIN_WIDTH = 690
WIN_HT = 300
window("Car Test", WIN_WIDTH, WIN_HT)
gravity(0, 900)

# floor
base = static_line((-100, 300), (1000, 220), 5)
base.color = Color("black")
base.friction = 1.0
base.elasticity = 0.0

wheel1 = ball((45, 200), 25, 100)
wheel1.color = Color (52, 219, 119)
wheel1.friction = 1.5
wheel1.elasticity = 0.0

wheel2 = ball((155, 200), 25, 100)
wheel2.color = Color(52, 219, 119)
wheel2.friction = 1.5
wheel2.elasticity = 0.0

chassis = box((75, 160), 50, 30, 100)
chassis.elasticity = 0.0

pin((45, 200), wheel1, (75, 160), chassis)
pin((45, 200), wheel1, (75, 190), chassis)
pin((155, 200), wheel2, (125, 160), chassis)
pin((155, 200), wheel2, (125, 190), chassis)

motor(wheel1, chassis, 4)
motor(wheel2, chassis, 4)

run(True)
