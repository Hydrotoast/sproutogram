class AnalysisStrategy(object):
    def __init__(self):
        self.integration_method = 'median'

        self.__img = None
        self.__crossings = None

    def bind(self, img, crossings):
        self.__img = img
        self.__crossings = crossings

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
    def sprout_maximum(self):
        """
        Returns the maximum number of crossings of all radii.

        :rtype: int
        """
        pass

    @property
    def ramification_index(self):
        """
        Returns the Shoenen Ramification Index which is a ratio for branching
        factor. This is calculated by dividing the sprout maximum with the
        number of primary sprouts.

        :rtype: float
        """
        pass

    @property
    def branching_count(self):
        """
        Returns the branching count which is defined to be the number of branches
        which stem from initial sprouts i.e. sprout maximum - sprout count

        :rtype: float
        """
        pass


class ShollAnalysisDescriptor(object):
    """
    Descriptor for a Sholl Analysis containing the raw data dump of the
    analysis as well as other derivable calculations.
    """
    def __init__(self, img, crossings, strategy):
        self.strategy = strategy
        self.strategy.bind(img, crossings)
        # self.integrationMethod = 'median'

        self.__img = img
        self.__crossings = crossings
        self.__sproutCount = self.strategy.sprout_count
        self.__criticalValue = self.strategy.critical_value
        self.__sproutMaximum = self.strategy.sprout_maximum
        self.__ramificationIndex = self.strategy.ramification_index
        self.__branchingCount = self.strategy.branching_count
        self.__trocAverage = self.strategy.troc_average

    @property
    def img(self):
        """Returns the image analyzed."""
        return self.__img

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
        return self.__sproutCount

    @property
    def critical_value(self):
        """
        Returns the critical value which is defined to be the radius at which
        the maximum number of crossings occur.

        :rtype: int
        """
        return self.__criticalValue

    @property
    def sprout_maximum(self):
        """
        Returns the maximum number of crossings of all radii.

        :rtype: int
        """
        return self.__sproutMaximum

    @property
    def ramification_index(self):
        """
        Returns the Shoenen Ramification Index which is a ratio for branching
        factor. This is calculated by dividing the sprout maximum with the
        number of primary sprouts.

        :rtype: float
        """
        return self.__ramificationIndex

    @property
    def branching_count(self):
        """
        Returns the branching count which is defined to be the number of branches
        which stem from initial sprouts i.e. sprout maximum - sprout count

        :rtype: float
        """
        return self.__branchingCount

    @property
    def troc_average(self):
        """
        Returns the average of the terminal radius of crossings.

        :rtype: float
        """
        return self.__trocAverage
