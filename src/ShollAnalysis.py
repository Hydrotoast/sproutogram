from SimpleCV import Color

from collections import deque
import operator

import utils

class ShollAnalysisDescriptor(object):
	"""
	Descriptor for a Sholl Analysis containing the raw data dump of the
	analysis as well as other derivable calculations.
	"""
	def __init__(self, img, crossings):
		self.__img = img
		self.__crossings = crossings
		self.__sproutCount = None
		self.__criticalValue = None
		self.__sproutMaximum = None
		self.__ramificationIndex = None

	@property
	def img(self):
		"""Returns the image analyzed."""
		return self.__img

	@property
	def crossings(self):
		"""
		Returns a cached list of crossings as a function of radius. A crossing
		is an instance of an intersection with a concentric circle of specified
		radius with a sprout blob.

		:rtype: dictionary of {int: int}
		"""
		return self.__crossings

	@property
	def sproutCount(self):
		"""
		Returns a count of the primary sprouts. Primary sprouts are those
		sprouts which stem directly from the bead.

		:rtype: int
		"""
		if not self.__sproutCount:
			subs = utils.lis(self.crossings.values())
			self.__sproutCount = sum(subs) / len(subs)
		return self.__sproutCount

	@property
	def criticalValue(self):
		"""
		Returns the critical value which is defined to be the radius at which
		the maximum number of crossings occur.

		:rtype: int
		"""
		if not self.__criticalValue:
			self.__criticalValue = max(self.crossings.iteritems(), key=operator.itemgetter(1))[0]
		return self.__criticalValue

	@property
	def sproutMaximum(self):
		"""
		Returns the maximum number of crossings of all radii.

		:rtype: int
		"""
		if not self.__sproutMaximum:
			self.__sproutMaximum = max(self.crossings.itervalues())
		return self.__sproutMaximum

	@property
	def ramificationIndex(self):
		"""
		Returns the Shoenen Ramification Index which is a ratio for branching
		factor. This is calculated by dividing the sprout maximum with the
		number of primary sprouts.
		
		:rtype: float
		"""
		if not self.__ramificationIndex:
			self.__ramificationIndex = float(self.sproutMaximum) / float(self.sproutCount)
		return self.__ramificationIndex


class ShollAnalyzer(object):
	"""
	An analayzer for quantitatively analyzing the morphological characteristics
	of an angiogram. This analyzer depends on the known position of the bead in
	the angiogram to perform the analysis using concentric circles.
	"""
	def __init__(self, img, bead):
		self.img = img
		self.bead = bead

	def generateCircularCoordinates(self, origin, radius):
		"""
		Generator for circular coordinates starting from the x+ vector and
		iterates counterclockwise.

			>>> for x, y in analyzer.generateCircularCoordinates((0, 0), 5):
			>>>		print x, y

		:returns: A list of circular coordinates given a specified origin and radius
		"""
		x = radius
		y = 0
		radiusError = 1 - x

		octants = []
		for i in range(8):
			octants.append(deque())

		while x >= y:
			# x+ Q0
			octants[0].append((x + origin[0], -y + origin[1]))
			# y- Q1
			octants[1].appendleft((y + origin[0], -x + origin[1]))
			# y- Q2
			octants[2].append((-y + origin[0], -x + origin[1]))
			# x- Q3
			octants[3].appendleft((-x + origin[0], -y + origin[1]))
			# x- Q4
			octants[4].append((-x + origin[0], y + origin[1]))
			# y+ Q5
			octants[5].appendleft((-y + origin[0], x + origin[1]))
			# y+ Q6
			octants[6].append((y + origin[0], x + origin[1]))
			# x+ Q7
			octants[7].appendleft((x + origin[0], y + origin[1]))

			y += 1
			if radiusError < 0:
				radiusError += y << 2 + 1
			else:
				x -= 1
				radiusError += (y - x + 1) << 2

		for octant in octants:
			for point in octant:
				yield point

	def analyze(self, stepSize = 1):
		"""Returns a descriptor of the analysis.
		
		:rtype: ``ShollAnalysisDescriptor``"""
		initRadius = int(self.bead.radius() * 1.714)
		maxRadius = min([self.bead.x, self.bead.y, self.img.size()[0] -
			self.bead.x, self.img.size()[1] - self.bead.y])

		lastPixel = Color.BLACK[0]
		crossings = {}
		for r in range(initRadius, maxRadius, stepSize):
			crossings.update({r: 0})
			for x, y in self.generateCircularCoordinates(self.bead.origin(), r):
				pixel = self.img.getGrayPixel(x, y)
				if pixel != lastPixel and lastPixel == Color.WHITE[0]:
					crossings[r] += 1
				lastPixel = pixel

		return ShollAnalysisDescriptor(self.img, crossings)
