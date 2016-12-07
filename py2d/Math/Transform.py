class Transform(object):
	"""Class for representing affine transformations"""

	def __init__(self, data):
		self.data = data

	@staticmethod
	def unit():
		"""Get a new unit tranformation"""
		return Transform([[1, 0, 0],
		                  [0, 1, 0],
		                  [0, 0, 1]])

	@staticmethod
	def move(dx, dy):
		"""Get a transformation that moves by dx, dy"""
		return Transform([[1, 0, dx],
		                  [0, 1, dy],
		                  [0, 0, 1]])

	@staticmethod
	def rotate(phi):
		"""Get a transformation that rotates by phi"""
		return Transform([[math.cos(phi), -math.sin(phi), 0],
		                  [math.sin(phi), math.cos(phi), 0],
		                  [0, 0, 1]])

	@staticmethod
	def rotate_around(cx, cy, phi):
		"""Get a transformation that rotates around (cx, cy) by phi"""
		return Transform.move(cx, cy) * Transform.rotate(phi) * Transform.move(-cx, -cy)

	@staticmethod
	def scale(sx, sy):
		"""Get a transformation that scales by sx, sy"""
		return Transform([[sx, 0, 0],
		                  [0, sy, 0],
		                  [0, 0, 1]])
	@staticmethod
	def mirror_x():
		"""Get a transformation that mirrors along the x axis"""
		return Transform([[-1, 0, 0],
		                  [ 0, 1, 0],
		                  [ 0, 0, 1]])

	@staticmethod
	def mirror_y():
		"""Get a transformation that mirrors along the y axis"""
		return Transform([[ 1, 0, 0],
		                  [ 0,-1, 0],
		                  [ 0, 0, 1]])

	def __add__(self, b):
		t = Transform()
		t.data = [[self.data[x][y] + b.data[x][y] for y in range(3)] for x in range(3)]
		return t

	def __sub__(self, b):
		t = Transform()
		t.data = [[self.data[x][y] - b.data[x][y] for y in range(3)] for x in range(3)]
		return t

	def __mul__(self, val):

		if isinstance(val, Vector):

			x = val.x * self.data[0][0] + val.y * self.data[0][1] + self.data[0][2]
			y = val.x * self.data[1][0] + val.y * self.data[1][1] + self.data[1][2]

			return Vector(x,y)

		elif isinstance(val, Transform):
			data = [[0 for y in range(3)] for x in range(3)]
			for i in range(3):
				for j in range(3):
					for k in range(3):
						data[i][j] += self.data[i][k] * val.data[k][j]

			return Transform(data)

		elif isinstance(val, Polygon):
			p_transform = [ self * v for v in val.points ]
			return Polygon.from_pointlist(p_transform)

		else:
			raise ValueError("Unknown multiplier: %s" % val)


