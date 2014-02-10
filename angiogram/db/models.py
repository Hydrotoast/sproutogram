from sqlalchemy import ForeignKey, Column, Integer, Float, String, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Experiment(Base):
    __tablename__ = 'experiments'

    name = Column(String(255), primary_key=True)
    params = Column(Text(), primary_key=True)

    def __repr__(self):
        return "<Experiment(name='%s', params='%s')>" % (self.name, self.params)


class Analysis(Base):
    __tablename__ = 'analyses'

    filename = Column(String(), primary_key=True)

    # Belongs to an experiment.
    experiment_name = Column(String(), ForeignKey('experiments.name'))
    experiment_params = Column(Text(), ForeignKey('experiments.params'))
    experiment = relationship('Experiment', backref=backref('analyses', order_by=filename))

    sprout_count = Column(Float())
    critical_value = Column(Float())
    total_branch_count = Column(Float())
    aux_branch_count = Column(Float())
    branching_factor = Column(Float())
    average_troc_length = Column(Float())

    def __repr__(self):
        return "<Analysis(" \
               "sprout_count='%s', " \
               "total_branch_count='%s', " \
               "auxiliary_branch_count='%s', " \
               "branching_factor='%s', " \
               "average_sprout_length='%s'" \
               % (self.sprout_count,
                  self.total_branch_count,
                  self.aux_branch_count,
                  self.branching_factor,
                  self.average_sprout_length)


class TrainData(Base):
    __tablename__ = 'training'

    filename = Column(String(), primary_key=True)
    max_sprout_count = Column(Integer())
    focus_sprout_count = Column(Integer())
    aux_branch_count = Column(Integer())
    total_branch_count = Column(Integer())

    def __repr__(self):
        return "<TrainData(" \
               "filename='%s', " \
               "max_sprout_count='%s', " \
               "focus_sprout_count='%s', " \
               "aux_branch_count='%s', " \
               "total_branch_count='%s')>" \
               % (self.filename,
                  self.max_sprout_count,
                  self.focus_sprout_count,
                  self.aux_branch_count,
                  self.total_branch_count)
