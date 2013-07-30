from SimpleCV import Feature, Circle, Line
from numpy import array, argmin, argmax
from Geometry import euclidDistance

class Bead(Circle):
	def __init__(self, img, circle):
		super(Bead, self).__init__(
			img, 
			circle.x, 
			circle.y, 
			circle.radius())

	def origin(self):
		return (self.x, self.y)

class Sprout(Line):
	def __init__(self, img, lines, bead):
		minx = miny = float('inf')
		maxx = maxy = float('-inf')
		for (start, end) in [l.end_points for l in lines]:
			minx = min([minx, start[0], end[0]])
			miny = min([miny, start[1], end[1]])
			maxx = max([maxx, start[0], end[0]])
			maxy = max([maxy, start[1], end[1]])
		at_x = maxx - minx
		at_y = maxy - miny
		points = [(minx, miny), (maxx, miny),
			(minx, maxy), (maxx, miny)]

		# TODO: Fit a line based on line start/end points
		pointsDist = array([euclidDistance(p, (bead.x, bead.y)) for p in points])
		minPoint = argmin(pointsDist)
		maxPoint = argmax(pointsDist)

		super(Sprout, self).__init__(img, (points[minPoint], points[maxPoint]))

	def length(self, img, lines):
		return sum(line.length() for line in lines)

	def draw(self, color, width):
		self.image.drawLine(self.end_points[0], self.end_points[1], color, width)

class HLSG(Feature):
	def __init__(self, img, bead, sprouts):
		self.bead = bead
		self.sprouts = sprouts
		points = []
		super(HLSG, self).__init__(img, bead.x, bead.y, points)

	def __repr__(self):
		return "HLSG at (%d, %d) with %d sprouts" % (self.bead.x, self.bead.y, len(self.sprouts))

	def draw(self, color, width=4):
		self.bead.draw(color, width)
		for sprout in self.sprouts:
			sprout.draw(color, width)
