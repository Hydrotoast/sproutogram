from strategy import *

from collections import deque


class ShollAnalyzer(object):
    """
    An analayzer for quantitatively analyzing the morphological characteristics
    of an angiogram. This analyzer depends on the known position of the bead in
    the angiogram to perform the analysis using concentric circles.
    """
    def __init__(self, strategy=IntegrationStrategy.AveragedAnalysisStrategy(), bead_factor=1.5, step_size=1):
        self.strategy = strategy
        self.bead_factor = bead_factor
        self.step_size = step_size

    def generate_circular_coordinates(self, origin, radius):
        """
        Generator for circular coordinates starting from the x+ vector and
        iterates counterclockwise.

            >>> for x, y in analyzer.generateCircularCoordinates((0, 0), 5):
            >>>     print x, y

        :returns: A list of circular coordinates given a specified origin and radius
        """
        x = radius
        y = 0
        radius_error = 1 - x

        octants = []
        for i in range(8):
            octants.append(deque())

        while x >= y:
            # x+ Q0
            octants[0].append((x + origin[0], -y + origin[1]))
            # y- Q1
            octants[1].appendleft((y + origin[0], -x + origin[1]))
            # y- Q2
            octants[2].append((-y + origin[0], -x + origin[1]))
            # x- Q3
            octants[3].appendleft((-x + origin[0], -y + origin[1]))
            # x- Q4
            octants[4].append((-x + origin[0], y + origin[1]))
            # y+ Q5
            octants[5].appendleft((-y + origin[0], x + origin[1]))
            # y+ Q6
            octants[6].append((y + origin[0], x + origin[1]))
            # x+ Q7
            octants[7].appendleft((x + origin[0], y + origin[1]))

            y += 1
            if radius_error < 0:
                radius_error += y << 2 + 1
            else:
                x -= 1
                radius_error += (y - x + 1) << 2

        for octant in octants:
            for point in octant:
                yield point

    def analyze(self, img, bead):
        """Returns a descriptor of the analysis.

        :rtype: ``ShollAnalysisDescriptor``"""
        init_radius = int(bead.radius() * self.bead_factor)
        max_radius = min([bead.x, bead.y, img.size()[0] - bead.x, img.size()[1] - bead.y])

        last_pixel = Color.BLACK[0]
        crossings = {}
        for r in range(init_radius, max_radius, self.step_size):
            crossings.update({r: 0})
            for x, y in self.generate_circular_coordinates(bead.origin(), r):
                pixel = img.getGrayPixel(x, y)
                if pixel != last_pixel and last_pixel == Color.WHITE[0]:
                    crossings[r] += 1
                last_pixel = pixel

        return ShollAnalysisDescriptor(img, crossings, self.strategy)
