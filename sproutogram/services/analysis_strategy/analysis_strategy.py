from ...repositories import models


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
        return models.Analysis(sprout_count=self.sprout_count,
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
