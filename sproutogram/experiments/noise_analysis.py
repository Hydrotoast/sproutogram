import os

import numpy as np

from SimpleCV import ImageSet, Color, spsd
from SimpleCV import Image

from .. import BeadExtractor, SproutExtractor
from ..services.analysis_strategy.integration_strategy import AveragedAnalysisStrategy
from .. import ShollAnalyzer
from ..report_generation import CSVReportGenerator


class NoiseAnalysis(object):
    def __init__(self, **kwargs):
        self.analyzer = ShollAnalyzer(AveragedAnalysisStrategy(), 1.5, 1)
        self.in_path = kwargs['in_path']
        self.out_path = kwargs['out_path']
        self.method_name = self.__class__.__name__ + str(self.analyzer.bead_factor)
        self.report_path = os.path.join(kwargs['report_path'], self.method_name)
        self.plot_path = os.path.join(self.report_path, 'plots')

        if not os.path.exists(self.report_path):
            os.makedirs(self.report_path)
        if not os.path.exists(self.plot_path):
            os.makedirs(self.plot_path)

    def analyze_single(self, img):
        canny_min, canny_max = (100, 240)
        dilateCount = 8
        img_edges = img.copy().edges(canny_min, canny_max)

        img_edges = img_edges.morphClose().dilate(dilateCount)
        blobs = img_edges.findBlobs()
        for blob in blobs:
            if len(blob.mContourAppx) > 2:
                blob.drawAppx(color=Color.WHITE, width=-1)
            blob.drawHoles(color=Color.WHITE, width=-1)
        img_edges = img_edges.applyLayers()

        img_edges.resize(w=800).show()
        img_edges.filename = img.filename

        sobel_img = img.binarize(120) - img_edges
        sobel_img.resize(w=800).show()
        sobel_img.sobel().resize(w=800).show()

        return np.sum(sobel_img.getGrayNumpy())

    def analyze(self):
        image_set = ImageSet(self.in_path)
        image_set.sort()
        report_gen = CSVReportGenerator(os.path.join(self.report_path, 'noise_analysis.csv'))
        counter = 1
        print 'Extracting using %s' % self.method_name
        for image in sorted(image_set, key=lambda img: img.filename):
            filename = os.path.splitext(os.path.basename(image.filename))[0]

            noise = self.analyze_single(image)

            #print 'Analyzing %d/%d: %s' % (counter, len(image_set.filelist), filename)
            print '%.2f' % noise

            counter += 1
        report_gen.generate()

