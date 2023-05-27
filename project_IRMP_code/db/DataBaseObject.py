from sqlalchemy import Column, Integer
from sqlalchemy.orm import DeclarativeBase


class DataBaseObject(DeclarativeBase):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pass
