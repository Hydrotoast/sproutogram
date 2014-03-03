from .base import Base
from sqlalchemy import Column, Integer, String


def seed_train_data():
    data = [
        ('Ang1 250 ng_ml 1 Day 7', 14, 8, 1, 11),
        ('1k 3 Day 7', 23, 14, 2, 14),
        ('1k 2 Day 7', 15, 11, 3, 14),
        ('10k 5 Day 7', 20, 10, 4, 16),
        ('10k 1 Day 7', 16, 7, 4, 13),
        ('Control 5 Day 7', 17, 7, 0, 26),
        ('Control 4 Day 7', 17, 8, 2, 10),
        ('Control 2 Day 7', 18, 12, 3, 11),
        ('Control 1 Day 7', 17, 10, 7, 10),
        ('20k 5 Day 7', 24, 9, 2, 9),
        ('20k 3 Day 7', 12, 6, 4, 9),
        ('20k 2 Day 7', 23, 15, 11, 17),
        ('20k 1 Day 7', 17, 10, 3, 15),
        ('Ang1 100ng_ml 5 Day 7', 13, 9, 0, 10),
        ('Ang1 100ng_ml 3 Day 7', 12, 7, 3, 7)]

    train_data = []
    for datum in data:
        train_data.append(TrainData(filename=datum[0],
                                    max_sprout_count=datum[1],
                                    focus_sprout_count=datum[2],
                                    auxiliary_branch_count=datum[3],
                                    total_branch_count=datum[4]))

    from . import session
    session.add_all(train_data)
    session.commit()


class TrainData(Base):
    __tablename__ = 'training'

    filename = Column(String(), primary_key=True)
    max_sprout_count = Column(Integer())
    focus_sprout_count = Column(Integer())
    auxiliary_branch_count = Column(Integer())
    total_branch_count = Column(Integer())

    def __repr__(self):
        return "<TrainData(" \
               "filename='%s', " \
               "max_sprout_count='%s', " \
               "focus_sprout_count='%s', " \
               "auxilary_branch_count='%s', " \
               "total_branch_count='%s')>" \
               % (self.filename,
                  self.max_sprout_count,
                  self.focus_sprout_count,
                  self.auxiliary_branch_count,
                  self.total_branch_count)