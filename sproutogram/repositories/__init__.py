from .experiment import Experiment
from .analysis import Analysis
from .train_data import TrainData

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_ENGINE = 'sqlite'
DB_FILE = 'db/development.db'

engine = create_engine('%s:///%s' % (DB_ENGINE, DB_FILE))
Session = sessionmaker(bind=engine)
session = Session()
