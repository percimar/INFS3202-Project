from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from db import db, table_name_prefix, table_name_prefix_with_schema
from models import Follower


class User(db.Model):
    __tablename__ = table_name_prefix + "users"
    __table_args__ = {"schema": "public"}  # needed for db.drop_all() to work https://stackoverflow.com/a/56499548

    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False, unique=True)
    last_login = Column(DateTime(), nullable=True)

    posts = relationship("Post", back_populates="author")
    liked_posts = relationship("Post", secondary=table_name_prefix_with_schema + "likes", back_populates="likes")

    # followers = relationship("User", secondary=table_name_prefix_with_schema + "followers",
    #                          back_populates="followed_by", foreign_keys="following_id")
    # followed_by = relationship("User", secondary=table_name_prefix_with_schema + "followers",
    #                            back_populates="followers", foreign_keys="user_id")
    followers = relationship(
        "User",
        secondary=table_name_prefix_with_schema + "followers",
        primaryjoin=id == Follower.user_id,
        secondaryjoin=id == Follower.following_id,
        backref="followed_by",
    )

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_or_create_user(cls, username):
        return cls.get_by_username(username)
