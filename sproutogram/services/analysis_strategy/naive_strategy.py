from operator import itemgetter

from sproutogram.services.analysis_strategy.analysis_strategy import AnalysisStrategy


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
