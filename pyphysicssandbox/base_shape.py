import pygame
import pymunk


class BaseShape:
    def __init__(self):
        self.elasticity = 0.90
        self.friction = 0.6
        self.color = pygame.Color('black')
        self.wrap = False
        self._active = True
        self.visible = True

    def hit(self, x, y):
        self.body.apply_impulse_at_world_point((0, -200), (x, y))

    def has_own_body(self):
        return True

    def draw(self, screen):
        if self.visible:
            self._draw(screen)

    @property
    def active(self):
        return self._active

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
        return self._wrap

    @wrap.setter
    def wrap(self, value):
        if type(value) == bool:
            self._wrap = value
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
