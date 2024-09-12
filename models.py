from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True)
    username = Column(String)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String)
    is_active = Column(String)


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    owner = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
