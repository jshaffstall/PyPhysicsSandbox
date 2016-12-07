"""Bezier curve tools.

All functions in this module assume the following naming:

         C1           
         ____
        /    \      P2
        |     \______|          
	P1             
                       C2

A bezier curve is formed between two points P1 and P2, with curve direction coming from control points Ci.

References:
	www.caffeineowl.com/graphics/2d/vectorial/bezierintro.htm
"""

from py2d import distance_point_line


def point_on_cubic_bezier(p1,p2,c1,c2,t):
	"""Find a point on a cubic bezier curve, i.e. a bezier curve with two control points.
	
	@type p1: Vector
	@param p1: Start point of the curve
	
	@type p2: Vector
	@param p2: Stop point of the curve

	@type c1: Vector
	@param c1: Control point for point A

	@type c2: Vector
	@param c2: Control point for point B

	@type t: float
	@param t: Relative position on the bezier curve between 0 and 1
	"""

	one_minus_t = 1.0 - t
	one_minus_t_2 = one_minus_t * one_minus_t
	one_minus_t_3 = one_minus_t_2 * one_minus_t

	t_2 = t * t
	t_3 = t_2 * t

	return p1 * one_minus_t_3 + c1 * (3 * one_minus_t_2 * t) + c2 * (3 * one_minus_t * t_2) + p2 * t_3


def subdivide_cubic_bezier(p1,p2,c1,c2,t):
	"""Subdivide a cubic bezier curve and return the point on the curve plus new control points"""

	one_minus_t = 1.0 - t

	a = p1 * one_minus_t + c1 * t
	b = c1 * one_minus_t + c2 * t
	c = c2 * one_minus_t + p2 * t

	m = a * one_minus_t + b * t 
	n = b * one_minus_t + c * t

	p = m * one_minus_t + n * t

	return a,m,p,n,c


def flatten_cubic_bezier(p1,p2,c1,c2, max_divisions=None, max_flatness=0.1):
	out = []

	if not __is_flat(max_divisions, max_flatness, __bezier_flatness(p1,p2,c1,c2)):
		a,m,p,n,c = subdivide_cubic_bezier(p1,p2,c1,c2,0.5)

		md_rec = max_divisions - 1 if max_divisions else None

		out.extend(flatten_cubic_bezier(p1,p,a,m, md_rec, max_flatness))
		out.append(p)
		out.extend(flatten_cubic_bezier(p,p2,n,c, md_rec, max_flatness))

	return out


def point_on_quadratic_bezier(p1,p2,c,t):
	one_minus_t = 1.0 - t
	one_minus_t_2 = one_minus_t * one_minus_t

	t_2 = t * t

	return p1 * one_minus_t_2 + c * (2 * one_minus_t * t) + p2 * t_2


def subdivide_quadratic_bezier(p1,p2,c,t):
	one_minus_t = 1.0 - t
	
	a = p1 * one_minus_t + c * t
	b = c * one_minus_t + p2 * t

	p = a * one_minus_t + b * t

	return a,p,b

def flatten_quadratic_bezier(p1,p2,c, max_divisions=None, max_flatness=0.1):
	out = []
	if not __is_flat(max_divisions, max_flatness, __bezier_flatness(p1,p2,c)):
		_a,_p,_c = subdivide_quadratic_bezier(p1,p2,c,0.5)

		md_rec = max_divisions - 1 if max_divisions else None

		out.extend(flatten_quadratic_bezier(p1,_p,_a, md_rec, max_flatness))
		out.append(_p)
		out.extend(flatten_quadratic_bezier(_p,p2,_c, md_rec, max_flatness))

	return out

def __is_flat(max_divisions, max_flatness, flatness):
	return (max_divisions == 0) or (max_flatness != None and flatness <= max_flatness)

def __bezier_flatness(p1,p2, *c):
	return max(distance_point_line(cp, p1, p2) for cp in c)
