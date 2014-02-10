from analysis_descriptor import AnalysisStrategy
from operator import itemgetter


class NaiveAnalysisStrategy(AnalysisStrategy):
    def bind(self, img, crossings, bead):
        super(AnalysisStrategy, self).__init__(img, crossings, bead)

    @property
    def sprout_count(self):
        return self.crossings.values()[0]

    @property
    def critical_value(self):
        return max(self.crossings.items(), key=itemgetter(1))[0]

    @property
    def sprout_maximum(self):
        return max(self.crossings.values())

    @property
    def ramification_index(self):
        if self.sprout_count == 0:
            return 0
        return self.sprout_maximum / self.sprout_count

    @property
    def branching_count(self):
        return self.sprout_maximum - self.sprout_count

    @property
    def troc_average(self):
        return self.critical_value / self.sprout_count
