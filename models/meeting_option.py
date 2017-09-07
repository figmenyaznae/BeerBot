from sqlalchemy import Column, Integer, String, Date
from .base import Base


class MeetingOption(Base):
    __tablename__ = 'meeting_options'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    chat_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    message_id = Column(Integer, nullable=False)
    date = Column(Date)

    def __repr__(self):
        return u"<Option(id={}, name={} user={}, message={}, date={})>".format(
            self.id, self.name, self.user_id, self.message_id, self.date)