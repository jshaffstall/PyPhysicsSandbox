"""SVG to Polygon conversion

This is still experimental code and only a tiny subset of SVG is supported.

Testing files were generated using Inkscape. Make sure to use "Make selected nodes corner" on all polygons to be converted so they contain no problematic SVG path commands!
"""

import re
import warnings
from xml.etree import ElementTree

from py2d import Polygon, Vector, Transform
from py2d.Bezier import flatten_cubic_bezier

def convert_svg(f, transform=Transform.unit(), bezier_max_divisions=None, bezier_max_flatness=0.1):
	"""Convert an SVG file to a hash of Py2D Polygons.

	The hash keys will be the ids set to the corresponding <path> elements in the SVG file.
	The hash value is a list of polygons, the first one being the outline polygon and all additional polygons being holes.

	@param f: File object or file name to a SVG file.

	@type transform: Transform
	@param transform: A transformation to apply to all polygons
	"""

	svg_ns = "http://www.w3.org/2000/svg"
	et = ElementTree.parse(f)

	def transform_element(e, transform):
		new_t = e.get("transform", "")

		nt = transform
		m = re.match(r'translate\((?P<x>[0-9.-]+),(?P<y>[0-9.-]+)\)', new_t)
		if m:
			x, y = float(m.group("x")), float(m.group("y"))
			nt = Transform.move(x,y) * nt

		m = re.match(r'matrix\((?P<a>[0-9.-]+),(?P<b>[0-9.-]+),(?P<c>[0-9.-]+),(?P<d>[0-9.-]+),(?P<e>[0-9.-]+),(?P<f>[0-9.-]+)\)', new_t)
		if m:
			a,b,c,d,e,f = ( float(m.group(l)) for l in "abcdef" )

			import pdb; pdb.set_trace()
			nt = Transform([[ a, c, e ],
			                [ b, d, f ],
					[ 0, 0, 1 ]]) * nt

		return nt

	def path_find(e, transform=Transform.unit()):
		"""Generator function to recursively list all paths under an element e"""

		# yield path nodes within current element
		for p in e.iterfind("{%s}path" % svg_ns):
			yield (p, transform_element(p, transform))

		# yield path nodes in subgroups
		for g in e.iterfind("{%s}g" % svg_ns):
			for p,t in path_find(g, transform_element(g, transform)):
				yield (p, t)


	def convert_element(e, transform):
		"""Convert an SVG path element to one or multiple Py2D polygons."""

		# get data from the <path> element
		id = e.get("id")
		d = e.get("d")

		#print "CONVERTING %s: %s" % (id, d)

		def parse_commands(draw_commands):
			"""Generator Function to parse a SVG draw command sequence into command and parameter tuples"""
			tokens = draw_commands.split(" ")
			while tokens:
				# find the next token that is a command
				par_index = next( i for i,v in enumerate(tokens[1:] + ["E"]) if re.match('^[a-zA-Z]$', v) ) + 1

				# first token should always be the command, rest the parameters
				cmd = tokens[0]
				pars = tokens[1:par_index]

				# remove the parsed tokens
				del tokens[:par_index]

				yield cmd, pars

		def parse_vec(s):
			x,y = s.split(",")
			return Vector(float(x), float(y))


		polys = []
		verts = []
		relative_pos = Vector(0.0,0.0)
		last_control = None
		for cmd, pars in parse_commands(d):

			#print "cmd: %s, pars: %s" % (cmd, pars)

			if cmd == "m" or cmd == "l":
				for p in pars:
					relative_pos += parse_vec(p)
					verts.append(relative_pos)


			elif cmd == "M" or cmd == "L":
				for p in pars:
					relative_pos = parse_vec(p)
					verts.append(relative_pos)

			elif cmd == "c" or cmd == "C":
				# create cubic polybezier

				for i in range(0, len(pars), 3):
					c1, c2, b = parse_vec(pars[i]), parse_vec(pars[i+1]), parse_vec(pars[i+2])

					if cmd == "c":
						# convert to relative
						c1 += relative_pos
						c2 += relative_pos
						b += relative_pos

					bez = flatten_cubic_bezier(relative_pos, b, c1, c2, bezier_max_divisions, bezier_max_flatness)

					last_control = c2
					relative_pos = b

					verts.extend(bez)

			elif cmd == "s" or cmd == "S":
				# shorthand / smooth cubic polybezier

				for i in range(0, len(pars), 2):
					c2, b = parse_vec(pars[i]), parse_vec(pars[i+1])
					c1 = relative_pos + (relative_pos - last_control)

					if cmd == "s":
						# convert to relative
						c2 += relative_pos
						b += relative_pos

					bez = flatten_cubic_bezier(relative_pos, b, c1, c2, bezier_max_divisions, bezier_max_flatness)

					last_control = c2
					relative_pos = b

					verts.extend(bez)

			elif cmd == "z":
				# close line by only moving relative_pos to first vertex

				polys.append(transform * Polygon.from_pointlist(verts))
				relative_pos = verts[0]
				verts = []


			else:
				warnings.warn("Unrecognized SVG path command: %s - path skipped" % cmd)
				polys = []
				break

		if verts:
			polys.append(transform * Polygon.from_pointlist(verts))
		#print "----"

		return id, polys

	out = {}
	for p,tr in path_find(et.getroot(), transform):
		id, polys = convert_element(p,tr)
		out[id] = polys

	return out

if __name__ == "__main__":
	print(convert_svg("py2d/examples/shapes.svg"))
