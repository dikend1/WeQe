from sqlalchemy import Integer,String,Boolean,ForeignKey,Text,Column
from sqlalchemy.orm import relationship
from app.db.base import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=False)
    content = Column(Text,nullable=False)
    owner_id = Column(Integer,ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment",back_populates="post")
