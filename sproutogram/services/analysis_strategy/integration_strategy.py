import math
from collections import OrderedDict
from operator import itemgetter

import numpy as np

from sproutogram.services.analysis_strategy.naive_strategy import NaiveAnalysisStrategy
from .piecewise_constant_approximation import approximate_piecewise_constants


class AveragedAnalysisStrategy(NaiveAnalysisStrategy):
    def bind(self, img, crossings, bead):
        super(NaiveAnalysisStrategy, self).bind(img, crossings, bead)

    @property
    def sprout_count(self):
        ordered_items = OrderedDict(sorted(self.crossings.items(), key=itemgetter(0)))[0:self.critical_value]
        return sum(ordered_items.values()) / float(self.critical_value)

    @property
    def total_branch_count(self):
        subs = approximate_piecewise_constants(self.crossings.values())
        diffs = [r - l for l, r in zip(subs[:-1], subs[1:]) if r > l]
        return sum(diffs)

    @property
    def auxiliary_branch_count(self):
        return self.total_branch_count - self.sprout_count

    @property
    def average_troc(self):
        trocs = [self.critical_value]
        trocs_counter = self.total_branch_count - 1
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


class AveragedSproutPostRisingEdge(AveragedAnalysisStrategy):
    @property
    def total_branch_count(self):
        return self.sprout_count + self.auxiliary_branch_count

    @property
    def auxiliary_branch_count(self):
        start_radius = self.critical_value
        ordered_items = OrderedDict(sorted(self.crossings.items(), key=itemgetter(0))[start_radius:])
        subs = approximate_piecewise_constants(ordered_items.values())
        diffs = [r - l for l, r in zip(subs[:-1], subs[1:]) if r > l]
        return sum(diffs)


class MPlusDelta2(AveragedAnalysisStrategy):
    @property
    def total_branch_count(self):
        return max(self.crossings.values()) + self.auxiliary_branch_count

    @property
    def auxiliary_branch_count(self):
        start_radius = self.critical_value
        ordered_items = OrderedDict(sorted(self.crossings.items(), key=itemgetter(0))[start_radius:])
        subs = approximate_piecewise_constants(ordered_items.values())
        diffs = [r - l for l, r in zip(subs[:-1], subs[1:]) if r > l]
        return sum(diffs)


class ThresholdAverageStrategy(NaiveAnalysisStrategy):
    def __init__(self):
        super(NaiveAnalysisStrategy, self).__init__()
        self.threshold = None

    def bind(self, img, crossings, bead, threshold=10):
        super(NaiveAnalysisStrategy, self).bind(img, crossings, bead)
        self.threshold = threshold

    @property
    def sprout_count(self):
        return sum(self.crossings.values()[0:self.threshold]) / float(self.threshold)


class MedianAnalysisStrategy(NaiveAnalysisStrategy):
    @property
    def sprout_count(self):
        return np.median(self.crossings.values()[0:self.critical_value])


class ThresholdMedianAnalysisStrategy(NaiveAnalysisStrategy):
    @property
    def sprout_count(self):
        return np.median(self.crossings.values()[0:self.threshold])
