import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, BOOLEAN
from app.db.database import Base


class Notes(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(50))
    description = Column(String(1000))
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=None)
    status_delete = Column(BOOLEAN, default=False)
