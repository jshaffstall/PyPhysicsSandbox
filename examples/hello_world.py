"""
A traditional Hello World example for PyPhysicsSandbox.  A screencast showing the development
of this example can be found at:
"""

from pyphysicssandbox import *

window('Hello World', 300, 300)

floor = static_box((0, 290), 300, 10)
floor.color = Color('blue')

caption = text((125, 15), 'Hello World!')
caption.angle = 270
caption.wrap = True

run()

