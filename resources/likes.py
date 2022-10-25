from http import HTTPStatus

from flask import session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from models import User, Like, Post


class LikeResource(Resource):
    @staticmethod
    def post(post_id: int):
        if "user" not in session:
            return {"message": "Please login first."}, HTTPStatus.UNAUTHORIZED

        user_id = session["user"]

        try:
            Like(user_id=user_id, post_id=post_id).save()
        except IntegrityError:
            # even though this is an error, the goal (have logged-in user like post_id) is accomplished,
            # so we return OK instead of an error status.
            return {"message": "Current user already liked this post."}, HTTPStatus.OK

        return {"message": "Current user has liked this post."}, HTTPStatus.OK


class UnlikeResource(Resource):
    @staticmethod
    def post(post_id: int):
        if "user" not in session:
            return {"message": "Please login first."}, HTTPStatus.UNAUTHORIZED

        user_id = session["user"]

        like_record = Like.get_record(user_id, post_id)

        if like_record is None:
            # even though this is an error, the goal (have logged-in user not following user_id) is accomplished,
            # so we return OK instead of an error status.
            return {"message": "Current user did not have this post liked."}, HTTPStatus.OK

        like_record.delete()

        return {"message": "Current user no longer likes this post."}, HTTPStatus.OK


class UserLikesResource(Resource):
    @staticmethod
    def get(user_id: int):
        user = User.get_by_id(user_id)
        if user is None:
            return {"message": f"User with id {user_id} not found."}, HTTPStatus.NOT_FOUND

        likes = user.liked_posts

        return {
                   "posts": [post.json for post in likes]
               }, HTTPStatus.OK


class PostLikesResource(Resource):
    @staticmethod
    def get(post_id: int):
        post = Post.get_by_id(post_id)
        if post is None:
            return {"message": f"Post with id {post_id} not found."}, HTTPStatus.NOT_FOUND

        likes = post.likes

        return {
                   "users": [user.json for user in likes]
               }, HTTPStatus.OK
