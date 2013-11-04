from SimpleCV import Color, np

from NaiveStrategy import NaiveAnalysisStrategy
from PiecewiseConstantApproximation import fullPWConstants

from collections import deque

class AveragedAnalysisStrategy(NaiveAnalysisStrategy):
	def bind(self, img, crossings):
		super(NaiveAnalysisStrategy, self).bind(img, crossings)

	@property
	def sproutCount(self):
		return sum(self.crossings.values()[0:self.criticalValue]) / float(self.criticalValue)

class MedianAnalysisStrategy(NaiveAnalysisStrategy):
	def bind(self, img, crossings):
		super(NaiveAnalysisStrategy, self).bind(img, crossings)

	@property
	def sproutCount(self):
		return np.median(self.crossings.values()[0:self.criticalValue])
