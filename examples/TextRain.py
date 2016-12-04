from pyphysicssandbox import *
import random

def drop_balls ():
    if random.randint(1, 50) == 1:
        for i in range(30):
            ball1 = ball((i*10, 10), 5)
            ball1.color = Color(random.randint(0,255), random.randint (0,255), random.randint (0,255))


def inc_counter():
    global counter

    if random.randint(1, 50) == 1:
        counter -= 1

        text1.text = '*'*counter
        text2.text = '*' * counter

window("Amelia's Test", 300, 600)
add_observer(drop_balls)

counter = 30
text1 = static_text((100, 100), '*'*counter)

text2 = cosmetic_text((100, 30), '*'*counter)

add_observer(inc_counter)

run()
