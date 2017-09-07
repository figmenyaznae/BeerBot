from sqlalchemy import Column, Integer, Date
from .base import Base


class Meeting(Base):
    __tablename__ = 'meetings'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)

    def __repr__(self):
        return "<Meeting(id={}, date={})>".format(
            self.id, self.date)