'''
An example of how to do a one-click platform game.
PyPhysicsSandbox isn't designed for games, so we
have to work around some of the physics engine
features.

For example, to provide continuous movement for the
player, all the platforms are given the same surface
velocity.

This example just shows the possibilities.  You could
expand it to create power ups that allow jumping higher
or farther, some platforms that move faster or slower,
enemies that send the player back to the start, etc.
'''
from pyphysicssandbox import *

window_width = 1000
window_height = 600

window ("Simple platform game", window_width, window_height)

# The x component of the jump
jump_speed = 10000
# How much of a boost do walls give?
wall_boost = 5
# How fast does the player move?
move_speed = 100
# Is the player on the ground?
landed = True
# Direction of movement
# 1 for right, -1 for left
direction = 1

platforms = []
walls = []

def won_game(player, target, p):
    message = text_with_font((100, 100), "You Won!", "Comic Sans", 36)
    message.color = Color('red')
    deactivate (target)
    add_collision(player, message, landing)
    return False
    
def observer(keys):
    global landed
    
    # This prevents jumping in mid-air
    if landed:
        if mouse_clicked() or constants.K_SPACE in keys:
            landed = False
            player.hit((jump_speed*direction, -50000), player.position)
        
def landing(player, other, p):
    global landed
    landed = True
    return True

def reverse_direction(player, other, p):
    global direction
    
    direction *= -1
    
    for platform in platforms:
        platform.surface_velocity = (move_speed*direction, 0)
    
    # if the player hits a wall in midair, give them a bounce
    if not landed:
        player.hit((jump_speed*wall_boost*direction, -50000), player.position)
    
    return True

floor = static_box((0,window_height), window_width, 50)
platforms.append(floor)

left_wall = static_box((0,0), 5, window_height)
walls.append(left_wall)
right_wall = static_box((window_width-5, 0), 5, window_height)
walls.append(right_wall)
middle_wall = static_box((100, window_height-150), 5, 100)
walls.append(middle_wall)

platform = static_box ((window_width-100, window_height-50), 100, 5)
platforms.append(platform)

platform = static_box ((window_width-100, window_height-50), 100, 5)
platforms.append(platform)

platform = static_box ((window_width-250, window_height-100), 100, 5)
platforms.append(platform)

target = static_box((window_width-300, window_height-150), 20, 20)
target.color = Color("red")

player = box((20, window_height-20), 15, 15)
player.elasticity = 0.0

add_observer(observer)
add_collision(player, target, won_game)

for wall in walls:
    add_collision(player, wall, reverse_direction)
    
for platform in platforms:
    platform.surface_velocity = (move_speed, 0)
    add_collision(player, platform, landing)

run()
