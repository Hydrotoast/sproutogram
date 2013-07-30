from SimpleCV import Line

from math import *

def euclidDistance(start, end):
	return sqrt((end[1] - start[1]) ** 2 + (end[0] - start[0]) ** 2)

class RadialSegment(Line):
	def __init__(self, img, start, end, blob=None):
		self.start = start
		self.end = end

		self.blob = blob
		super(RadialSegment, self).__init__(img, (start, end))
