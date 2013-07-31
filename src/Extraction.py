from math import *

from SimpleCV import *

from SetForest import *
from SproutSegmentation import *

class NoBeadException(Exception):
	pass

class ExtractorBase(object):
	def __init__(self, img):
		self.img = img

	def preprocess(self):
		"""Preprocesses a target image before feature extraction is
		performed."""
		pass

	def extract(self):
		"""
		Extracts a homogenous list of a single feature from a target image. The
		template first applies preprocessing steps and follows with feature
		extraction.

		Returns:
			A homogenous list of a single feature.
		"""
		pass

class BeadExtractor(ExtractorBase):
	"""
	Extracts bead features from a target image using a circular hough
	transformation to find the center and radius of the bead.
	"""
	def __init__(self, img):
		super(BeadExtractor, self).__init__(img)

	def preprocess(self):
		cannyMin, cannyMax = (100, 300)
		self.img = self.img.smooth(sigma=20)
		self.img = self.img.edges(cannyMin, cannyExtraction.py
	def extract(self):
		self.preprocess()
		circles = self.img.findCircle(canny=250, thresh=120, distance=150)
		if not circles:
			raise NoBeadException()
		beads = [Bead(self.img, circle) for circle in circles]
		return FeatureSet(beads)

class SproutExtractor(ExtractorBase):
	"""
	Extracts sprout features form a target image using segmentation
	strategies and computational geometry. Sprout features extracted
	from the image must belong to a specified bead.
	"""
	def __init__(self, img, beads, segmentStrat = SproutSegmenter()):
		self.beads = beads
		super(SproutExtractor, self).__init__(img)

		# Strategies
		self.segmentStrat = segmentStrat

	def maskBeads(self, img):
		"""Mask the beads."""
		maskedImg = img
		for bead in self.beads:
			goldenRatio = 1.614
			circleMask = Image(self.img.size())
			circleMask.dl().circle(
				(bead.x, bead.y),
				bead.radius() * goldenRatio,
				filled = True,
				color = Color.WHITE)
			circleMask = circleMask.applyLayers()
			maskedImg = maskedImg - circleMask
			maskedImg = maskedImg.applyLayers()
		return maskedImg

	def preprocess(self):
		cannyMin, cannyMax = (100, 300)
		dilateCount = 2
		imgEdges = self.img.edges(cannyMin, cannyMax)
		imgEdges = self.maskBeads(imgEdges)

		dilatedEdges = imgEdges.dilate(dilateCount)
		skeleton = dilatedEdges.skeletonize(3)

		self.img = skeleton

	def extract(self):
		self.preprocess()
		self.segmentStrat.injectImg(self.img)
		self.segmentStrat.injectBeads(self.beads)
		sprouts = self.segmentStrat.segment()
		return FeatureSet(sprouts)

class HLSGExtractor(ExtractorBase):
	"""
	Extracts High-Level Sprout Geometry (HLSG) features from a target image.
	These features include a heterogenous composition of lower-level features:
	a bead and sprouts.
	"""
	def __init__(self, img):
		super(HLSGExtractor, self).__init__(img)
	
	def preprocess(self):
		pass

	def maskBeads(self, beads):
		"""Mask the beads."""
		maskedImg = self.img
		for bead in beads:
			goldenRatio = 1.614
			circleMask = Image(self.img.size())
			circleMask.dl().circle(
				(bead.x, bead.y),
				bead.radius() * goldenRatio,
				filled = True,
				color = Color.WHITE)
			circleMask = circleMask.applyLayers()
			maskedImg = maskedImg - circleMask
			maskedImg = maskedImg.applyLayers()
		return maskedImg

	def mapSproutsToBeads(self, sprouts, beads):
		hlsgs = []
		hlsgsMapper = {}

		# Initialize mapper
		for bead in beads:
			hlsgsMapper[bead] = []

		# Map sprouts
		for sprout in sprouts:
			closestBead = None
			closestDist = float('inf')
			for bead in beads:
				dist = spsd.euclidean((bead.x, bead.y), sprout.points[0])
				if dist < closestDist:
					closestDist = dist
					closestBead = bead
			hlsgsMapper[closestBead].append(sprout)
		
		# Generate HLSGs
		for bead, sprouts in hlsgsMapper.items():
			hlsgs.append(HLSG(self.img, bead, sprouts))

		return hlsgs

	def extract(self):
		# Extract beads
		try:
			beadExtractor = BeadExtractor(self.img)
			beads = beadExtractor.extract()

			# Extract sprouts
			maskedImg = self.maskBeads(beads)
			sproutExtractor = SproutExtractor(maskedImg, beads)
			sprouts = sproutExtractor.extract()
			hlsgs = self.mapSproutsToBeads(sprouts, beads)

			return FeatureSet(hlsgs)
		except NoBeadException as e:
			return []
