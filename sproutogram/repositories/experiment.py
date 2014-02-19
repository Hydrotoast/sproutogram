from .base import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Experiment(Base):
    __tablename__ = 'experiments'

    name = Column(String(255), primary_key=True)
    params = Column(String(255), primary_key=True)

    analyses = relationship('Analysis', backref='experiment')

    def __repr__(self):
        return "<Experiment(name='%s', params='%s')>" % (self.name, self.params)
