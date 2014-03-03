from ..services.sholl_analysis import ShollAnalyzer
from ..services.analysis_strategy.naive_strategy import NaiveAnalysisStrategy
from .extractor import BeadExtractor

from ..repositories import Experiment
from ..repositories import session

from .exception import ExperimentAlreadyCompleteException


class NaiveAnalysisExperiment(object):
    def __init__(self, **kwargs):
        self.__img = kwargs['img']

        instance = session.query(Experiment).filter_by(name=self.__class__.__name__, params=str(kwargs)).first()
        if instance:
            raise ExperimentAlreadyCompleteException()
        else:
            self.__experiment = Experiment(name=self.__class__.__name__, params=str(kwargs))
            session.add(self.__experiment)

    def execute(self):
        bead_extractor = BeadExtractor(self.__img)
        beads = bead_extractor.extract()

        analyzer = ShollAnalyzer(NaiveAnalysisStrategy())
        analysis = analyzer.analyze(self.__img, beads[0])

        analysis.experiment = self.__experiment
        session.add(analysis)
        session.commit()
