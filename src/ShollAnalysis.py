from SimpleCV import Color
from collections import deque

class ShollAnalyzer(object):
	def __init__(self, img):
		self.img = img

	def shootCircle(self, origin, radius):
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

	def analyze(self, bead):
		initRadius = int(bead.radius() * 1.814)
		maxRadius = min([bead.x, bead.y, self.img.size()[0] - bead.x, self.img.size()[1] - bead.y])
		stepSize = 1

		lastPixel = Color.WHITE[0]
		counts = {}
		for r in range(initRadius, maxRadius, stepSize):
			counts.update({r: 0})
			for x, y in self.shootCircle(bead.origin(), r):
				pixel = self.img.getGrayPixel(x, y)
				if pixel != lastPixel and lastPixel == Color.WHITE[0]:
					counts[r] += 1
				lastPixel = pixel

		self.counts = counts

		return counts

	def sproutCount(self):
		return sum(self.counts.values()[:5]) / 5

	def sproutMaximum(self):
		return max(self.counts.values())
