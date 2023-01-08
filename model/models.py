from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()

class Mark(Base):
    __tablename__ = 'marks'
    id = Column(Integer, primary_key=True)
    date = Column(String(100))
    pupil_name = Column(String(100), nullable=False)
    subject = Column(String(255), nullable=False)
    mark = Column(Integer, nullable=False)

class Homework(Base):
    __tablename__ = 'homeworks'
    id = Column(Integer, primary_key=True)
    date = Column(String(100))
    subject = Column(String(255), nullable=False)
    homework_text = Column(String(255), nullable=False)