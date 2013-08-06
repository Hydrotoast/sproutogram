from SimpleCV import *
from numpy import *

class Bead(Circle):
	"""
	The Bead feature describes a bead in an angiogram.
	"""
	def __init__(self, img, circle):
		super(Bead, self).__init__(
			img, 
			circle.x, 
			circle.y, 
			circle.radius())

	def origin(self):
		"""
		Returns the origin of the bead.

		:rtype: (int, int)
		"""
		return (self.x, self.y)

class Sprout(FeatureSet):
	"""
	The Sprout feature set describes a set of possible lines (possibly
	disjoint) that may comprise an individual sprout.
	"""
	def __init__(self, lines):
		self.extend(lines)

	def length(self, img, lines):
		"""
		Returns the length of the sprout in pixels.

		:rtype: (int)
		"""
		return sum(line.length() for line in lines)

	def restore(self, color=Color.WHITE, width=1, distanceThreshold=20):
		"""Attempts to restore the sprout segments by drawing on the image
		layers."""
		connections = []
		for inner in self:
			for outer in self:
				if outer == inner:
					continue
				distance = spsd.euclidean(inner.end, outer.start)
				if distance < distanceThreshold:
					connections.append((inner, outer))

		for inner, outer in connections:
			self[-1].image.drawLine(inner.end, outer.start, color, width)

class HLSG(Feature):
	"""
	The High-Level Sprout Geometry (HLSG) feature describes an angiogram by its
	bead and associated sprouts.
	"""
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
