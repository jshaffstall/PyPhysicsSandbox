"""Conversion of map data structures to obstructor data"""
import Math

def convert_tilemap(width, height, blocking_function, tile_width, tile_height):
	"""Convert a tile-based map file to obstructors for FOV calculation.

	>>> map_data = [[1,1,1,1,0,0,0,0],
	...	        [1,1,1,1,0,1,1,1],
	...	        [1,1,1,1,0,1,1,1],
	...    	        [1,1,0,0,0,1,1,1],
	...	        [1,1,0,0,0,1,1,1],
	...	        [0,0,0,0,0,1,1,1],
	...             [0,0,0,0,0,0,0,0]]
	>>> blocking_func = lambda x,y: map_data[x][y]
	>>> obstructors = convert_tilemap( len(map_data), len(map_data[0]), blocking_func, 1, 1)
	>>> print "\\n".join(map(str, obstructors))
	[Vector(0.000, 0.000), Vector(5.000, 0.000), Vector(5.000, 2.000), Vector(3.000, 2.000), Vector(3.000, 4.000), Vector(0.000, 4.000), Vector(0.000, 0.000)]
    	[Vector(1.000, 5.000), Vector(6.000, 5.000), Vector(6.000, 8.000), Vector(1.000, 8.000), Vector(1.000, 5.000)]
    	[Vector(0.000, 4.000), Vector(3.000, 4.000), Vector(3.000, 2.000), Vector(5.000, 2.000), Vector(5.000, 0.000), Vector(7.000, 0.000), Vector(7.000, 8.000), Vector(6.000, 8.000), Vector(6.000, 5.000), Vector(1.000, 5.000), Vector(1.000, 8.000), Vector(0.000, 8.000), Vector(0.000, 4.000)]

	@type width: int
	@param width: The width of the map in tiles
	@type height: int
	@param height: The height of the map in tiles

	@type blocking_function: function(x,y)
	@param blocking_function: The function with parameters x,y used to determine whether the tile at x,y blocks light. e.g.: C{lambda x,y: map.get_tile(x,y).block_light}

	@type tile_width: float
	@param tile_width: The width of a single tile

	@type tile_height: float
	@param tile_height: The height of a single tile
	"""


	def find_clusters():
		clusters = [[0 for i in range(height)] for j in range(width)]
		cluster_count = 0
		clusters_seen = set()

		def rename_cluster(old, new):
			#print "rename cluster %d --> %d" % (old, new)
			clusters_seen.remove(old)
			clusters_seen.add(new)
			
			for x in range(width):
				for y in range(height):
					if clusters[x][y] == old:
						clusters[x][y] = new 

		for x in range(width):
			for y in range(height):

				block = blocking_function(x,y)
				block_left = blocking_function(x-1, y) if x > 0 else False
				block_top = blocking_function(x,y-1) if y > 0 else False
	

				#print "x: %d\ty:%d" % (x,y)

				# merge tiles to clusters of the same blocking status by
				# assigning cluster numbers to them. Iterate over whole
				# map array and compare blocking statuses of tiles to the
				# left and to the top of the current tile. If they have
				# the same blocking status, take their cluster information.
				# If cluster informations differ, merge the clusters.
				# If differing blocking information, create new cluster.
					
				if block == block_left and block == block_top and x > 0 and y > 0:
					# clusters both to the left and the top.
					# merge clusters by overwriting all occurrences of the left cluster with the top cluster
					new_cluster = clusters[x][y-1]
					old_cluster = clusters[x-1][y]

					if new_cluster != old_cluster:
						rename_cluster(old_cluster, new_cluster)
					clusters[x][y] = new_cluster

					#print "x: %d\ty:%d: join left %d -> top %d" % (x,y, old_cluster, new_cluster)
				elif block == block_left and x > 0:
					# add to left cluster
					clusters[x][y] = clusters[x-1][y]
					#print "x: %d\ty:%d: use left %d" % (x,y, clusters[x-1][y])

				elif block == block_top and y > 0:
					# add to top cluster
					clusters[x][y] = clusters[x][y-1]
					#print "x: %d\ty:%d: use top %d" % (x,y, clusters[x][y-1])

				else:
					# no adjacent clusters, create a new one
					cluster_count += 1
					#print "x: %d\ty:%d: new cluster %d" % (x,y, cluster_count)
					clusters[x][y] = cluster_count
					clusters_seen.add(cluster_count)





		translation = {}
		cs = list(clusters_seen)
		for i in range(len(clusters_seen)):
			translation[cs[i]] = i + 1

		for x in range(width):
			for y in range(height):
				old = clusters[x][y]
				if(old > 0): clusters[x][y] = translation[old]

		return clusters, clusters_seen	

	
	def cluster_outline(cluster):

		def get_startpos():
			for x in range(width):
				for y in range(height):
					if clusters[x][y] == cluster:
						return x,y
		
		start_x, start_y = get_startpos()

		# directions:
		# 0: going right at the top of the cluster, 
		# 1: going down at the right of the cluster,
		# 2: going left at the bottom of the cluster, 
		# 3: going up at the left of the cluster.
		direction = 0

		x, y = start_x, start_y
		outline = [Math.Vector(x * tile_width, y * tile_height)]

		while True:

			right  = clusters[x+1][y] if x + 1 < width else 0
			top    = clusters[x][y-1] if y > 0 else 0
			left   = clusters[x-1][y] if x > 0 else 0
			bottom = clusters[x][y+1] if y + 1 < height else 0

			if direction == 0:
				# we are going right at the top of the cluster.

				if right == cluster and top != cluster:
					# everything is fine, follow along the path
					x += 1;
				elif top == cluster:
					# we have a cluster member at the top. 
					# go up now and add top-left corner to outline
					direction = 3
					outline.append(Math.Vector((x) * tile_width, (y) * tile_height))
					y -= 1;
				else:
					# we have no more cluster members to the right. 
					# go down now and add top-right corner to outline
					direction = 1
					outline.append(Math.Vector((x+1) * tile_width, (y) * tile_height))

			elif direction == 1:
				# we are going down at the right of the cluster.

				if bottom == cluster and right != cluster:
					# everything is fine, follow along the path
					y += 1;
				elif right == cluster:
					# we have a cluster member to the right.
					# go right now and add top-right corner to outline
					direction = 0
					outline.append(Math.Vector((x+1) * tile_width, (y) * tile_height))
					x += 1;
				else:
					# we have no more cluster members at the bottom.
					# go left now and add bottom-right corner to outline
					direction = 2
					outline.append(Math.Vector((x+1) * tile_width, (y+1) * tile_height))

			elif direction == 2:
				# we are going left at the bottom of the cluster.

				if left == cluster and bottom != cluster:
					# everything is fine, follow along the path
					x -= 1
				elif bottom == cluster:
					# we have a cluster member at the bottom.
					# go down now and add bottom-right corner to outline
					direction = 1
					outline.append(Math.Vector((x+1) * tile_width, (y+1) * tile_height))
					y += 1;
				else:
					# we have no more cluster members at the left.
					# go up now and add bottom-left corner to outline
					direction = 3
					outline.append(Math.Vector((x) * tile_width, (y+1) * tile_height))
			else:
				# we are going up at the left of the cluster.

				if top == cluster and left != cluster:
					# everything is fine, follow along the path
					y -= 1
				elif left == cluster:
					# we have a cluster member to the left.
					# go left now and add bottom-left corner to outline
					direction = 2
					outline.append(Math.Vector((x) * tile_width, (y+1) * tile_height))
					x -= 1;
				else:
					# we have no more cluster members at the top.
					# go right now and add top-left corner to outline
					direction = 0
					outline.append(Math.Vector((x) * tile_width, (y) * tile_height))
			
			# find if we've made a full loop and have come back to the start
			if direction == 0 and x == start_x and y == start_y:
				#outline += [outline[1]]
				break

		return outline

	
	clusters, clusters_seen = find_clusters()
	cluster_outlines = []

	for cluster in range(1, len(clusters_seen) + 1):
		cluster_outlines += [cluster_outline(cluster)]

	return cluster_outlines

