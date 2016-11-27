from pyPhysicsSandbox import *

WIN_WIDTH = 690
WIN_HT = 300
window("Car Test", WIN_WIDTH, WIN_HT)

# floor
base = static_line((-100, 300), (1000, 220), 5)
base.color = Color("black")
base.friction = 1.0

base = line((100, 100), (200, 150), 5)
base.color = Color("black")
base.friction = 1.0

run()
