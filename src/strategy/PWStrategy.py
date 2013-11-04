from SimpleCV import Color, np

from NaiveStrategy import NaiveAnalysisStrategy
from PiecewiseConstantApproximation import fullPWConstants

from collections import deque
import utils

class PWAnalysisStrategy(NaiveAnalysisStrategy):
	"""
	Descriptor for a Sholl Analysis containing the raw data dump of the
	analysis as well as other derivable calculations.
	"""
	def bind(self, img, crossings):
		super(NaiveAnalysisStrategy, self).bind(img, crossings)

	@property
	def sproutCount(self):
		# subs = utils.lis(self.crossings.values())
		# subs = self.crossings.values()
		# print self.crossings
		u, subs = fullPWConstants(self.crossings.values())
		self._PWConstants = u
		self._PWsubs = subs
		# for i in range(len(subs)):
		# 	if subs[i] != 0:
		# 		self.__sproutCount = subs[i+1]
		# 		break
		return self.__sproutCount

	@property
	def criticalValue(self):
		return max(zip(self.crossings.keys(), self._PWsubs), key=operator.itemgetter(1))[0]

	@property
	def sproutMaximum(self):
		return max(self._PWsubs)
