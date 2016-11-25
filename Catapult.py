from pyPhysicsSandbox import *

WIN_WIDTH = 500
WIN_HT = 600
window("Catapult", WIN_WIDTH, WIN_HT)
gravity(0.0, 500.0)

# floor
base = static_box((0, 500), WIN_WIDTH, 510)
base.color = Color("black")

# fulcrum
triangle = poly(((250, 450), (275, 500), (225, 500)))
triangle.color = Color("green")

# lever
lever = poly(((50, 425), (65, 425), (65, 440), (450, 440), (450, 450), (50, 450)))
#lever = poly(((50, 200), (50, 450), (450, 450), (450, 440), (65, 440), (65, 200)))
lever.color = Color("darkblue")
lever.elasticity = 0.50

ball1 = ball( (90, 425), 10)
ball1.color = Color("green")
ball1.wrap = True

# bigger ball, initially off the top of the screen
ball2 = ball( (425, -1000), 20)
ball2.color = Color("darkgreen")

# bigger ball, farther off the top of the screen
ball3 = ball( (425, -5000), 20)
ball3.color = Color("blue")


text
text = text ((90,250), "Catapult")

run()



