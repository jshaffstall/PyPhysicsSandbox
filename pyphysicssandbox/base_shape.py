import pygame
import pymunk
import math

from pyphysicssandbox import pin
from pyphysicssandbox import win_width
from pyphysicssandbox import win_height
from pyphysicssandbox import space
from pyphysicssandbox import add_observer


class BaseShape:
    next_collision_type = 0

    def __init__(self, cosmetic=False):
        self._cosmetic = cosmetic

        if cosmetic:
            self.body = None
            self.shape = []
        else:
            self.body.custom_gravity = space.gravity
            self.body.custom_damping = space.damping
            self.body.constant_velocity = None

        self.elasticity = 0.90
        self.friction = 0.6
        self._color = pygame.Color('black')
        self._wrap_x = False
        self._wrap_y = False
        self._active = True
        self._visible = True
        self._debug = False
        self.custom_velocity_func = False

        BaseShape.next_collision_type += 1
        self._collision_type = BaseShape.next_collision_type

        if type(self.shape) is list:
            for shape in self.shape:
                shape.collision_type = BaseShape.next_collision_type
        else:
            self.shape.collision_type = BaseShape.next_collision_type

        add_observer(self.observer)

    def observer(self, keys):
        if self._debug:
            print (repr(self))

    def hit(self, direction, position):
        if self._cosmetic:
            return

        self.body.apply_impulse_at_world_point(direction, position)

    def has_own_body(self):
        return not self._cosmetic

    def inside(self, p):
        mask = pygame.Surface((win_width, win_height))
        color = self.color
        self.color = pygame.Color('white')
        self._draw(mask)
        self.color = color

        mask.lock()
        pixel = mask.get_at(p)
        mask.unlock()

        return pixel == pygame.Color('white')

    def draw(self, screen):
        if self.visible:
            self._draw(screen)

    def paste_on(self, other_shape):
        p1, p2 = self._pin_points()

        pin(p1, self, p1, other_shape).visible = False
        pin(p2, self, p2, other_shape).visible = False

    @property
    def active(self):
        return self._active

    def deactivate(self):
        self._active = False

        if type(self.shape) is list:
            for s in self.shape:
                space.remove(s)

            if self.has_own_body():
                space.remove(self.body)
        else:
            if self.has_own_body():
                space.remove(self.shape, self.body)
            else:
                space.remove(self.shape)

    def reactivate(self):
        self._active = True

        if type(self.shape) is list:
            for s in self.shape:
                space.add(s)

            if self.has_own_body():
                space.add(self.body)
        else:
            if self.has_own_body():
                space.add(self.shape, self.body)
            else:
                space.add(self.shape)

    @property
    def angle(self):
        if self.body:
            return -math.degrees(self.body.angle)

        return 0.0

    @angle.setter
    def angle(self, value):
        if type(value) == float or type(value) == int:
            self.body.angle = math.radians(-value)
        else:
            print("Angle value must be a number")

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        if type(value) == bool:
            self._debug = value
        else:
            print("Debug value must be a boolean")

    @property
    def position(self):
        if self.body:
            return self.body.position

        return pymunk.vec2d.Vec2d(self._x, self._y)

    @position.setter
    def position(self, value):
        if type(value) == tuple and len(value) == 2:
            if self.body:
                self.body.position = value
            else:
                self._x = value.x
                self._y = value.y
        else:
            print("Position value must be a (x, y) tuple")

    @property
    def surface_velocity(self):
        if type(self.shape) is list:
            return self.shape[0].surface_velocity

        return self.shape.surface_velocity

    @surface_velocity.setter
    def surface_velocity(self, value):
        if type(value) == tuple and len(value)==2:
            if type(self.shape) is list:
                for shape in self.shape:
                    shape.surface_velocity = value
            else:
                self.shape.surface_velocity = value
        else:
            print("Surface velocity value must be a (x, y) tuple")

    @property
    def elasticity(self):
        if type(self.shape) is list:
            return self.shape[0].elasticity

        return self.shape.elasticity

    @elasticity.setter
    def elasticity(self, value):
        if type(value) == float:
            if type(self.shape) is list:
                for shape in self.shape:
                    shape.elasticity = value
            else:
                self.shape.elasticity = value
        else:
            print("Elasticity value must be a floating point value")

    @property
    def collision_type(self):
        return self._collision_type

    @property
    def friction(self):
        if type(self.shape) is list:
            return self.shape[0].friction

        return self.shape.friction

    @friction.setter
    def friction(self, value):
        if type(value) == float:
            if type(self.shape) is list:
                for shape in self.shape:
                    shape.friction = value
            else:
                self.shape.friction = value
        else:
            print("Friction value must be a floating point value")

    @property
    def wrap(self):
        return self._wrap_x or self.wrap_y

    @wrap.setter
    def wrap(self, value):
        if type(value) == bool:
            self._wrap_x = value
            self._wrap_y = value
        else:
            print("Wrap value must be True or False")

    @property
    def wrap_x(self):
        return self._wrap_x

    @wrap_x.setter
    def wrap_x(self, value):
        if type(value) == bool:
            self._wrap_x = value
        else:
            print("Wrap value must be True or False")

    @property
    def wrap_y(self):
        return self._wrap_y

    @wrap_y.setter
    def wrap_y(self, value):
        if type(value) == bool:
            self._wrap_y = value
        else:
            print("Wrap value must be True or False")

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        if type(value) == bool:
            self._visible = value
        else:
            print("Visible value must be True or False")

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if type(value) == pygame.Color:
            self._color = value
        else:
            print("Color value must be a Color instance")

    @property
    def group(self):
        if type(self.shape) is list:
            return self.shape[0].filter.group

        return self.shape.filter.group

    @group.setter
    def group(self, value):
        if type(value) == int:
            if type(self.shape) is list:
                for shape in self.shape:
                    shape.filter = pymunk.ShapeFilter(group=value)
            else:
                self.shape.filter = pymunk.ShapeFilter(group=value)
        else:
            print("Group value must be an integer")

    def _check_velocity_func(self):
        if not self.custom_velocity_func:
            self.custom_velocity_func = True
            self.body.velocity_func = adjust_velocity

    @property
    def gravity(self):
        if self._cosmetic:
            return 0, 0

        return self.body.custom_gravity

    @gravity.setter
    def gravity(self, value):
        if self._cosmetic:
            return

        if type(value) == tuple and len(value) == 2:
            self.body.custom_gravity = value
            self._check_velocity_func()
        else:
            print("Gravity value must be a (x, y) tuple")

    @property
    def damping(self):
        if self._cosmetic:
            return 0, 0

        return self.body.custom_damping

    @damping.setter
    def damping(self, value):
        if self._cosmetic:
            return

        if type(value) == float:
            self.body.custom_damping = value
            self._check_velocity_func()
        else:
            print("Damping value must be a float")

    @property
    def velocity(self):
        if self._cosmetic:
            return 0, 0

        return self.body.custom_velocity

    @velocity.setter
    def velocity(self, value):
        if self._cosmetic:
            return

        if type(value) == tuple and len(value) == 2:
            self.body.constant_velocity = value
            self._check_velocity_func()
        else:
            print("Velocity value must be an x,y tuple")

def adjust_velocity(body, gravity, damping, dt):
    if body.constant_velocity:
        body.velocity = body.constant_velocity
        return

    return body.update_velocity(body, body.custom_gravity, pow(body.custom_damping, dt), dt)
