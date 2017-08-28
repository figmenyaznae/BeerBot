from sqlalchemy import Column, Integer, String, Boolean, Date
from .base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Status(Base):
    __tablename__ = 'status'

    chat_id = Column(Integer, primary_key=True)
    is_polling = Column(Boolean, nullable=False)
    meeting_id = Column(Integer, ForeignKey('meetings.id'))
    meeting = relationship("Meeting")

    def __repr__(self):
        return "<Status(id={}, polling={}, date={})>".format(
            self.chat_id, self.is_polling, self.meeting.date)
