import math
import numpy as np

from NaiveStrategy import NaiveAnalysisStrategy

from collections import OrderedDict
from operator import itemgetter


class AveragedAnalysisStrategy(NaiveAnalysisStrategy):
    def bind(self, img, crossings, bead):
        super(NaiveAnalysisStrategy, self).bind(img, crossings, bead)

    @property
    def sprout_count(self):
        return sum(self.crossings.values()[0:self.critical_value]) / float(self.critical_value)

    @property
    def troc_average(self):
        trocs = [self.critical_value]
        trocs_counter = self.sprout_maximum - 1
        start_radius = self.critical_value + 1
        ordered_items = OrderedDict(sorted(self.crossings.items()[start_radius:], key=itemgetter(0), reverse=True))
        while trocs_counter > 0 and len(ordered_items) > 0:
            radius, hits = ordered_items.popitem()
            diff = int(trocs_counter - math.floor(hits))
            if diff >= 0:
                trocs = trocs + [radius - self.bead.radius()] * diff
                trocs_counter -= diff
        print '\tTerminal Radius of Counts: %.2f' % np.mean(trocs)
        return np.mean(trocs)


class ThresholdAverageStrategy(NaiveAnalysisStrategy):
    def __init__(self):
        self.threshold = None

    def bind(self, img, crossings, threshold=10):
        super(NaiveAnalysisStrategy, self).bind(img, crossings)
        self.threshold = threshold

    @property
    def sprout_count(self):
        return sum(self.crossings.values()[0:self.threshold]) / float(self.threshold)


class MedianAnalysisStrategy(NaiveAnalysisStrategy):
    def bind(self, img, crossings):
        super(NaiveAnalysisStrategy, self).bind(img, crossings)

    @property
    def sprout_count(self):
        return np.median(self.crossings.values()[0:self.critical_value])


class ThresholdMedianAnalysisStrategy(NaiveAnalysisStrategy):
    def bind(self, img, crossings, threshold=10):
        super(NaiveAnalysisStrategy, self).bind(img, crossings)

    @property
    def sprout_count(self):
        return np.median(self.crossings.values()[0:self.threshold])

# class AveragedAdaptiveAnalysisStrategy(AveragedAnalysisStrategy):
# 	def bind(self, img, crossings):
# 		super(NaiveAnalysisStrategy, self).bind(img, crossings)
# 
# 	@property
# 	def sproutCount(self):
# 		return sum(self.crossings.values()[0:self.criticalValue]) / float(self.criticalValue)
# 
