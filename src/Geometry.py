from SimpleCV import Line

from math import *

class RadialSegment(Line):
    def __init__(self, img, start, end, blob=None):
        self.start = start
        self.end = end

        self.blob = blob
        super(RadialSegment, self).__init__(img, (start, end))