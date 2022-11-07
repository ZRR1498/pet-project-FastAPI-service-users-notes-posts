import datetime
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base


class AuthToken(Base):
    __tablename__ = "auth_token"

    id = Column(Integer, primary_key=True)
    token = Column(String)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow())


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True)
    email = Column(String(50), unique=True)
    hash_password = Column(String(300))
    first_name = Column(String(20))
    last_name = Column(String(20))
    nickname = Column(String(20), unique=True)
    is_active = Column(Boolean, default=True)
    avatar = Column(String, default=None)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    child = relationship(AuthToken, backref="parent", passive_deletes=True)


class UserFriends(Base):
    __tablename__ = "user_friends"

    id = Column(Integer, primary_key=True, unique=True)
    first_user_id = Column(Integer, ForeignKey('users.id'))
    second_user_id = Column(Integer, ForeignKey('users.id'))
    status_accepted = Column(Boolean, default=False)
    date_time = Column(DateTime, default=datetime.datetime.utcnow())
