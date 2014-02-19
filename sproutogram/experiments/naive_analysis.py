from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..services.sholl_analysis import ShollAnalyzer
from ..sproutogram.services.strategy import NaiveAnalysisStrategy
from .extractor import BeadExtractor
from ..repositories.models import Experiment


# ORM
engine = create_engine('sqlite:///db/development.db')
Session = sessionmaker(bind=engine)
session = Session()


class NaiveAnalysisExperiment(object):
    def __init__(self, **kwargs):
        self.__img = kwargs['img']

        self.__experiment = Experiment(name=self.__class__.__name__, params=str(kwargs))
        session.add(self.__experiment)

    def execute(self):
        bead_extractor = BeadExtractor(self.__img)
        beads = bead_extractor.extract()

        analyzer = ShollAnalyzer(NaiveAnalysisStrategy())
        analysis = analyzer.analyze(self.__img, beads[0])

        analysis.filename = self.__img.filename
        analysis.experiment = self.__experiment
        session.add(analysis)
        session.commit()
