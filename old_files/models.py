from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String
from sqlalchemy.types import DateTime

Base = declarative_base()

class to_follow(Base):
    __tablename__ = 'to_follow'
    id = Column('id',String, primary_key = True)
    username = Column('username',String, unique = True)

    def __repr__(self):
        return f"Username: {self.username}"

class followed(Base):
    __tablename__ = 'followed'
    id = Column('id',String,primary_key = True)
    username = Column('username',String,unique=True)
    date = Column(DateTime)

    def __repr__(self):
        return f"Following {self.username} at {self.date}"