from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Post(Base):

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(1048576), nullable=False) 
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    author = relationship("User", back_populates="posts")

    def __repr__(self):
        return f"<Post(id={self.id}, author_id={self.author_id})>"