from sqlalchemy import ForeignKeyConstraint, Column, Integer, Float, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Experiment(Base):
    __tablename__ = 'experiments'

    name = Column(String(255), primary_key=True)
    params = Column(String(255), primary_key=True)

    analyses = relationship('Analysis', backref='experiment')

    def __repr__(self):
        return "<Experiment(name='%s', params='%s')>" % (self.name, self.params)


class Analysis(Base):
    __tablename__ = 'analyses'
    __table_args__ = (
        ForeignKeyConstraint(
            ['experiment_name', 'experiment_params'],
            ['experiments.name', 'experiments.params']),
    )

    filename = Column(String(), primary_key=True)

    # Belongs to an experiment.
    experiment_name = Column(String(255))
    experiment_params = Column(String(255))

    sprout_count = Column(Float())
    critical_value = Column(Float())
    total_branch_count = Column(Float())
    auxiliary_branch_count = Column(Float())
    branching_factor = Column(Float())
    average_troc = Column(Float())

    def __repr__(self):
        return "<Analysis(" \
               "sprout_count='%s', " \
               "total_branch_count='%s', " \
               "auxiliary_branch_count='%s', " \
               "branching_factor='%s', " \
               "average_troc='%s'" \
               % (self.sprout_count,
                  self.total_branch_count,
                  self.auxiliary_branch_count,
                  self.branching_factor,
                  self.average_troc)


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
