from pyphysicssandbox import *

WIN_WIDTH = 500
WIN_HT = 600
window("Catapult", WIN_WIDTH, WIN_HT)
gravity(0.0, 500.0)

# floor
base = static_box((0, 500), WIN_WIDTH, 10)
base.color = Color("black")

# fulcrum
triangle = polygon(((250, 450), (275, 500), (225, 500)))
triangle.color = Color("green")

# lever
lever = polygon(((50, 390), (65, 390), (65, 430), (450, 430), (450, 450), (50, 450)))
lever.color = Color("darkblue")
lever.elasticity = 0.90

ball1 = ball((90, 425), 5)
ball1.color = Color("green")
ball1.wrap = True

ball4 = ball((110, 425), 5)
ball4.color = Color("green")
ball4.wrap = True

ball5 = ball((120, 425), 5)
ball5.color = Color("green")
ball5.wrap = True

# very heavy ball, off the top of the screen
ball2 = ball((425, -200), 20, 200000)
ball2.color = Color("darkgreen")

text = text((90, 250), "Catapult")

run(True)



