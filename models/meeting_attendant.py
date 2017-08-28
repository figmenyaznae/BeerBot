from sqlalchemy import Column, Integer, String, Boolean, Date
from .base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class MeetingAttendant(Base):
    __tablename__ = 'meeting_attendants'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    meeting_id = Column(Integer, ForeignKey('meetings.id'))
    meeting = relationship("Meeting", backref="attendants")
    status = Column(Integer, nullable=False)

    def __repr__(self):
        return u"<Attendance(id={}, meeting={}, status={})>".format(
            self.id, self.meeting_id, self.status.encode('ascii', 'ignore'))