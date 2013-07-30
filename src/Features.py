from SimpleCV import *
from numpy import *

class Bead(Circle):
	def __init__(self, img, circle):
		super(Bead, self).__init__(
			img, 
			circle.x, 
			circle.y, 
			circle.radius())

	def origin(self):
		return (self.x, self.y)

class Sprout(FeatureSet):
	def __init__(self, lines):
		self.extend(lines)

	def length(self, img, lines):
		return sum(line.length() for line in lines)

	def restore(self, color=Color.WHITE, width=1, distanceThreshold=20):
		connections = []
		for segmentInner in self:
			for segmentOuter in self:
				if segmentOuter == segmentInner:
					continue
				distance = spsd.euclidean(segmentInner.end, segmentOuter.start)
				if distance < distanceThreshold:
					connections.append((segmentInner, segmentOuter))

		for inner, outer in connections:
			self[-1].image.drawLine(inner.end, outer.start, color, width)

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
