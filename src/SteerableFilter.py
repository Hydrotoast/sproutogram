from itertools import *

from SimpleCV import *


class SteerableFilter(object):
    def __init__(self, image):
        self.convolved_images = []

        self.filter_a = [[0, 0, 0, 0, 0],
            [1, 1, 3, 1, 1],
            [2, 2, 4, 2, 2],
            [1, 1, 3, 1, 1],
            [0, 0, 0, 0, 0]]
        # normA = float(sum(list(chain.from_iterable(self.filterA))))
        # accMatrix = []
        # for subl in self.filterA:
        #   accMatrix.append([elem / normA for elem in subl])
        # self.filterA = accMatrix
        self.filter_b = [[0, 1, 2, 1, 0],
            [0, 1, 2, 1, 0],
            [0, 3, 4, 3, 0],
            [0, 1, 2, 1, 0],
            [0, 1, 2, 1, 0]]
        # normB = float(sum(list(chain.from_iterable(self.filterB))))
        # accMatrix = []
        # for subl in self.filterB:
        #   accMatrix.append([elem / normA for elem in subl])
        # self.filterB = accMatrix
        self.filters = [self.filter_a, self.filter_b]
        self.image = image

    def convolve(self, origin):
        # Basis images
        self.convolved_images = [self.image.convolve(kernel) for kernel in self.filters]
        
        # Applies a filter in the direction away from the origin of the blood vessel
        accumulated_image = Image(self.image.size())
        for pixel in product(range(1, self.image.size()[0]), range(1, self.image.size()[1])):
            accumulated_image[pixel[0], pixel[1]] = tuple([self.accumulate(pixel, origin)] * 3)
        self.image = accumulated_image

        # Steerable filter applied to image
        return self.image

    def accumulate(self, pixel, origin):
        dot_product = sum(a * b for a, b in zip(pixel, origin))
        denom = sqrt(sum(map(lambda x: x ** 2, pixel))) * sqrt(sum(map(lambda x: x ** 2, origin)))
        if dot_product / denom > 1:
            dot_product = denom
        theta = acos(dot_product / denom)
        if theta > 0.5 or theta < -0.5:
            print(theta)
        
        first_component = cos(theta) * self.convolved_images[0].getGrayPixel(pixel[0], pixel[1])
        second_component = sin(theta) * self.convolved_images[1].getGrayPixel(pixel[0], pixel[1])
        return first_component + second_component
