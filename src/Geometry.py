from math import *

def euclidDistance(start, end):
	return sqrt((end[1] - start[1]) ** 2 + (end[0] - start[0]) ** 2)

class RadialSegment(object):
	def __init__(self, label, start, end, blob=None):
		self.label = label
		self.start = start
		self.end = end

		self.blob = blob

	def length(self):
		return euclidDistance(self.start, self.end)

	def __repr__(self):
		return "%s: from (%d, %d) to (%d, %d) with length %f" % (self.label,
			self.start[0], self.start[1], self.end[0], self.end[1],
			self.length())

class Sprout(object):
	def __init__(self, initRadialSegment):
		self.segments = [initRadialSegment]
		self.__centroid = [0, 0]

	def append(self, segment):
		self.segments.append(segment)
	
	def centroid(self):
		if self.__centroid != [0, 0]:
			return self.__centroid
		centroids = [segment.blob.centroid() for segment in self.segments]

		x_sum = 0
		y_sum = 0
		for centroid in centroids:
			x_sum += centroid[0]
			y_sum += centroid[1]

		self.__centroid[0] = x_sum // len(centroids)
		self.__centroid[1] = y_sum // len(centroids)

		return self.__centroid

	def __repr__(self):
		return "%s: at (%d, %d): %s" % (self.segments[0].label, self.centroid()[0], self.centroid()[1], [segment.label for segment in self.segments])

	def __eq__(self, other):
		return sorted(self.segments) == sorted(other.segments)
