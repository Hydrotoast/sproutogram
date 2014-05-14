from sproutogram.repositories.analysis import Analysis
from sproutogram.utils import lis
from piecewise_constant_approximation import approximate_piecewise_constants, full_piecewise_constants

from collections import OrderedDict
from operator import itemgetter

import math
import numpy as np


class AnalysisStrategy(object):
    def __init__(self):
        self.integration_method = 'median'

        self.__img = None
        self.__crossings = None
        self.__bead = None

    def bind(self, img, crossings, bead):
        self.__img = img
        self.__crossings = crossings
        self.__bead = bead

    def make_analysis_descriptor(self):
        if not self.__crossings:
            return Analysis(filename=self.__img.filename,
                            sprout_count=0,
                            critical_value=0,
                            total_branch_count=0,
                            auxiliary_branch_count=0,
                            branching_factor=0,
                            average_troc=0)
        return Analysis(filename=self.__img.filename,
                        sprout_count=self.sprout_count,
                        critical_value=self.critical_value,
                        total_branch_count=self.total_branch_count,
                        auxiliary_branch_count=self.auxiliary_branch_count,
                        branching_factor=self.branching_factor,
                        average_troc=self.average_troc)

    @property
    def bead(self):
        """
        Returns the bead under analysis

        :rtype: Bead
        """
        return self.__bead

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
    def sprout_count(self):
        """
        Returns a count of the primary sprouts. Primary sprouts are those
        sprouts which stem directly from the bead.

        :rtype: int
        """
        pass

    @property
    def critical_value(self):
        """
        Returns the critical value which is defined to be the radius at which
        the maximum number of crossings occur.

        :rtype: int
        """
        pass

    @property
    def total_branch_count(self):
        """
        Returns the maximum number of crossings of all radii.

        :rtype: int
        """
        pass

    @property
    def auxiliary_branch_count(self):
        """
        Returns the branching count which is defined to be the number of branches
        which stem from initial sprouts i.e. sprout maximum - sprout count

        :rtype: float
        """
        pass

    @property
    def branching_factor(self):
        """
        Returns the Shoenen Ramification Index which is a ratio for branching
        factor. This is calculated by dividing the sprout maximum with the
        number of primary sprouts.

        :rtype: float
        """
        pass

    @property
    def average_troc(self):
        pass


class NaiveAnalysisStrategy(AnalysisStrategy):
    @property
    def sprout_count(self):
        return self.crossings.values()[0]

    @property
    def critical_value(self):
        return max(self.crossings.items(), key=itemgetter(1))[0]

    @property
    def total_branch_count(self):
        return max(self.crossings.values())

    @property
    def auxiliary_branch_count(self):
        return self.total_branch_count - self.sprout_count

    @property
    def branching_factor(self):
        if self.sprout_count == 0:
            return 0
        return self.total_branch_count / self.sprout_count

    @property
    def average_troc(self):
        return self.critical_value / self.sprout_count if self.sprout_count > 0 else 0


class AveragedAnalysisStrategy(NaiveAnalysisStrategy):
    def bind(self, img, crossings, bead):
        super(NaiveAnalysisStrategy, self).bind(img, crossings, bead)

    @property
    def sprout_count(self):
        ordered_items = OrderedDict(sorted(self.crossings.items(), key=itemgetter(0))[0:self.critical_value])
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


class AveragedAnalysisStrategy(NaiveAnalysisStrategy):
    @property
    def sprout_count(self):
        l = lis(self.crossings.values())
        return sum(l) / len(l)


class MedianAnalysisStrategy(NaiveAnalysisStrategy):
    @property
    def sprout_count(self):
        l = lis(self.crossings.values())
        return np.median(l)


class PWAnalysisStrategy(NaiveAnalysisStrategy):
    def __init__(self):
        self.__piecewise_constants = None
        self.__piecewise_subs = None

    """
    Descriptor for a Sholl Analysis containing the raw data dump of the
    analysis as well as other derivable calculations.
    """
    def bind(self, img, crossings):
        super(NaiveAnalysisStrategy, self).bind(img, crossings)

    @property
    def sprout_count(self):
        # subs = utils.lis(self.crossings.values())
        # subs = self.crossings.values()
        # print self.crossings
        u, subs = full_piecewise_constants(self.crossings.values())
        self.__piecewise_constants = u
        self.__piecewise_subs = subs
        # for i in range(len(subs)):
        # 	if subs[i] != 0:
        # 		self.__sproutCount = subs[i+1]
        # 		break
        return self.__sproutCount

    @property
    def critical_value(self):
        return max(zip(self.crossings.keys(), self.__piecewise_subs), key=operator.itemgetter(1))[0]

    @property
    def sprout_maximum(self):
        return max(self.__piecewise_subs)

