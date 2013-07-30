from SimpleCV import Color
from collections import deque

class ShollAnalyzer(object):
	"""
	An analayzer for quantitatively analyzing the morphological characteristics
	of an angiogram. This analyzer depends on the known position of the bead in
	the angiogram to perform the analysis using concentric circles.
	"""
	def __init__(self, img, bead):
		self.img = img
		self.bead = bead

		self.__crossings = {}
		self.__sproutCount = None
		self.__sproutMaximum = None

	def generateCircularCoordinates(self, origin, radius):
		"""
		Generator for circular coordinates starting from the x+ vector and
		iterates counterclockwise.

		Returns:
			A list of circular coordinates given a specified origin and radius
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
		initRadius = int(self.bead.radius() * 1.814)
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

		self.__crossings = crossings

		return crossings

	@property
	def crossings(self):
		return self.__crossings

	@property
	def sproutCount(self):
		if not self.__sproutCount:
			self.__sproutCount = sum(self.crossings.values()[:5]) / 5
		return self.__sproutCount


	@property
	def sproutMaximum(self):
		if not self.__sproutMaximum:
			self.__sproutMaximum = max(self.crossings.values())
		return self.__sproutMaximum
