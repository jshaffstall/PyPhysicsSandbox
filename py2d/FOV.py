"""Calculation of polygonal Field of View (FOV)"""
import functools

import py2d.Math

class Vision:
	"""Class for representing a polygonal field of vision (FOV).

	It requires a list of obstructors, given as line strips made of lists of vectors (i.e. we have a list of lists of vectors).
	The vision polygon will be cached as long as the eye position and obstructors don't change.

		>>> obs = [[ py2d.Math.Vector(2,4), py2d.Math.Vector(4, 1), py2d.Math.Vector(7, -2) ],
		...        [ py2d.py2d.Math.Vector(1,-2), py2d.Math.Vector(6, -3) ],
		...	   [ py2d.Math.Vector(2.5,5), py2d.Math.Vector(3, 4) ]]
		>>> radius = 20
		>>> eye = py2d.Math.Vector(0,0)
		>>> boundary = py2d.Math.Polygon.regular(eye, radius, 4)
		>>> v = Vision(obs)
		>>> poly = v.get_vision(eye, radius, boundary)
		>>> poly.points[0:6]
		[Vector(4.000, 1.000), Vector(2.000, 4.000), Vector(2.000, 4.000), Vector(0.000, 20.000), Vector(0.000, 20.000), Vector(-20.000, 0.000)]
		>>> poly.points[6:]
		[Vector(-20.000, 0.000), Vector(-0.000, -20.000), Vector(-0.000, -20.000), Vector(1.000, -2.000), Vector(1.000, -2.000), Vector(6.000, -3.000), Vector(6.000, -3.000), Vector(7.000, -2.000), Vector(7.000, -2.000)]
	"""

	def __init__(self, obstructors, debug=False):
		"""Create a new vision object.

		@type obstructors: list
		@param obstructors: A list of obstructors. Obstructors are a list of vectors, so this should be a list of lists.
		"""

		self.set_obstructors(obstructors)
		self.debug = debug
		self.debug_points = []
		self.debug_linesegs = []

	def set_obstructors(self, obstructors):
		"""Set new obstructor data for the Vision object.

		This will also cause the vision polygon to become invalidated, resulting in a re-calculation the next time you access it.

		@type obstructors: list
		@param obstructors: A list of obstructors. Obstructors are a list of vectors, so this should be a list of lists.
		"""
		def flatten_list(l):
			return functools.reduce(lambda x,y: x+y, l)

		# concatenate list of lists of vectors to a list of vectors
		self.obs_points = flatten_list(obstructors)

		# convert obstructor line strips to lists of line segments
		self.obs_segs = flatten_list([ list(zip(strip, strip[1:])) for strip in obstructors ])

		self.cached_vision = None
		self.cached_position = None
		self.cached_radius = None

	def get_vision(self, eye, radius, boundary):
		"""Get a vision polygon for a given eye position and boundary Polygon.

		@type eye: Vector
		@param eye: The position of the viewer (normally the center of the boundary polygon)
		@type radius: float
		@param radius: The maximum vision radius (normally the radius of the boundary polygon)
		@type boundary: Polygon
		@param boundary: The boundary polygon that describes the maximal field of vision
		"""

		if self.cached_vision == None or (self.cached_position - eye).get_length_squared() > 1:
			self.calculate(eye, radius, boundary)

		return self.cached_vision


	def calculate(self, eye, radius, boundary):
		"""Re-calculate the vision polygon.

		WARNING: You should only call this if you want to re-calculate the vision polygon for some reason.

		For normal usage, use L{get_vision} instead!
		"""

		self.cached_radius = radius
		self.cached_position = eye
		self.debug_points = []
		self.debug_linesegs = []

		radius_squared = radius * radius


		closest_points = lambda points, reference: sorted(points, key=lambda p: (p - reference).get_length_squared())


		def sub_segment(small, big):
			return py2d.Math.distance_point_lineseg_squared(small[0], big[0], big[1]) < 0.0001 and py2d.Math.distance_point_lineseg_squared(small[1], big[0], big[1]) < 0.0001


		def segment_in_obs(seg):
			for line_segment in self.obs_segs:
				if sub_segment(seg, line_segment):
					return True
			return False

		def check_visibility(p):
			bpoints = set(boundary.points)

			if p not in bpoints:
				if (eye - p).get_length_squared() > radius_squared: return False
				if not boundary.contains_point(p): return False

			for line_segment in obs_segs:
				if py2d.Math.check_intersect_lineseg_lineseg(eye, p, line_segment[0], line_segment[1]):
					if line_segment[0] != p and line_segment[1] != p:
						return False

			return True

		def lineseg_in_radius(seg):
			return py2d.Math.distance_point_lineseg_squared(eye, seg[0], seg[1]) <= radius_squared

		obs_segs = filter(lineseg_in_radius, self.obs_segs)

		# add all obstruction points and boundary points directly visible from the eye
		visible_points = list(filter(check_visibility, set(self.obs_points + boundary.points )))

		# find all obstructors intersecting the vision polygon
		boundary_intersection_points = py2d.Math.intersect_linesegs_linesegs(obs_segs, list(zip(boundary.points, boundary.points[1:])) + [(boundary.points[-1], boundary.points[0])])

		if self.debug: self.debug_points.extend([(p, 0xFF0000) for p in visible_points])
		if self.debug: self.debug_points.extend([(p, 0x00FFFF) for p in boundary_intersection_points])

		# filter boundary_intersection_points to only include visible points
		# - need extra code here to handle points on obstructors!
		for line_segment in obs_segs:
			i = 0
			while i < len(boundary_intersection_points):
				p = boundary_intersection_points[i]

				if py2d.Math.distance_point_lineseg_squared(p, line_segment[0], line_segment[1]) > 0.0001 and py2d.Math.check_intersect_lineseg_lineseg(eye, p, line_segment[0], line_segment[1]):
					boundary_intersection_points.remove(p)
				else:
					i+=1

		visible_points += boundary_intersection_points

		poly = py2d.Math.Polygon()
		poly.add_points(visible_points)
		poly.sort_around(eye)

		i = 0
		while i < len(poly.points):
			p = poly.points[i-1]
			c = poly.points[i]
			n = poly.points[ (i+1) % len(poly.points) ]

			# intersect visible point with obstructors and boundary polygon
			intersections = set(
                py2d.Math.intersect_linesegs_ray(obs_segs, eye, c) + py2d.Math.intersect_poly_ray(boundary.points, eye, c))

			intersections = [ip for ip in intersections if ip != c and boundary.contains_point(ip)]


			if self.debug: self.debug_points.extend([(pt, 0x00FF00) for pt in intersections])
			if intersections:

				intersection = min(intersections, key=lambda p: (p - eye).length_squared)

				#if self.debug: self.debug_linesegs.append((0xFF00FF, [eye, intersection]))

				#if self.debug: print "%d prev: %s current: %s next: %s" % (i, p, c, n)

				sio_pc = segment_in_obs((p,c))
				sio_cn = segment_in_obs((c,n))

				if not sio_pc:
					#if self.debug: print "insert %s at %d" % (closest_intersection, i)
					poly.points.insert(i, intersection)
					i+=1


					# We might have wrongly inserted a point before because this insert was missing
					# and therefore the current-next check (incorrectly) yielded false. remove the point again
					if segment_in_obs((poly.points[i-3], poly.points[i-1])):
						#if self.debug: print "Fixing erroneous insert at %d" % (i-2)
						poly.points.remove(poly.points[i-2])
						i-=1

				elif sio_pc and not sio_cn:

					#if self.debug: print "insert %s at %d (+)" % (closest_intersection, i+1)
					poly.points.insert(i+1, intersection)
					i+=1

				#elif self.debug:
					#print "no insert at %i" % i


			i+=1

			#if self.debug: print "%d %d" % (i, len(poly.points))


		# handle border case where polypoint at 0 is wrongfully inserted before because poly was not finished at -1
		if segment_in_obs((poly.points[-1], poly.points[1])):
			poly.points[0], poly.points[1] = poly.points[1], poly.points[0]


		self.cached_vision = poly

		return poly



