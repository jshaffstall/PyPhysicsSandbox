# TODO: create this as an open source library for distribution
# https://jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/

# TODO: Expose motor's max torque

# TODO: Figure out how to do a slip gear

# TODO: automatically figure out a default mass for a shape based on its area?

# TODO: expose surface_velocity for conveyor belts
# on shape in pymunk

# TODO: add way to detect collisions between shapes
Code examples here: https://www.reddit.com/r/pygame/comments/2vogr6/pymunk_and_pygamehow_do_i_figure_out_which/

That code is bugged, here's the fixed code:

def smack(arbiter, space, data):
    if arbiter.is_first_contact: # is this the first frame contact was made?
        for shape in arbiter.shapes:
            shape.color = random.choice(["blue","green","yellow","purple","orange","red"])

space = pm.Space()
space.add_collision_handler(1, 1).post_solve=smack # calls the ball


The 1 and 1 being passed is a collision type.  Each shape needs to have a collision type
set, so I'll need to expose that (or set it automatically?)  Maybe each shape has a
unique collision type?







# TODO: expose surface_velocity of shape to allow conveyor belts
# need to experiment with what this means for polygons


https://coderwall.com/p/qawuyq/use-markdown-readme-s-in-python-modules
https://docs.python.org/2/distutils/setupscript.html
https://pythonhosted.org/an_example_pypi_project/setuptools.html

Can install py2d from the github source
https://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-dependencies

# TODO: Maybe use epydoc for generating HTML documentation from doc strings?
http://epydoc.sourceforge.net/

# TODO: tutorials on common tasks like collision detection
