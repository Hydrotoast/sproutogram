import os

from SimpleCV import ImageSet, Color, spsd

from .. import BeadExtractor, SproutExtractor, HLSGExtractor
from .. import ShollAnalyzer
from ..report_generation import CSVReportGenerator
from sproutogram.services.analysis_strategy import integration_strategy

from ..repositories import Experiment
from ..repositories import session


class ExtractionTask(object):
    """
    An Extraction task defines an atomic job for extracting and quantitatively
    analyzing an image set of fibrin gel bead sprouting assays.
    """
    def __init__(self, **kwargs):
        instance = session.query(Experiment).filter_by(name=self.__class__.__name__, params=str(kwargs)).first()
        if instance:
            self.__experiment = instance
        else:
            self.__experiment = Experiment(name=self.__class__.__name__, params=str(kwargs))
            session.add(self.__experiment)
            session.commit()

        self.in_path = kwargs['in_path']
        self.out_path = kwargs['out_path']
        self.method_name = self.__class__.__name__ + str(self.analyzer.bead_factor)
        self.report_path = os.path.join(kwargs['report_path'], self.method_name)
        self.plot_path = os.path.join(self.report_path, 'plots')

        if not os.path.exists(self.report_path):
            os.makedirs(self.report_path)
        if not os.path.exists(self.plot_path):
            os.makedirs(self.plot_path)

    def analyze_mono_bead(self, img):
        bead_extractor = BeadExtractor(img)
        beads = bead_extractor.extract()

        sprout_extractor = SproutExtractor(img, beads)
        sprouts = sprout_extractor.extract()
        for sprout in sprouts:
            sprout.restore(width=3, distance_threshold=24, color=Color.WHITE)
        sprouts_img = sprouts[-1].image.applyLayers()
        sprouts_img.resize(w=800).show()
        sprouts_img.filename = img.filename

        analysis = self.analyzer.analyze(sprouts_img, beads[0])

        hlsg_extractor = HLSGExtractor(img)
        hlsgs = hlsg_extractor.extract()
        average_sprout_length = sum(map(lambda sprout: spsd.euclidean(sprout.origin, sprout.head), hlsgs[0].sprouts))
        average_sprout_length /= analysis.sprout_count
        print '\tAverage Sprout Length: %.2f' % average_sprout_length

        return analysis

    def extract(self):
        image_set = ImageSet(self.in_path)
        image_set.sort()
        report_gen = CSVReportGenerator(os.path.join(self.report_path, self.__experiment.name + '.csv'))
        #report_gen = DBReportGenerator(os.path.join('repositories', 'extractions.repositories'), self.method_name)
        counter = 1
        print 'Extracting using %s' % self.method_name
        for image in sorted(image_set, key=lambda img: img.filename):
            filename = os.path.splitext(os.path.basename(image.filename))[0]

            analysis = self.analyze_mono_bead(image)
            analysis.experiment = self.__experiment
            session.add(analysis)

            print 'Analyzing %d/%d: %s' % (counter, len(image_set.filelist), filename)

            # Sholl Analysis Plots
            # self.plot_sholl_analysis(analysis, filename)

            # Add to overall report
            report_gen.add_analysis(filename, analysis)

            counter += 1
        session.commit()
        #report_gen.generate()
    #
    # def plot_sholl_analysis(self, analysis, filename):
    #     plt.figure(1, figsize=(18, 6))
    #     plt.plot(analysis.crossings.keys(), analysis.crossings.values())
    #     plt.title('Sholl Analysis for ' + filename)
    #     plt.xlabel('Radius')
    #     plt.ylabel('Crossings')
    #     plt.savefig(os.path.join(self.plot_path, filename + ".png"))
    #     plt.clf()


class AveragedExtractionTask(ExtractionTask):
    def __init__(self, in_path, out_path, report_path, bead_factor=1.5, step_size=1):
        self.analyzer = ShollAnalyzer(integration_strategy.AveragedAnalysisStrategy(), bead_factor, step_size)
        super(AveragedExtractionTask, self).__init__(in_path=in_path, out_path=out_path, report_path=report_path)


# class ThresholdAverageExtractionTask(ExtractionTask):
#     def __init__(self, in_path, out_path, report_path, bead_factor=1.5, step_size=1):
#         self.analyzer = ShollAnalyzer(integration_strategy.ThresholdAverageStrategy(), bead_factor)
#         super(ThresholdAverageExtractionTask, self).__init__(in_path, out_path, report_path)
#
#
# class MedianIntegrationExtractionTask(ExtractionTask):
#     def __init__(self, in_path, out_path, report_path, bead_factor=1.5, step_size=1):
#         self.analyzer = ShollAnalyzer(integration_strategy.MedianAnalysisStrategy(), bead_factor, step_size)
#         super(MedianIntegrationExtractionTask, self).__init__(in_path, out_path, report_path)
#
#
# class ThresholdMedianIntegrationExtractionTask(ExtractionTask):
#     def __init__(self, in_path, out_path, report_path, bead_factor=1.5, step_size=1):
#         self.analyzer = ShollAnalyzer(integration_strategy.MedianAnalysisStrategy(), bead_factor, step_size)
#         super(ThresholdMedianIntegrationExtractionTask, self).__init__(in_path, out_path, report_path)
#

