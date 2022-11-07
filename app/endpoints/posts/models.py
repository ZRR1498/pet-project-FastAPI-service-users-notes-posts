import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from app.db.database import Base


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String(2000))
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=None)
    likes = Column(Integer, default=0)


class Likes(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, unique=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
