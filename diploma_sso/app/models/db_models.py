from sqlalchemy import (
    Column,
    Integer,
    PrimaryKeyConstraint,
    String,
    Boolean
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "User"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    second_name = Column(String)
    phone_number = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    role = Column(String)


class ChildTutor(Base):
    __tablename__ = "ChildTutor"
    child_id = Column(Integer)
    tutor_id = Column(Integer)
    is_approoved = Column(Boolean)

    __table_args__ = (PrimaryKeyConstraint("child_id", "tutor_id"),)


class ChildParent(Base):
    __tablename__ = "ChildParent"
    child_id = Column(Integer)
    parent_id = Column(Integer)
    is_approoved = Column(Boolean)

    __table_args__ = (PrimaryKeyConstraint("child_id", "parent_id"),)
