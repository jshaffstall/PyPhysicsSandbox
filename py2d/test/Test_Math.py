import unittest

class TestVector(unittest.TestCase):

	def setUp(self):

		
		self.u = Vector(3.0, 4.0)
		self.v = Vector(2.0, 3.0)
		self.w = Vector(0.5, 0.75)


		
		self.x = Vector(1, 0)
		self.y = Vector(0, 1)
		self.z = Vector(0, 0)

	def test_equality(self):
		self.assertNotEqual(self.v, self.w)
		self.assertEqual(self.v, Vector(2.0, 3.0))

	def test_add(self):
		self.assertEqual( Vector(2.5, 3.75), self.v + self.w )
		self.assertEqual( Vector(2.5, 3.75), self.w + self.v )

	def test_sub(self):
		self.assertEqual( Vector(1.5, 2.25), self.v - self.w )
		self.assertEqual( Vector(-1.5, -2.25), self.w - self.v )

	def test_mul_with_scalar(self):
		self.assertEqual( Vector(1, 1.5), self.w * 2 )
		self.assertEqual( Vector(1.0, 1.5), self.v * 0.5 )
	
	def test_mul_dot_product(self):
		self.assertEqual( 3.25 , self.v * self.w )

	def test_div(self):
		self.assertEqual( Vector(1.0, 1.5), self.v / 2 )
	
	def test_tuple(self):
		a,b = self.v.as_tuple()
		self.assertEqual( 2.0, a )
		self.assertEqual( 3.0, b )

	def test_key_access(self):
		self.assertEqual( 0.5, self.w[0] )
		self.assertEqual( 0.75, self.w[1] )

		self.w[0] = 9001
		self.w[1] = 42
		self.assertEqual( 9001, self.w.x)
		self.assertEqual( 42, self.w.y)


		try:
			x = self.w[2]
		except KeyError:
			pass
		else:
			self.fail("Expected KeyError")


		try:
			x = self.w["x"]
		except KeyError:
			pass
		else:
			self.fail("Expected KeyError")

		try:
			self.w[2] = 4
		except KeyError:
			pass
		else:
			self.fail("Expected KeyError")

		try:
			self.w["x"] = 4
		except KeyError:
			pass
		else:
			self.fail("Expected KeyError")


	def test_length(self):
		self.assertEqual( 5, self.u.length )
		self.assertEqual( 25, self.u.length_squared )

	def test_clone(self):
		self.assertEqual( Vector(0.5, 0.75), self.w.clone() )

	def test_clamp(self):
		self.assertEqual( Vector(0.6, 0.8), self.u.clamp() )
		self.assertEqual( Vector(0,0), self.z.clamp() )
		self.assertEqual( Vector(1,0), self.x.clamp() )

	def test_normal(self):
		self.assertEqual( Vector(-4, 3), self.u.normal())
	
	def test_repr(self):
		self.assertEqual( "Vector(3.000, 4.000)", str(self.u) )

	def test_hash(self):
		self.assertEqual( hash(self.u), hash(Vector(3.0, 2.0) + self.y * 2) )

	def test_slope(self):

		self.assertEqual(float('inf'), self.y.slope)
		self.assertEqual(1.5, self.v.slope)

class TestPolygon(unittest.TestCase):

	def setUp(self):
		self.square = Polygon.regular( Vector( 10.0, 30.0 ), 3, 4 )
		self.square2 = Polygon.regular( Vector( 5.0, 30.0), 4, 4 )
		self.triangle = Polygon.regular( Vector( 12.0, 32.0 ), 5, 3 )
		self.irregular = Polygon.from_pointlist( [ Vector(1, 1), Vector(0, 3), Vector(4, 5), Vector(3, 2) ] )

	def test_pointlen(self):
		self.assertEqual(3, len(self.triangle))
		self.assertEqual(4, len(self.square))


	def test_add_point(self):
		self.square.add_point( Vector(1,1) )
		self.assertEqual(5, len(self.square))
		self.assertEqual( Vector(1,1), self.square[4])

	def test_add_points(self):
		self.square.add_points( [Vector(1,1), Vector(2,2)] )
		self.assertEqual(6, len(self.square))
		self.assertEqual( Vector(1,1), self.square[4])
		self.assertEqual( Vector(2,2), self.square[5])

	def test_centerpoint(self):
		self.assertEqual( Vector( 12.0, 32.0 ), self.triangle.center )


	def test_sort_around(self):
		pts = [ Vector( 1.0, 3.0 ), Vector( -1.0, -2.0), Vector(2, -3), Vector(-2, 3), Vector(1,0), Vector(-1,0), Vector(0,-1), Vector(0,1)]
		pts_sorted = [ pts[4], pts[0], pts[7], pts[3], pts[5], pts[1], pts[6], pts[2] ]
		pts_sorted2 = [ pts[3], pts[0], pts[7], pts[5], pts[1], pts[6], pts[4], pts[2] ]

		poly = Polygon.from_pointlist(pts)
		
		poly.sort_around( Vector(0,0) ) 
		self.assertEqual( pts_sorted, poly.points )

		poly.sort_around( Vector(10,10) )
		self.assertEqual( pts_sorted2, poly.points )

	def test_repr(self):
		self.assertEqual("Polygon [(13.00, 30.00), (10.00, 33.00), (7.00, 30.00), (10.00, 27.00)]", str(self.square))

	def test_item_access(self):
		self.assertEqual( Vector(10, 33), self.square[1] )
		
		self.square[0] = Vector(12,34)
		self.assertEqual(Vector(12,34), self.square.points[0])

	def test_item_delete(self):
		del self.square[3]
		self.assertEqual(3, len(self.square))

	
	def test_clone(self):
		self.assertEqual(self.square.clone(), self.square)


	def test_clockwise(self):
		self.assertFalse(self.irregular.is_clockwise())

	def test_flip(self):
		self.irregular.flip()
		self.assertTrue(self.irregular.is_clockwise())

	def test_contains_point(self):

		self.assertEqual(1, self.irregular.contains_point(Vector(2,2)))
		self.assertEqual(1, self.irregular.contains_point(Vector(1,2)))
		self.assertEqual(2, self.irregular.contains_point(Vector(2,4)))
		self.assertEqual(2, self.irregular.contains_point(Vector(1,1)))
		self.assertEqual(2, self.irregular.contains_point(Vector(2,1.5)))
		self.assertEqual(0, self.irregular.contains_point(Vector(0,4)))
		self.assertEqual(0, self.irregular.contains_point(Vector(0,1)))
		self.assertEqual(0, self.irregular.contains_point(Vector(0,0)))



	def test_union(self):
		union = Polygon.union(self.square, self.square2)
		expected = [ Polygon.from_pointlist([Vector(13, 30), Vector(10,33), Vector(8,31), Vector(5,34), Vector(1,30), Vector(5,26), Vector(8,29), Vector(10,27) ]) ]
		for p in union:
			p.sort_around(Vector(8,30))

		self.assertEqual(expected, union)

	def test_intersection(self):
		intersection = Polygon.intersect(self.square, self.square2)
		for p in intersection:
			p.sort_around(Vector(8,30))

		expected = [ Polygon.from_tuples([(9.00, 30.00), (8.00, 31.00), (7.00, 30.00), (8.00, 29.00)]) ]
		self.assertEqual(expected, intersection)

	def test_subtract(self):
		subtract = Polygon.subtract(self.square, self.square2)
		for p in subtract:
			p.sort_around(Vector(8,30))
		
		expected = [ Polygon.from_tuples( [(13.00, 30.00), (9.00, 30.00), (10.00, 33.00), (8.00, 31.00), (8.00, 29.00), (10.00, 27.00)] )]
		self.assertEqual(expected, subtract)


	def test_offset(self):
		#self.square = Polygon.regular( Vector( 10.0, 30.0 ), 3, 4 )
		#self.square2 = Polygon.regular( Vector( 5.0, 30.0), 4, 4 )
		#self.triangle = Polygon.regular( Vector( 12.0, 32.0 ), 5, 3 )
		
		self.assertEqual( [Polygon.regular( Vector(10, 30), 5, 4) ], Polygon.offset([self.square], 2.0) )

class TestIntersection(unittest.TestCase):
	def setUp(self):

		self.origin = Vector(0,0)
		self.x = Vector(1,0)
		self.y = Vector(0,1)

		self.a = Vector(1, 3)
		self.b = Vector(5, 1)
		
		self.c = Vector(4, 2)
		self.d = Vector(1, 1)
		self.e = Vector(2, 4)
		self.f = Vector(-1, 0)

		self.square = Polygon.from_pointlist([ Vector(3, 3), Vector(-3, 3), Vector(-3, -3), Vector(3, -3) ])
		self.diamond = Polygon.regular(Vector(0,0), 5, 4)

	def test_intersect_lineseg_lineseg(self):
		self.assertTrue( check_intersect_lineseg_lineseg( self.a, self.b, self.origin, self.c ) )
		self.assertFalse( check_intersect_lineseg_lineseg( self.a, self.b, self.origin, self.d ) )

		
		self.assertEqual( Vector(3.5,1.75), intersect_lineseg_lineseg( self.a, self.b, self.origin, self.c ) )

	def test_intersect_lineseg_ray(self):
		self.assertEqual( Vector(3, 2), intersect_lineseg_ray(self.a, self.b, self.f, self.d) )
		self.assertEqual( None, intersect_lineseg_ray(self.a, self.b, self.d, self.f) )


	def test_intersect_poly_lineseg(self):
		self.assertEqual( [ Vector(-3, -1.5), Vector(3, 1.5) ], intersect_poly_lineseg( self.square.points, self.origin - self.c, self.c ) )
		self.assertEqual( [], intersect_poly_lineseg( self.diamond.points, self.origin, self.d ) )

	def test_intersect_poly_ray(self):
		self.assertEqual( [ Vector(3, 1.5) ], intersect_poly_ray(self.square.points, self.origin, self.c) )

	def test_intersect_line_line(self):
		self.assertEqual( Vector(3.5, 1.75), intersect_line_line( self.a, self.b, self.origin, self.c) )
		self.assertEqual( None, intersect_line_line(self.a, self.a + self.x * 3, self.origin, self.x) )

	def test_intersect_lineseg_line(self):
		self.assertEqual( Vector(1.4,2.8), intersect_lineseg_line(self.a, self.b, self.origin, self.e) )
		self.assertEqual( None, intersect_lineseg_line(self.origin, self.e.clamp(), self.a, self.b) )


	def test_intersect_poly_poly(self):
		self.assertEqual( [Vector(2, 3), Vector(-2, 3), Vector(-3, 2), Vector(-3, -2), Vector(-2, -3), Vector(2, -3), Vector(3, 2), Vector(3, -2)], intersect_poly_poly(self.square.points, self.diamond.points) )


	def test_distance_point_lineseg_squared(self):
		self.assertEqual( 3.2, distance_point_lineseg_squared(self.d, self.a, self.b) )
		self.assertEqual( 0, distance_point_lineseg_squared(Vector(2,4), Vector(0,3), Vector(4, 5)) )
		self.assertNotEqual( 0, distance_point_lineseg_squared(Vector(2,2), Vector(3,2), Vector(1, 1)) )

if __name__ == '__main__':
	unittest.main()
