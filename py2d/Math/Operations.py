def __intersect_line_line_u(p1, p2, q1, q2):

	d = (q2.y - q1.y) * (p2.x - p1.x) - (q2.x - q1.x) * (p2.y - p1.y)
	n1 = (q2.x - q1.x) * (p1.y - q1.y) - (q2.y - q1.y) * (p1.x - q1.x)
	n2 = (p2.x - p1.x) * (p1.y - q1.y) - (p2.y - p1.y) * (p1.x - q1.x)

	if d == 0: return None

	u_a = float(n1) / d
	u_b = float(n2) / d

	return (u_a, u_b)

def intersect_poly_lineseg(poly_points, p1, p2):
	"""Intersect a polygon and a line segment.

	@type poly_points: List
	@param poly_points: The list of points in the polygon

	@type p1: Vector
	@param p1: The starting point of the line segment

	@type p2: Vector
	@param p2: The ending point of the line segment

	@return: The list of intersection points or an empty list
	"""
	return intersect_linesegs_lineseg(list(zip(poly_points[0:], poly_points[1:])) + [(poly_points[-1], poly_points[0])], p1, p2)

def intersect_poly_ray(poly_points, p1, p2):
	"""Intersect a polygon and a ray

	@type poly_points: List
	@param poly_points: The list of points in the polygon

	@type p1: Vector
	@param p1: The starting point of the ray

	@type p2: Vector
	@param p2: The ending point of the ray

	@return: The list of intersection points or an empty list
	"""
	return intersect_linesegs_ray(list(zip(poly_points[0:], poly_points[1:])) + [(poly_points[-1], poly_points[0])], p1, p2)

def intersect_line_line(p1, p2, q1, q2):
	"""Intersect two lines

	@type p1: Vector
	@param p1: The first point of the first line

	@type p2: Vector
	@param p2: The second point of the first line

	@type q1: Vector
	@param q1: The first point of the second line

	@type q2: Vector
	@param q2: The second point of the second line

	@return: The point of intersection or None
	"""

	ll = __intersect_line_line_u(p1, p2, q1, q2)

	if ll == None: return None
	return Vector(p1.x + ll[0] * (p2.x - p1.x) , p1.y + ll[0] * (p2.y - p1.y) )

def intersect_lineseg_line(p1, p2, q1, q2):
	"""Intersect a line segment and a line

	@type p1: Vector
	@param p1: The starting point of the line segment

	@type p2: Vector
	@param p2: The ending point of the line segment

	@type q1: Vector
	@param q1: The first point on the line

	@type q2: Vector
	@param q2: The second point on the line

	@return: The point of intersection or None
	"""

	ll = __intersect_line_line_u(p1, p2, q1, q2)

	if ll == None: return None
	if ll[0] < 0 or ll[0] > 1: return None

	return Vector(p1.x + ll[0] * (p2.x - p1.x) , p1.y + ll[0] * (p2.y - p1.y) )

def intersect_lineseg_ray(p1, p2, q1, q2):
	"""Intersect a line segment and a ray

	@type p1: Vector
	@param p1: The starting point of the line segment

	@type p2: Vector
	@param p2: The ending point of the line segment

	@type q1: Vector
	@param q1: The first point on the ray

	@type q2: Vector
	@param q2: The second point on the ray

	@return: The point of intersection or None
	"""

	ll = __intersect_line_line_u(p1, p2, q1, q2)

	if ll == None: return None
	if ll[0] < 0 or ll[0] > 1: return None
	if ll[1] < 0: return None

	return Vector(p1.x + ll[0] * (p2.x - p1.x) , p1.y + ll[0] * (p2.y - p1.y) )

def intersect_linesegs_ray(segs, p1, p2):
	"""Intersect a list of line segments and a ray

	@type segs: List
	@param segs: The list of line segments, i.e. a list of 2-tuples of vectors

	@type p1: Vector
	@param p1: The first point on the ray

	@type p2: Vector
	@param p2: The second point on the ray

	@return: The list of intersections or an empty list
	"""
	intersect_points = []

	for line_segment in segs:
		intersect = intersect_lineseg_ray(line_segment[0], line_segment[1], p1, p2)
		if intersect:
			#if line_segment[0] != p2 and line_segment[1] != p2:
			intersect_points += [intersect]

	return intersect_points

def intersect_linesegs_lineseg(segs, p1, p2):
	"""Intersect a list of line segments and a line segment

	@type segs: List
	@param segs: The list of line segments, i.e. a list of 2-tuples of vectors

	@type p1: Vector
	@param p1: The first point on the line segment

	@type p2: Vector
	@param p2: The second point on the line segment

	@return: The list of intersections or an empty list
	"""
	intersect_points = []

	for line_segment in segs:
		intersect = intersect_lineseg_lineseg(line_segment[0], line_segment[1], p1, p2)
		if intersect:
			if line_segment[0] != p2 and line_segment[1] != p2:
				intersect_points += [intersect]

	return intersect_points

def intersect_poly_poly(poly_points1, poly_points2):
	"""Intersect two polygons

	@type poly_points1: List
	@param poly_points1: The list of points of polygon 1

	@type poly_points2: List
	@param poly_points2: The list of points of polygon 2

	@return: The list of intersections or an empty list
	"""

	return intersect_linesegs_linesegs(list(zip(poly_points1[0:], poly_points1[1:])) + [(poly_points1[-1], poly_points1[0])], list(zip(poly_points2[0:], poly_points2[1:])) + [(poly_points2[-1], poly_points2[0])])

def intersect_linesegs_linesegs(segs1, segs2):
	"""Intersect two lists of line segments

	@type segs1: List
	@param segs1: The first list of line segments, i.e. a list of 2-tuples of vectors

	@type segs2: List
	@param segs2: The second list of line segments, i.e. a list of 2-tuples of vectors

	@return: The list of intersections or an empty list
	"""
	intersect_points = []
	for ls1 in segs1:
		intersect_points += intersect_linesegs_lineseg(segs2, ls1[0], ls1[1])

	return intersect_points

def intersect_lineseg_lineseg(p1, p2, q1, q2):
	"""Intersect two line segments

	@type p1: Vector
	@param p1: The first point on the first line segment

	@type p2: Vector
	@param p2: The second point on the first line segment

	@type q1: Vector
	@param q1: The first point on the secondline segment

	@type q2: Vector
	@param q2: The second point on the second line segment
	"""

	if max(q1.x, q2.x) < min(p1.x, p2.x): return None
	if min(q1.x, q2.x) > max(p1.x, p2.x): return None
	if max(q1.y, q2.y) < min(p1.y, p2.y): return None
	if min(q1.y, q2.y) > max(p1.y, p2.y): return None

	ll = __intersect_line_line_u(p1, p2, q1, q2)

	if ll == None: return None
	if ll[0] < 0 or ll[0] > 1: return None
	if ll[1] < 0 or ll[1] > 1: return None

	return Vector(p1.x + ll[0] * (p2.x - p1.x) , p1.y + ll[0] * (p2.y - p1.y) )

def check_intersect_lineseg_lineseg(p1, p2, q1, q2):
	"""Check if two line segments intersect - this can conserve memory if we don't need the intersection points

	@type p1: Vector
	@param p1: The first point on the first line segment

	@type p2: Vector
	@param p2: The second point on the first line segment


	@type q1: Vector
	@param q1: The first point on the secondline segment

	@type q2: Vector
	@param q2: The second point on the second line segment

	"""

	if max(q1.x, q2.x) < min(p1.x, p2.x): return False
	if min(q1.x, q2.x) > max(p1.x, p2.x): return False
	if max(q1.y, q2.y) < min(p1.y, p2.y): return False
	if min(q1.y, q2.y) > max(p1.y, p2.y): return False

	ll = __intersect_line_line_u(p1, p2, q1, q2)

	if ll == None: return False
	if ll[0] < 0 or ll[0] > 1: return False
	if ll[1] < 0 or ll[1] > 1: return False

	return True

def distance_point_lineseg_squared(p, a, b):
	"""Get the shortest distance from a point to a line segment.

	This can either be a perpendicular to a point on the line segment or the straight connection of p to one of the end points.

	@type p: Vector
	@param p: The point to compare to the line segment

	@type a: Vector
	@param a: The first point on the first line segment

	@type b: Vector
	@param b: The second point on the first line segment
	"""


	ap = p - a
	ab = b - a
	bp = p - b

	r = float(ap * ab) / ab.length_squared

	if r <= 0: return ap.length_squared
	if r >= 1: return bp.length_squared

	s = ((a.y - p.y) * (b.x - a.x) - (a.x - p.x) * (b.y - a.y))

	return float(s * s) / ab.length_squared

	# ap_squared = (p - a).get_length_squared()
	# bp_squared = (p - b).get_length_squared()
	# ap_prime = a * b

	# perpendicular_squared = abs( ap_squared - ap_prime * ap_prime )

	# return min(ap_squared, bp_squared, perpendicular_squared)


def distance_point_line(p, a, b):
	return abs((p.x - a.x) * (b.y - a.y) - (p.y - a.y) * (b.x - a.x)) / math.sqrt((b.x - a.x) * (b.x - a.x) + (b.y - a.y) * (b.y - a.y))

def point_in_triangle(p, a,b,c):
	to = point_orientation(a,b,c)
	return point_orientation(a,b,p) == to and point_orientation(b,c,p) == to and point_orientation(a,p,c) == to

def point_orientation(a,b,c):
	"""Returns the orientation of the triangle a, b, c.

	Return True if a,b,c are oriented clock-wise.
	"""
	return (b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y) > 0

