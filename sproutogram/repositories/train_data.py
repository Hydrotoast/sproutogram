from .base import Base
from sqlalchemy import Column, Integer, String


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