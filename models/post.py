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

    @classmethod
    def get_by_id(cls, post_id: int):
        return cls.query.filter_by(id=post_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_partial_content(cls, content: str):
        return cls.query.filter(Post.content.ilike(f"%{content}%")).limit(10).all()

    @classmethod
    def get_by_user(cls, user_id: int):
        """Get created posts by user i in order of most recent"""
        return cls.query.filter_by(author_id=user_id).order_by(Post.date_created).limit(10).all()
    
    @classmethod
    def get_by_users(cls, users: [int]):
        """Get created posts by users in list in order of most recent"""
        return cls.query.filter(Post.author_id.in_(users)).order_by(Post.date_created).limit(10).all()

    @property
    def json(self):
        return {
            "id": self.id,
            "content": self.content,
            "date_created": str(self.date_created),
            "author_id": self.author_id,
            "author_username": self.author.username,
            "likes": [like.user_id for like in self.likes]
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True
