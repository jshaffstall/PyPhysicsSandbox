import itertools
from py2d.Math.Vector import *
from py2d.Math.Operations import *

def tip_decorator_pointy(a,b,c,d,is_cw):
	intersection = intersect_line_line(a,b,c,d)
	return [intersection]

def tip_decorator_flat(a,b,c,d,is_cw):
	return []


class Polygon(object):
	"""Class for 2D Polygons.

	A Polgon behaves like a list of points, but the last point in the list is assumed to be connected back to the first point.
	"""

	def __init__(self):
		"""Create a new, empty Polygon object"""
		self.points = []

	@staticmethod
	def regular(center, radius, points):
		"""Create a regular polygon

		@type center: Vector
		@param center: The center point of the polygon

		@type radius: float
		@param radius: The radius of the polygon

		@type points: int
		@param points: The number of polygon points. 3 will create a triangle, 4 a square, and so on.
		"""

		angular_increment = 2 * math.pi / points

		p = Polygon()
		for i in range(points):
			p.add_point( Vector(center.x + radius * math.cos(i * angular_increment), center.y + radius * math.sin(i * angular_increment)) )

		return p

	@staticmethod
	def from_pointlist(points):
		"""Create a polygon from a list of points

		@type points: List
		@param points: List of Vectors that make up the polygon
		"""

		p = Polygon()
		p.points = points
		return p

	@staticmethod
	def from_tuples(tuples):
		"""Create a polygon from 2-tuples

		@type tuples: List
		@param tuples: List of tuples of x,y coordinates
		"""

		p = Polygon()
		p.points = [ Vector(t[0], t[1]) for t in tuples ]
		return p

	def add_point(self, point):
		"""Add a new point at the end of the polygon

		@type point: Vector
		@param point: The new Vector to add to the polygon
		"""
		self.points.append(point)

	def add_points(self, points):
		"""Add multiple new points to the end of the polygon

		@type points: List
		@param points: A list of Vectors to add
		"""
		self.points.extend(points)

	def get_centerpoint(self):
		"""Get the center of mass for the polygon"""

		xes = [p.x for p in self.points]
		yes = [p.y for p in self.points]

		return Vector(float(sum(xes)) / len(xes), float(sum(yes)) / len(yes) )

	def sort_around(self, center):
		"""Re-order points by their angle with respect to a certain center point"""

		def angle_from_origin(p):
			phi = math.acos(float(p.x) / p.get_length())
			if p.y < 0: phi = 2 * math.pi - phi
			return phi


		self.points.sort(key=lambda p: angle_from_origin(p - center))

	def __repr__(self):
		pts = ["(%.2f, %.2f)" % (p.x, p.y) for p in self.points]
		return "Polygon [%s]" % ", ".join(pts)

	def __getitem__(self, key):
		return self.points[key]

	def __setitem__(self, key, value):
		self.points[key] = value

	def __delitem__(self, key):
		del self.points[key]

	def __len__(self):
		return len(self.points)

	def __eq__(self, other):
		if not isinstance(other, Polygon): return False
		return self.points == other.points

	def clone(self):
		"""Return a shallow copy of the polygon (points are not cloned)"""
		poly = Polygon()
		poly.points = [ p for p in self.points ]
		return poly

	def clone_ccw(self):
		p = self.clone()
		if p.is_clockwise(): p.flip()
		return p

	def clone_cw(self):
		p = self.clone()
		if not p.is_clockwise(): p.flip()
		return p

	@staticmethod
	def boolean_operation(polygon_a, polygon_b, operation):
		"""Perform a boolean operation on two polygons.

		Reference:
		Avraham Margalit. An Algorithm for Computing the Union, Intersection or Difference of Two Polygons.
		Comput & Graphics VoI. 13, No 2, pp 167-183, 1989

		This implementation will only consider island-type polygons, so control tables are replaced by small boolean expressions.

		@type polygon_a: Polygon
		@param polygon_a: The first polygon

		@type polygon_b: Polygon
		@param polygon_b: The second polygon

		@type operation: char
		@param operation: The operation to perform. Either 'u' for union, 'i' for intersection, or 'd' for difference.
		"""

		def inorder_extend(v, v1, v2, ints):
			"""Extend a sequence v by points ints that are on the segment v1, v2"""

			k, r = None, False
			if v1.x < v2.x:
				k = lambda i: i.x
				r = True
			elif v1.x > v2.x:
				k = lambda i: i.x
				r = False
			elif v1.y < v2.y:
				k = lambda i: i.y
				r = True
			else:
				k = lambda i: i.y
				r = False

			l = [ (p, 2) for p in sorted(ints, key=k, reverse=r) ]

			i = next((i for i, p in enumerate(v) if p[0] == v2), -1)
			assert(i>=0)

			for e in l:
				v.insert(i, e)

		if operation not in 'uid' or len(operation) > 1: raise ValueError("Operation must be 'u', 'i' or 'd'!")

		# for union and intersection, we want the same orientation on both polygons. for difference, we want different orientation.
		matching_orientation = polygon_a.is_clockwise() == polygon_b.is_clockwise()
		if matching_orientation != (operation != 'd'):

			polygon_b = polygon_b.clone()
			polygon_b.flip()

		# initialize vector rings
		v_a = [(p, polygon_b.contains_point(p)) for p in polygon_a.points]
		v_b = [(p, polygon_a.contains_point(p)) for p in polygon_b.points]


		# find all intersections
		intersections_a = defaultdict(list)
		intersections_b = defaultdict(list)
		for a1, a2 in list(zip(v_a, v_a[1:])) + [(v_a[-1], v_a[0])]:
			for b1, b2 in list(zip(v_b, v_b[1:])) + [(v_b[-1], v_b[0])]:
				i = intersect_lineseg_lineseg(a1[0],a2[0],b1[0],b2[0])
				if i:
					intersections_a[(a1[0],a2[0])].append(i)
					intersections_b[(b1[0],b2[0])].append(i)


		# extend vector rings by intersections
		for k, v in intersections_a.iteritems():
			inorder_extend(v_a, k[0], k[1], v)

		for k, v in intersections_b.iteritems():
			inorder_extend(v_b, k[0], k[1], v)


		edge_fragments = defaultdict(list)

		def extend_fragments(v, poly, fragment_type):
			for v1, v2 in list(zip(v, v[1:])) + [(v[-1], v[0])]:
				if v1[1] == fragment_type or v2[1] == fragment_type:
					# one of the vertices is of the required type
					edge_fragments[v1[0]].append( v2[0] )

				elif v1[1] == 2 and v2[1] == 2:
					# we have two boundary vertices
					m = (v1[0] + v2[0]) / 2.0
					t = poly.contains_point(m)
					if t == fragment_type or t == 2:
						edge_fragments[v1[0]].append( v2[0] )

		fragment_type_a = 1 if operation == 'i' else 0
		fragment_type_b = 1 if operation != 'u' else 0

		extend_fragments(v_a, polygon_b, fragment_type_a)
		extend_fragments(v_b, polygon_a, fragment_type_b)

		def print_edge():
			for k in edge_fragments.keys():
				for v in edge_fragments[k]:
					print("%s -> %s" % (k, v))




		output = []
		while edge_fragments:
			start = edge_fragments.keys()[0]
			current = edge_fragments[start][0]
			sequence = [start]

			# follow along the edge fragments sequence
			while not current in sequence:
				sequence.append(current)
				current = edge_fragments[current][0]


			# get only the cyclic part of the sequence
			sequence = sequence[sequence.index(current):]

			for c,n in list(zip(sequence, sequence[1:])) + [(sequence[-1], sequence[0])]:
				edge_fragments[c].remove(n)

				if not edge_fragments[c]:
					del edge_fragments[c]



			output.append(Polygon.from_pointlist(Polygon.simplify_sequence(sequence)))

		return output

	@staticmethod
	def simplify_sequence(seq):
		"""Simplify a point sequence so that no subsequent points are on the same line"""

		i = 0
		while i < len(seq):
			p, c, n = seq[i-1], seq[i], seq[(i + 1) % len(seq)]

			if p == c or c == n or p == n or distance_point_lineseg_squared(c, p, n) < EPSILON:
				del seq[i]
			else:
				i+=1
		return seq


	@staticmethod
	def union(polygon_a, polygon_b):
		"""Get the union of polygon_a and polygon_b

		@type polygon_a: Polygon
		@param polygon_a: The first polygon

		@type polygon_b: Polygon
		@param polygon_b: The second polygon

		@return: A list of fragment polygons
		"""
		return Polygon.boolean_operation(polygon_a, polygon_b, 'u')

	@staticmethod
	def intersect(polygon_a, polygon_b):
		"""Intersect the area of polygon_a and polygon_b

		@type polygon_a: Polygon
		@param polygon_a: The first polygon

		@type polygon_b: Polygon
		@param polygon_b: The second polygon

		@return: A list of fragment polygons
		"""
		return Polygon.boolean_operation(polygon_a, polygon_b, 'i')

	@staticmethod
	def subtract(polygon_a, polygon_b):
		"""Subtract the area of polygon_b from polygon_a

		@type polygon_a: Polygon
		@param polygon_a: The first polygon

		@type polygon_b: Polygon
		@param polygon_b: The second polygon

		@return: A list of fragment polygons
		"""
		return Polygon.boolean_operation(polygon_a, polygon_b, 'd')


	@staticmethod
	def offset(polys, amount, tip_decorator=tip_decorator_pointy, debug_callback=None):
		"""Shrink or grow a polygon by a given amount.

		Reference:
		Xiaorui Chen and Sara McMains. Polygon Offsetting by Computing Winding Numbers
		Proceedings of IDETC/CIE 2005. ASME 2005 International Design Engineering Technical Conferences &
		Computers and Information in Engineering Conference

		@type polys: List
		@param polys: The list of polygons to offset. Counter-clockwise polygons will be treated as islands, clockwise polygons as holes.

		@type amount: float
		@param amount: The amount to offset. Positive values will grow the polygon, negative values will shrink.

		@type tip_decorator: function
		@param tip_decorator: A function used for decorating tips generated in the offset polygon
		"""

		# fix passing a single polygon instead of a poly list
		if isinstance(polys, Polygon): polys = [polys]

		if amount == 0: return polys

		def offset_poly(poly):
			r = []
			for i in range(len(poly.points)):
				c, n, n2 = poly.points[i], poly.points[ (i+1) % len(poly) ], poly.points[ (i+2) % len(poly) ]
				is_convex = point_orientation(c,n,n2)

				unit_normal = (n - c).normal().normalize()
				unit_normal2 = (n2 - n).normal().normalize()

				c_prime = c + unit_normal * amount
				n_prime = n + unit_normal * amount
				n2_prime = n2 + unit_normal2 * amount
				n_prime2 = n + unit_normal2 * amount

				r.append(c_prime)
				r.append(n_prime)

				if is_convex == (amount > 0):
					r.append(n)
				else:
					r.extend(tip_decorator(c_prime, n_prime, n_prime2, n2_prime, True))


			return r


		def decompose(poly_points):
			"""Decompose a possibly self-intersecting polygon into multiple simple polygons."""

			def inorder_extend(v, v1, v2, ints):
				"""Extend a sequence v by points ints that are on the segment v1, v2"""

				k, r = None, False
				if v1.x < v2.x:
					k = lambda i: i.x
					r = True
				elif v1.x > v2.x:
					k = lambda i: i.x
					r = False
				elif v1.y < v2.y:
					k = lambda i: i.y
					r = True
				else:
					k = lambda i: i.y
					r = False

				l = sorted(ints, key=k, reverse=r)
				i = next((i for i, p in enumerate(v) if p == v2), -1)
				assert(i>=0)

				for e in l:
					v.insert(i, e)

			pts = [p for p in poly_points]

			# find self-intersections
			ints = defaultdict(list)
			for i in range(len(pts)):
				for j in range(i+1, len(pts)):
					a = pts[i]
					b = pts[(i+1)%len(pts)]
					c = pts[j]
					d = pts[(j+1)%len(pts)]

					x = intersect_lineseg_lineseg(a, b, c, d)
					if x and x not in (a,b,c,d):
						ints[(a,b)].append( x )
						ints[(c,d)].append( x )


			# add self-intersection points to poly
			for k, v in ints.iteritems():
				inorder_extend(pts, k[0], k[1], v)

			# build a list of loops
			out = []
			while pts:

				# build up a list of seen points until we re-visit one - a loop!
				seen = []
				for p in pts + [pts[0]]:
					if p not in seen:
						seen.append(p)
					else:
						break

				loop = seen[seen.index(p):]

				# remove the loop from pts
				for p in loop:
					pts.remove(p)

				out.append(loop)

			return out


		def winding_number(p, raw):

			# compute winding number of point
			#http://softsurfer.com/Archive/algorithm_0103/algorithm_0103.htm

			wn = 0
			for pp in raw:
				for a,b in list(zip(pp, pp[1:])) + [(pp[-1], pp[0])]:
					if a.y < p.y and b.y > p.y:
						i = intersect_lineseg_ray(a,b,p,p+VECTOR_X)
						if i and i.x > p.x:
							wn -= 1

					if a.y > p.y and b.y < p.y:
						i = intersect_lineseg_ray(a,b,p,p+VECTOR_X)
						if i and i.x > p.x:
							wn += 1
			return wn


		def find_point_in_poly(pts):
			# find point inside of pts according to http://www.exaflop.org/docs/cgafaq/cga2.html#Subject%202.06:%20How%20do%20I%20find%20a%20single%20point%20inside%20a%20simple%20polygonu

			if len(pts) == 3: return (pts[0] + pts[1] + pts[2]) / 3


			# find convex point v
			v = None
			for i in range(len(pts)):
				a, v, b = pts[i-1], pts[i], pts[(i+1) % len(pts)]
				if not point_orientation(a,v,b): break


			q_s = [ q for q in pts if q not in [a,v,b] and point_in_triangle(q, a,v,b) ]

			if len(pts) >= 5:
				dbg(v, 0x000000, "V")
				dbg(a, 0x000000, "A")
				dbg(b, 0x000000, "B")

				for q in q_s:
					dbg(q, 0x000000, "Q")

			if q_s:
				# return the midpoint of the shortest diagonal qv
				q = min(q_s, key=lambda q: (q-v).length_squared )


				return (q - v) / 2.0 + v
			else:
				# no diagonal from v, return midpoint of ab instead
				return (b - a) / 2.0 + a



		def dbg(p, color, text):
			if debug_callback:
				debug_callback(p,color,text)


		raw = []
		for poly in polys:

			offset = offset_poly(poly)
			decomp = decompose( offset )

			raw.extend( decomp )


		#print "\n-----------------\n"
		output = []
		for poly in raw:

			poly = Polygon.simplify_sequence(poly)
			p = find_point_in_poly( poly )
			wn = winding_number(p, raw)


			dbg(p, 0xffff00, "%d %d" % (wn, len(poly)))
			#print "%d %d" % (wn, len(poly))

			# shrink: include poly in solution only if winding number of that region is greater than 1
			# grow: include only if winding number is 1
			if False or (amount < 0 and wn > 0) or (amount > 0 and wn == 1):
				output.append(Polygon.from_pointlist(poly))



		return output

	@staticmethod
	def convex_decompose(polygon, holes=[], debug_callback=None):
		"""Decompose a polygon into convex parts

		Reference:
		Jose Fernandez, Boglarka Toth, Lazaro Canovas and Blas Pelegrin. A practical algorithm for decomposing polygonal domains into convex polygons by diagonals
		Trabajos de Investigacion Operativa Volume 16, Number 2, 367-387.
		doi 10.1007/s11750-008-0055-2

		@type polygon: Polygon
		@param polygon: The possibly concave polygon to decompose.

		@type holes: List
		@param holes: A list of polygons inside of polygon to be considered as holes
		"""

		def dbg(p, c, t):
			if debug_callback: debug_callback(p,c,t)

		if polygon.is_self_intersecting(): return []
		if polygon.is_convex() and not holes: return [polygon]

		if not polygon.is_clockwise(): polygon = polygon.clone().flip()

		p = [v for v in polygon.points]
		out = []

		class G: pass
		g = G()
		g.del_index = 0

		def check_decomp(l, p_minus_l, p):
			"""check the decomposition l of polygon p"""
			l_v = [p[v] for v in l]

			xes = [v.x for v in l_v]
			x_min,x_max = min(xes), max(xes)

			yes = [v.y for v in l_v]
			y_min,y_max = min(yes), max(yes)

			def is_notch(i):
				return not point_orientation(p[i-1], p[i], p[(i+1) % len(p)])

			# extra criterion MP3: only accept if at least one of the diagonal points is a notch
			if not (is_notch(l[0]) or is_notch(l[-1])): return False
			if not Polygon.is_convex_s(l_v): return False

			# find only notches in p_minus_l that are within the axis-aligned bounding box of l
			pts = (v for v in p_minus_l if p[v].x <= x_max and p[v].x >= x_min and p[v].y <= y_max and p[v].y >= y_min and is_notch(v))

			# decomposition is invalid if any point in p is in l
			if pts:
				for v in pts:
					if Polygon.contains_point_s(l_v,p[v]) == 1: return False

				return True
			else:
				return True

		def handle_holes(l, d_a, d_b):

			# TODO add hole handling!

			closest_hole = None
			intersecting = True


			# check if the polygon intersects a hole
			closest_intersection = None
			while intersecting:
				intersecting = False
				for hole in holes:
					for a,b in list(zip(hole, hole[1:])) + [(hole[-1],hole[0])]:
						i = intersect_lineseg_lineseg(d_a, d_b, a, b)
						if i and i not in [a,b]:
							if not closest_intersection or (closest_intersection - d_b).length_squared > (i-d_b).length_squared:
								closest_intersection = i
								d_a = min([a,b], key = lambda v: (v-d_b).length_squared)
								closest_hole = hole
							intersecting = True

			# check if the polygon contains a hole
			if not closest_hole:
				closest_intersection = None
				for hole in holes:
					if Polygon.contains_point_s(l, hole[0]):
							i = min(hole, key = lambda v: (v- d_b).length_squared)
							if not closest_intersection or (closest_intersection - d_b).length_squared > (i-d_b).length_squared:
								closest_intersection = i
								d_a = i
								closest_hole = hole

			if closest_hole:
				absorb_hole(d_b, closest_hole, d_a)
				return False
			else:
				return True

		def handle_holes_convex():
			d_b = p[0]

			closest_intersection = None
			for hole in holes:
				i = min(hole, key=lambda v: (v-d_b).length_squared)
				if not closest_intersection or (closest_intersection - d_b).length_squared > (i-d_b).length_squared:
					closest_intersection = i
					d_a = i
					closest_hole = hole

			absorb_hole(d_b, closest_hole, d_a)


		def absorb_hole(d_b, closest_hole, d_a):

			holes.remove(closest_hole)
			if Polygon.is_clockwise_s(closest_hole): closest_hole = closest_hole.clone_ccw()

			i = closest_hole.points.index(d_a)
			j = p.index(d_b)

			extension = [d_b] + closest_hole.points[i:] + closest_hole.points[:i+1]

			p[j:j] = extension

			#print "hole!"




		def try_decompose(i_start):
			"""try to decompose p by a convex polygon starting at index i_start"""

			lookat = 1


			# find the next notch index
			i_extend = next( ( i for i in itertools.chain(range(i_start+1, len(p)), range(0,i_start+1)) if not point_orientation( p[i-1], p[i], p[(i+1) % len(p)] ) ) )

			# build provisional l
			l = list(range(i_start,i_extend+1)) if i_start < i_extend else list(range(i_start,len(p))) + list(range(0,i_extend+1))

			#print "l=%s" % l

			# remove elements from the end of l until we have a valid decomposition
			p_minus_l = [k for k in range(len(p)) if k not in l]
			while len(l) > 2 and not check_decomp(l, p_minus_l, p):
				l_pop = l.pop()
				p_minus_l.insert(0, l_pop)

			#print "l'=%s" % l

			# try to extend l counter-clockwise - find next notch
			i_extend2 = next( ( i for i in itertools.chain((i_start,-1,-1), range(len(p)-1,i_start, -1)) if not point_orientation( p[i-1], p[i], p[(i+1) % len(p)] ) ) )

			l2 =  list(range(i_extend2,len(p))) + list(range(0,i_start)) if i_extend2 > i_start else list(range(i_extend2,i_start))

			#print "l2=%s" % l2

			l = l2 + l

			# remove elements from the start of l until we have a valid decomposition
			p_minus_l = [k for k in range(len(p)) if k not in l]
			while len(l) > 2 and not check_decomp(l, p_minus_l, p):
				p_minus_l.append(l[0])
				del l[0]


			#print "l*=%s" % l

			#print "i_start=%d, i_extend=%d, i_extend2=%d" % (i_start, i_extend, i_extend2)

			# do we still have enough points for a convex poly? if not, give up for this starting point
			if len(l) <= 2: return False

			# we now have a diagonal l[0] , l[-1] creating the convex poly l


			# Does the diagonal cut a hole or does the new polygon contain a hole? if so, incorporate and try again
			if not handle_holes( [p[v] for v in l], p[l[0]], p[l[-1]]): return False

			# we didn't cross or contain any holes, make a poly and remove extaneous points
			#print "poly! %s" % l

			out.append(Polygon.from_pointlist([p[k] for k in l]))
			for v in sorted(l[1:-1], reverse=True):
				dbg(p[v], (255,0,255), "del %d" % g.del_index)
				g.del_index += 1
				del p[v]

			return True

		#print "-----"

		if Polygon.is_convex_s(p) and holes: handle_holes_convex()

		i = 0
		while len(p) > 3 and not Polygon.is_convex_s(p):
			if not try_decompose(i):
				i+= 1

			if Polygon.is_convex_s(p) and holes: handle_holes_convex()

			#print "......"

			i = i % len(p)



		if len(p) >= 3:
			out.append(Polygon.from_pointlist(p))
		elif len(p) > 0:
			raise Exception("There are some points left over: %s" % p)

		return out

	def is_self_intersecting(self):

		for i in range(len(self.points)):
			for j in range(i+1, len(self.points)):
				a = self.points[i]
				b = self.points[(i+1)%len(self.points)]
				c = self.points[j]
				d = self.points[(j+1)%len(self.points)]

				if not (b == c or d == a):
					if check_intersect_lineseg_lineseg(a, b, c, d): return True

		return False

	def is_clockwise(self):
		"""Determines whether the polygon has a clock-wise orientation."""
		return Polygon.is_clockwise_s(self.points)

	@staticmethod
	def is_clockwise_s(pts):
		# get index of point with minimal x value
		i_min = min(range(len(pts)), key=lambda i: pts[i].x)

		# get previous, current and next points
		a = pts[i_min-1]
		b = pts[i_min]
		c = pts[(i_min+1) % len(pts)]

		return point_orientation(a,b,c)


	def is_convex(self):
		"""Determines whether the polygon is convex."""
		return Polygon.is_convex_s(self.points)

	@staticmethod
	def is_convex_s(poly_points):
		"""Determines whether a sequence of points forms a convex polygon."""
		# get orientation of first point
		ori = point_orientation(poly_points[-1], poly_points[0], poly_points[1])

		for i in range(1,len(poly_points)):
			p, c, n = poly_points[i-1], poly_points[i], poly_points[(i+1) % len(poly_points)]

			if point_orientation(p,c,n) != ori:
				return False

		return True


	def flip(self):
		"""Reverses the orientation of the polygon"""
		self.points.reverse()
		return self

	def contains_point(self, p):
		"""Checks if p is contained in the polygon, or on the boundary.

		@return: 0 if outside, 1 if in the polygon, 2 if on the boundary.
		"""
		return Polygon.contains_point_s(self.points, p)

	@staticmethod
	def contains_point_s(pts, p) :
		"""Checks if the polygon defined by the point list pts contains the point p"""

		# see if we find a line segment that p is on
		for a,b in list(zip(pts[0:], pts[1:])) + [(pts[-1], pts[0])]:
			d = distance_point_lineseg_squared(p, a, b)
			if d < EPSILON * EPSILON: return 2

		# p is not on the boundary, cast ray and intersect to see if we are inside
		intersections = set(intersect_poly_ray(pts, p, p + Vector(1,0)))

		# filter intersection points that are boundary points
		for int_point in filter(lambda x: x in pts, intersections):

			i = pts.index(int_point)
			prv = pts[i-1]
			nxt = pts[(i+1) % len(pts)]

			if point_orientation(p, int_point, nxt) == point_orientation(p,int_point, prv):
				intersections.remove(int_point)

		# we are inside if we have an odd amount of polygon intersections
		return 1 if len(intersections) % 2 == 1 else 0

	def as_tuple_list(self):
		return [(p.x, p.y) for p in self.points]

	def get_width(self):
		return self.right - self.left

	def get_height(self):
		return self.bottom - self.top

	def get_left(self):
		return min(self.points, key=lambda p: p.x).x

	def get_right(self):
		return max(self.points, key=lambda p: p.x).x

	def get_top(self):
		return min(self.points, key=lambda p: p.y).y

	def get_bottom(self):
		return max(self.points, key=lambda p: p.y).y

	append = add_point
	extend = add_points

	center = property(get_centerpoint)

	left = property(get_left)
	right = property(get_right)

	top = property(get_top)
	bottom = property(get_bottom)

	width = property(get_width)
	height = property(get_height)
