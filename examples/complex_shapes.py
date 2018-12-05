'''
Use this as a guide for creating more complex shapes.  Code for generating
points on an ellipse and a hexagon are given.

'''
from pyphysicssandbox import *

import math

window("More Complex Shapes", 800, 800)

# Call this to get the points for a polygon to plot an ellipse centered
# on the given point with the given width and height
# The num_points is a suggestion, you'll get something close to that
# number of points
def ellipse_points(center_point, width, height, starting_angle, ending_angle, num_points):
    points = []
    x = center_point[0]
    y = center_point[1]
    
    for angle in range(starting_angle, ending_angle, int((ending_angle-starting_angle)/num_points)):
        x1 = width * math.cos(math.radians(angle))
        y1 = height * math.sin(math.radians(angle))
        points.append((x+x1, y+y1))
        
    return points

ellipse = ellipse_points((150, 150), 100, 50, 0, 359, 50)
polygon(ellipse)

# Note that the ending point is only approximately at
# 270 degrees
half_ellipse = ellipse_points((250, 250), 100, 50, 90, 270, 50)
polygon(half_ellipse)

# The points generated don't need to be used in a polygon.  If we
# only want a curve, we can generate lines instead.
curve = ellipse_points((350, 350), 100, 50, 90, 270, 50)
for current in range(len(curve)-1):
    line(curve[current], curve[current+1], 5)

# Call this to get the points for a polygon to plot
# a hexagon centered on the given point.  
def hexagon_points(center_point, side_length):
    height = side_length * math.sqrt(3)
    x1 = center_point[0] - side_length//2
    y1 = center_point[1] - height//2
    x2 = center_point[0] + side_length//2
    y2 = center_point[1] - height//2
    x3 = center_point[0] + side_length
    y3 = center_point[1]
    x4 = center_point[0] + side_length//2
    y4 = center_point[1] + height//2
    x5 = center_point[0] - side_length//2
    y5 = center_point[1] + height//2
    x6 = center_point[0] - side_length
    y6 = center_point[1]
    
    return ((x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6))
    
hexagon = hexagon_points((400, 600), 50)
polygon(hexagon)

draw ()
