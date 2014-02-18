from SimpleCV import np

from naive_strategy import NaiveAnalysisStrategy
from ..utils import lis


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
