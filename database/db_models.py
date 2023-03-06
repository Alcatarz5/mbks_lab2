from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship

base = DeclarativeBase


class AccessMark(base):
    __tablename__ = "access_marks"

    id = Column(Integer, primary_key=True, nullable=False)

    description = Column(Text, nullable=False)

    users = relationship("User", back_populates="access_marks")


class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)

    access_mark = Column(Integer, ForeignKey("access_marks.id"), nullable=False)

    name = Column(Text, nullable=False)

    access_marks = relationship("AccessMark", back_populates="users")
    objects = relationship("Object", back_populates="users")


class Object(base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    secure_mark = Column(Integer, nullable=False)
    file_uri = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)

    users = relationship("User", back_populates="objects")
