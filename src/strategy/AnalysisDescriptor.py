from SimpleCV import Color, np

from PiecewiseConstantApproximation import fullPWConstants

from collections import deque
import operator

class AnalysisStrategy(object):
	def bind(self, img, crossings):
		self.integrationMethod = 'median'

		self.__img = img
		self.__crossings = crossings
		self.__sproutCount = None
		self.__criticalValue = None
		self.__sproutMaximum = None
		self.__ramificationIndex = None
		self.__branchingCount = None

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
		pass

	@property
	def criticalValue(self):
		"""
		Returns the critical value which is defined to be the radius at which
		the maximum number of crossings occur.

		:rtype: int
		"""
		pass

	@property
	def sproutMaximum(self):
		"""
		Returns the maximum number of crossings of all radii.

		:rtype: int
		"""
		pass

	@property
	def ramificationIndex(self):
		"""
		Returns the Shoenen Ramification Index which is a ratio for branching
		factor. This is calculated by dividing the sprout maximum with the
		number of primary sprouts.
		
		:rtype: float
		"""
		pass

	@property
	def branchingCount(self):
		"""
		Returns the branching count which is defined to be the number of branches
		which stem from initial sprouts i.e. sprout maximum - sprout count
		
		:rtype: float
		"""
		pass


class ShollAnalysisDescriptor(object):
	"""
	Descriptor for a Sholl Analysis containing the raw data dump of the
	analysis as well as other derivable calculations.
	"""
	def __init__(self, img, crossings, strategy=AnalysisStrategy()):
		self.strategy = strategy
		self.strategy.bind(img, crossings)
		# self.integrationMethod = 'median'

		self.__img = img
		self.__crossings = crossings
		self.__sproutCount = None
		self.__criticalValue = None
		self.__sproutMaximum = None
		self.__ramificationIndex = None
		self.__branchingCount = None

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
			self.__sproutCount = self.strategy.sproutCount
		return self.__sproutCount

	@property
	def criticalValue(self):
		"""
		Returns the critical value which is defined to be the radius at which
		the maximum number of crossings occur.

		:rtype: int
		"""
		if not self.__criticalValue:
			self.__criticalValue = self.strategy.criticalValue
		return self.__criticalValue

	@property
	def sproutMaximum(self):
		"""
		Returns the maximum number of crossings of all radii.

		:rtype: int
		"""
		if not self.__sproutMaximum:
			self.__sproutMaximum = self.strategy.sproutMaximum
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
			self.__ramificationIndex = self.strategy.ramificationIndex
		return self.__ramificationIndex

	@property
	def branchingCount(self):
		if not self.__branchingCount:
			self.__branchingCount = self.strategy.branchingCount
		return self.__branchingCount


