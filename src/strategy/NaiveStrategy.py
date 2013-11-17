from SimpleCV import Color, np

from AnalysisDescriptor import AnalysisStrategy
from PiecewiseConstantApproximation import fullPWConstants

from collections import deque
from operator import itemgetter

class NaiveAnalysisStrategy(AnalysisStrategy):
	def bind(self, img, crossings):
		super(AnalysisStrategy, self).__init__(img, crossings)

	@property
	def sproutCount(self):
		return self.crossings.values()[0]

	@property
	def criticalValue(self):
		return max(self.crossings.items(), key=itemgetter(1))[0]

	@property
	def sproutMaximum(self):
		return max(self.crossings.values())

	@property
	def ramificationIndex(self):
		if self.sproutCount == 0:
			return 0
		return self.sproutMaximum / self.sproutCount

	@property
	def branchingCount(self):
		return self.sproutMaximum - self.sproutCount

