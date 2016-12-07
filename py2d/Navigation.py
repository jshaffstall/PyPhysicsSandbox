"""Navigation Mesh generation and navigation."""

import itertools
from collections import defaultdict

import py2d.Math

def poly_midpoint_distance(poly_a, poly_b):
	"""Polygon distance function that takes the euclidean distance between polygon midpoints."""
	return (poly_a.get_centerpoint() - poly_b.get_centerpoint()).length

class NavMesh(object):
	"""Class for representing a navigation mesh"""

	def __init__(self, polygons):
		"""Create a new navigation mesh"""
		self._polygons = polygons
		self.update_nav()

	@staticmethod
	def generate(boundary, walls=[], distance_function=poly_midpoint_distance):
		"""Generate a new navigation mesh from a boundary polygon and a list of walls.

		The method will delete wall areas from the boundary polygon and then decompose the resulting polygon into convex polygons, generating a navigation graph in the process.

		@type boundary: Polygon
		@param boundary: The boundary of the navigable area.

		@type walls: List
		@param walls: List of Wall Polygons to subtract from the boundary polygon. These may intersect the polygon boundary or be properly inside the polygon.

		@type distance_function: Function
		@param distance_function: Function of the type f(p_a, p_b) that returns the distance between polygon objects p_a and p_b according to some metric.
		"""

		convex_decomp = py2d.Math.Polygon.convex_decompose(boundary, walls)

		# make NavPolygons out of the convex decomposition polygons
		polygons = [NavPolygon(poly) for poly in convex_decomp]

		# create dict of shared edges
		polygon_edges = defaultdict(list)
		for poly in polygons:
			for a,b in itertools.chain(zip(poly, poly[1:]), [(poly[-1],poly[0])]):
				c,d = (a,b) if a.x < b.x or (a.x == b.x and a.y < b.y ) else (b,a)
				polygon_edges[(c,d)].append(poly)

		# link polys that share edges
		for e, polys in polygon_edges.items():
			for i, p_a in enumerate(polys):
				for p_b in polys[i+1:]:

					dist = distance_function(p_a, p_b)

					p_a.neighbors[p_b] = (dist, e)
					p_b.neighbors[p_a] = (dist, e)

		return NavMesh(polygons)


	def update_nav(self):
		"""Pre-compute navigation data for the navigation mesh.

		This is called automatically upon mesh initialization, but you might want to call it if you have changed the navigation mesh.
		"""

		# initialize with simple distances
		self._nav_data = [
			[
				(q.neighbors[p][0], j) if p in q.neighbors.keys() else (float('inf'), None)
				for j, p in enumerate(self._polygons)
			]
			for i, q in enumerate(self._polygons)
		]

		# floyd-warshall algorithm to compute all-pair shortest paths
		for k in range(len(self._polygons)):
			for i in range( len(self._polygons) ):
				for j in range(len(self._polygons)):

					if k not in (i,j) and i != j:
						dist  = self.get_data(i,j)[0]
						dist2 = self.get_data(i,k)[0] + self.get_data(k,j)[0]
						if dist2 < dist:
							self.set_data(i,j, (dist2, k))

	def find_polygon(self, p):
		"""Find the NavPolygon that contains p"""
		for poly in self._polygons:
			if poly.contains_point(p):
				return poly

		return None


	def get_path(self, start, stop):
		"""Get a high-level path from start to stop.

		The path returned will be an optimal sequence of NavPolygons leading to the desired target.
		"""

		if isinstance(start, py2d.Math.Vector): start = self.find_polygon(start)
		if isinstance(stop, py2d.Math.Vector): stop = self.find_polygon(stop)

		if not (start and stop): return None

		def get_path_rec(i,j):

			if i == j:
				return []

			d = self.get_data(i,j)[1]

			if d == j:
				return [j]

			elif d == None:
				return None

			else:
				return get_path_rec(i,d) + get_path_rec(d,j)

		i = self._polygons.index(start)
		j = self._polygons.index(stop)

		path = get_path_rec(i,j)

		if path == None:
			return None

		path = [i] + path

		return NavPath(self, [self._polygons[p] for p in path])

	def get_data(self, i, j):
		return self._nav_data[i][j]

	def set_data(self, i, j, d):
		self._nav_data[i][j] = d

	def get_polygons(self):
		return self._polygons

	def get_nodes(self):
		return self._nodes

	polygons = property(get_polygons)
	nodes = property(get_nodes)


class NavPolygon(py2d.Math.Polygon):
	"""Polygon class with added navigation data"""
	def __init__(self, polygon):
		py2d.Math.Polygon.__init__(self)

		self.points = polygon.points
		self.neighbors = {}


class NavPath(object):
	"""Class representing a solved navigation path"""
	def __init__(self, mesh, polygons):
		self._mesh = mesh
		self._polygons = polygons


	def get_next_move_to(self, position, final_target):
		"""Get the next point an agent following this path should move to.

		Reference: Simple Stupid Funnel Algorithm
		http://digestingduck.blogspot.com/2010/03/simple-stupid-funnel-algorithm.html

		@type position: Vector
		@param position: The position of the agent following the path
		"""

		current_polys = []
		for poly in self._polygons:
			if poly.contains_point(position):
				current_polys.append(poly)

		i = max((self._polygons.index(p) for p in current_polys))

		if i == len(self._polygons)-1: return final_target

		edge = self._polygons[i].neighbors[self._polygons[i+1]][1]

		left, right = (edge[0], edge[1]) if py2d.Math.point_orientation(position, edge[0], edge[1]) else (edge[1], edge[0])

		for j in range(i+1, len(self._polygons)-1):
			edge = self._polygons[j].neighbors[self._polygons[j+1]][1]
			new_left, new_right = (edge[0], edge[1]) if py2d.Math.point_orientation(position, edge[0], edge[1]) else (edge[1], edge[0])

			# make the funnel smaller
			if py2d.Math.point_orientation(position, left, new_left): left = new_left
			if not py2d.Math.point_orientation(position, left, right):
				return right


			if not py2d.Math.point_orientation(position, right, new_right): right = new_right
			if not py2d.Math.point_orientation(position, left, right):
				return left

		if py2d.Math.point_orientation(position, left, final_target): left = final_target
		if not py2d.Math.point_orientation(position, left, right):
			return right

		if not py2d.Math.point_orientation(position, right, final_target): right = final_target
		if not py2d.Math.point_orientation(position, left, right):
			return left

		return final_target

	def get_polygons(self):
		return self._polygons

	polygons = property(get_polygons)
