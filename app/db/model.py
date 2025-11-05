from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base

class UserStep(Base):
    __tablename__ = "user_step"
    uuid = Column(String, primary_key=True, index=True)
    step = Column(Integer, default=1)

