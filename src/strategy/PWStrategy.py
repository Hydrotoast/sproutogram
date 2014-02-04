from NaiveStrategy import NaiveAnalysisStrategy
from PiecewiseConstantApproximation import full_piecewise_constants


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
