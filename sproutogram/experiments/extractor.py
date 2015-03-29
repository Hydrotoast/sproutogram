import os

from SimpleCV import ImageSet, Color
import matplotlib.pyplot as plt

from .. import BeadExtractor, SproutExtractor
from .. import ShollAnalyzer
from ..report_generation import CSVReportGenerator
from ..services.extraction import NoBeadException, NoSproutsException
from sproutogram.services.analysis_strategy import integration_strategy
from ..repositories import Experiment, Analysis
from ..repositories import session


class ExtractionExperiment(object):
    """
    An Extraction task defines an atomic job for extracting and quantitatively
    analyzing an image set of fibrin gel bead sprouting assays.
    """
    def __init__(self, **kwargs):
        self.params = kwargs
        instance = session.query(Experiment).filter_by(
            name=self.__class__.__name__, params=str(self.params)).first()
        if instance:
            self.__experiment = instance
            for analysis in instance.analyses:
                session.delete(analysis)
            session.commit()
        else:
            self.__experiment = Experiment(name=self.__class__.__name__,
                                           params=str(self.params))
            session.add(self.__experiment)
            session.commit()

        self.data_path = kwargs['data_path']
        self.method_name = self.__class__.__name__ + str(self.analyzer.bead_factor)
        self.result_path = os.path.join(kwargs['result_path'], self.method_name)
        self.plot_path = os.path.join(self.result_path, 'plots')

        self.canny_min = kwargs.get('canny_min', 40)
        self.canny_max = kwargs.get('canny_max', 120)

        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)
        if not os.path.exists(self.plot_path):
            os.makedirs(self.plot_path)

    def analyze_mono_bead(self, img):
        bead_extractor = BeadExtractor(img)
        beads = bead_extractor.extract()

        try:
            sprout_extractor = SproutExtractor(img, beads,
                                               canny_min=self.canny_min,
                                               canny_max=self.canny_max)
            sprouts = sprout_extractor.extract()
            for sprout in sprouts:
                sprout.restore(width=3, distance_threshold=24, color=Color.WHITE)
            sprouts_img = sprouts[-1].image.applyLayers()
            sprouts_img.resize(w=800).show()
            sprouts_img.filename = img.filename

            analysis = self.analyzer.analyze(sprouts_img, beads[0])
        except NoSproutsException:
            return Analysis(filename=img.filename,
                            sprout_count=0,
                            critical_value=0,
                            total_branch_count=0,
                            auxiliary_branch_count=0,
                            branching_factor=0,
                            average_troc=0)

        return analysis

    def extract(self):
        image_set = ImageSet(self.data_path)
        image_set.sort()
        output_path = os.path.join(self.result_path,
                                   self.__experiment.name + '.csv')
        report_gen = CSVReportGenerator(output_path, params=self.params)
        counter = 1
        print 'Extracting using %s' % self.method_name
        for image in sorted(image_set, key=lambda img: img.filename):
            filename = os.path.splitext(os.path.basename(image.filename))[0]

            instance = session.query(Analysis).filter_by(filename=image.filename,
                                                         experiment_name=self.__experiment.name,
                                                         experiment_params=self.__experiment.params).first()
            if instance:
                analysis = instance
            else:
                try:
                    analysis = self.analyze_mono_bead(image)
                    analysis.experiment = self.__experiment
                    session.add(analysis)
                    print 'Analyzing %d/%d: %s' % (counter, len(image_set.filelist), filename)
                except NoBeadException:
                    print 'No Bead Exception: %s' % filename

            # Sholl Analysis Plots
            #self.plot_sholl_analysis(analysis, filename)

            # Add to overall report
            report_gen.add_analysis(filename, analysis)

            counter += 1
        session.commit()
        report_gen.generate()

    def plot_sholl_analysis(self, analysis, filename):
        if not analysis.crossings():
            return
        plt.figure(1, figsize=(18, 6))
        plt.plot(analysis.crossings.keys(), analysis.crossings.values())
        plt.title('Sholl Analysis for ' + filename)
        plt.xlabel('Radius')
        plt.ylabel('Crossings')
        plt.savefig(os.path.join(self.plot_path, filename + ".png"))
        plt.clf()


class AveragedExtraction(ExtractionExperiment):
    def __init__(self, data_path, result_path, **kwargs):
        self.analyzer = ShollAnalyzer(
            bead_factor=kwargs.get('bead_factor', 1.5),
            step_size=kwargs.get('step_size', 1))
        super(AveragedExtraction, self).__init__(
            data_path=data_path, result_path=result_path, **kwargs)


class AveragedSproutPostRisingEdgeExperiment(ExtractionExperiment):
    def __init__(self, data_path, result_path, **kwargs):
        self.analyzer = ShollAnalyzer(
            bead_factor=kwargs.get('bead_factor', 1.5),
            step_size=kwargs.get('step_size', 1))
        self.analyzer.strategy = \
            integration_strategy.AveragedSproutPostRisingEdge()
        super(AveragedSproutPostRisingEdgeExperiment, self).__init__(
            data_path=data_path, result_path=result_path, **kwargs)


class MPlusDelta2(ExtractionExperiment):
    def __init__(self, data_path, result_path, **kwargs):
        self.analyzer = ShollAnalyzer(
            bead_factor=kwargs.get('bead_factor', 1.5),
            step_size=kwargs.get('step_size', 1))
        self.analyzer.strategy = integration_strategy.MPlusDelta2()
        super(MPlusDelta2, self).__init__(
            data_path=data_path, result_path=result_path, **kwargs)
