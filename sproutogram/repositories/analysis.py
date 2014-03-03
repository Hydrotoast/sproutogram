from .base import Base
from sqlalchemy import ForeignKeyConstraint, Column, String, Float


class Analysis(Base):
    __tablename__ = 'analyses'
    __table_args__ = (
        ForeignKeyConstraint(
            ['experiment_name', 'experiment_params'],
            ['experiments.name', 'experiments.params']),
    )

    filename = Column(String(), primary_key=True)

    # Belongs to an experiment.
    experiment_name = Column(String(255), primary_key=True)
    experiment_params = Column(String(255), primary_key=True)

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
