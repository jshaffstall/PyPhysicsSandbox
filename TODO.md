# TODO: Need to allow tying two objects together so they move as one
# Specifically putting text inside of another object would be nice if I need to special case it

# TODO: create this as an open source library for distribution
# https://jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/

# TODO: create __repr__ functions in the shape classes to show info during debugging

# TODO: Expose motor's max torque

# TODO: Figure out how to do a slip gear

# TODO: look at difference between dynamic bodies and kinematic bodies.
# Implement kinematic bodies?  They're controlled by code and not by physics.  Useful
# for things like elevators and doors.

# TODO: allow damping and gravity to be specified for each body
This https://github.com/viblo/pymunk/blob/0d79176cf2fd642bd2ce4005478cb8d6e37c1e9c/examples/breakout.py
shows setting a custom velocity function on a body.  That's for constant velocity, but might
be a start at allowing per body gravity and damping.

# TODO: move everything but the public interface into another module that
# gets imported here using import physics_util?  That would clean up autocomplete
# suggestions in IDEs

# TODO: add cosmetic text that gets drawn but is not involved in physics, and that
# you can change the text inside observer functions

# TODO: see if it's possible to change the text of text blocks that are involved in
# physics...can we alter the size of the box while the simulation is active?


