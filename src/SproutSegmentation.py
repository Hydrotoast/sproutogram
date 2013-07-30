from SimpleCV import *

from Geometry import *
from SetForest import *
from Features import *

import utils

class SproutSegmenter(object):
	def injectImg(self, img):
		self.img = img

	def injectBeads(self, beads):
		self.beads = beads

	def findClosestBead(self, blob):
		closestBead = None
		closestDist = float('inf')
		for bead in self.beads:
			dist = euclidDistance((bead.x, bead.y), blob.centroid())
			if dist < closestDist:
				closestDist = dist
				closestBead = bead
		return bead

	def generateConnections(self, blobSegments, distanceThreshold=20):
		"""
		Generates hypothetical connections between blob segments if they are
		within a thresholded neighborhood of each other.

		Returns:
			A list of generated, hypothetical connections.
		"""
		connections = []
		for segmentOuter in blobSegments:
			for segmentInner in blobSegments:
				# Do not connect segments to each other
				if segmentOuter == segmentInner:
					continue
				distance = euclidDistance(segmentOuter.end, segmentInner.start)
				if distance < distanceThreshold:
					connections.append((segmentOuter, segmentInner))
		return connections

	def generateBlobSegments(self, blobs):
		"""
		Generates a list of linear approximations for blobs. That is, blobs are
		modeled as geometric rays defined radially outward.
		
		Returns:
			A list of generated rays defined radially outward.
		"""
		blobSegments = []
		if blobs:
			# Acquire blob segments
			for blob in blobs:
				bead = self.findClosestBead(blob)
				sortedContour = sorted(
					blob.contour(), 
					key = lambda x: euclidDistance(x, (bead.x, bead.y)))
				start = sortedContour[0]
				end = sortedContour[-1]

				radialSegment = RadialSegment(self.img, start, end, blob, bead)
				blobSegments.append(radialSegment)
		return blobSegments

	def generateSproutSegments(self, blobSegments, connections):
		"""
		Generates the sprout segments as lists of blobs.

		Returns:
			A list of sprout segments.
		"""
		setForest = SetForest(blobSegments)
		for connection in connections:
			setForest.union(
				setForest.find(connection[0]), 
				setForest.find(connection[1]))

		seen = set()
		blobMap = {}
		for segment in blobSegments:
			parent = setForest.find(segment)
			if parent not in seen:
				blobMap.update({parent: list(set([parent, segment]))})
				seen.add(parent)
			else:
				blobMap[parent].append(segment)

		sprouts = []
		for segments in blobMap.values():
			sprouts.append(Sprout(self.img, segments, segments[0].bead))

		# # --DEBUG
		# FeatureSet(blobSegments).draw(color=Color.RED, width=4)
		# sprouts = [Sprout(self.img, [segment], segment.bead) for segment in blobSegments]
		# FeatureSet(sprouts).draw(color=Color.BLUE, width=4)
		return sprouts

	def segment(self):
		blobs = self.img.findBlobs()
		
		if not blobs:
			return []

		blobSegments = self.generateBlobSegments(blobs)

		if not blobSegments:
			return []

		connections = self.generateConnections(blobSegments)
		sprouts = self.generateSproutSegments(blobSegments, connections)

		return sprouts
