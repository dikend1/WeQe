from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True,nullable=False)
    email = Column(String,unique=True,nullable=False)
    password = Column(String,unique=True,nullable=False)
    is_admin = Column(Boolean,default=False)


    posts =relationship("Post",back_populates="owner")
    comments = relationship("Comment",back_populates="author")
    