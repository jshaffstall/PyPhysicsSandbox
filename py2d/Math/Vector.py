import math
from collections import defaultdict

class Vector(object):
	"""Class for 2D Vectors.

	Vectors v have an x and y component that can be accessed multiple ways:

		- v.x, v.y
		- v[0], v[1]
		- x,y = v.as_tuple()

	"""

	def __init__(self, x, y):
		"""Create a new vector object.

		@type x: float
		@param x: The X component of the vector

		@type y: float
		@param y: The Y component of the vector
		"""

		self.x = x
		self.y = y


	def get_length(self):
		"""Get the length of the vector."""
		return math.sqrt(self.get_length_squared())

	def get_length_squared(self):
		"""Get the squared length of the vector, not calculating the square root for a performance gain"""
		return self.x * self.x + self.y * self.y;

	def get_slope(self):
		"""Get the slope of the vector, or float('inf') if x == 0"""
		if self.x == 0: return float('inf')
		return float(self.y)/self.x

	def normalize(self):
		"""Return a normalized version of the vector that will always have a length of 1."""
		return self / self.get_length()

	def clamp(self):
		"""Return a vector that has the same direction than the current vector, but is never longer than 1."""
		if self.get_length() > 1:
			return self.normalize()
		else:
			return self

	def clone(self):
		"""Return a copy of this vector"""
		return Vector(self.x, self.y)

	def normal(self):
		"""Return a normal vector of this vector"""
		return Vector(-self.y, self.x)

	def as_tuple(self):
		"""Convert the vector to a non-object tuple"""
		return (self.x, self.y)

	def __add__(self, b):
		return Vector(self.x + b.x, self.y + b.y)

	def __sub__(self, b):
		return Vector(self.x - b.x, self.y - b.y)

	def __mul__(self, val):

		if isinstance(val, Vector):
			return self.x * val.x + self.y * val.y
		else:
			return Vector(self.x * val, self.y * val)

	def __div__(self, val):
		return Vector(self.x / val, self.y / val)

	def __repr__(self):
		return "Vector(%.3f, %.3f)" % (self.x, self.y)

	def __eq__(self, other):
		if not isinstance(other, Vector): return False
		d = self - other
		return abs(d.x) < EPSILON and abs(d.y) < EPSILON

	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash("%.4f %.4f" % (self.x, self.y))

	def __getitem__(self, key):
		if key == 0: return self.x
		elif key == 1: return self.y
		else: raise KeyError('Invalid key: %s. Valid keys are 0 and 1 for x and y' % key)

	def __setitem__(self, key, value):
		if key == 0: self.x = value
		elif key == 1: self.y = value
		else: raise KeyError('Invalid key: %s. Valid keys are 0 and 1 for x and y' % key)

	length = property(get_length, None, None)
	length_squared = property(get_length_squared, None, None)

	slope = property(get_slope, None, None)

VECTOR_NULL = Vector(0,0)
VECTOR_X = Vector(1,0)
VECTOR_Y = Vector(0,1)
EPSILON = 0.0001
