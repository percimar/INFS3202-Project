from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db import db, table_name_prefix, table_name_prefix_with_schema


class Post(db.Model):
    __tablename__ = table_name_prefix + "posts"
    __table_args__ = {"schema": "public"}  # needed for db.drop_all() to work https://stackoverflow.com/a/56499548

    id = Column(Integer, primary_key=True)
    content = Column(Text())
    date_created = Column(DateTime(), nullable=False, server_default=db.func.now())
    author_id = Column(ForeignKey(table_name_prefix_with_schema + 'users.id'), nullable=False)

    author = relationship("User", back_populates="posts")
    likes = relationship("User", secondary=table_name_prefix_with_schema + "likes", back_populates="liked_posts")
