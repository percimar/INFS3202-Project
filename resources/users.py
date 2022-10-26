from http import HTTPStatus

from flask import request
from flask_restful import Resource

from models import User, Post


class UsersResource(Resource):
    @staticmethod
    def get(user_id: int):
        user = User.get_by_id(user_id)
        if user is None:
            return {"message": f"User with id {user_id} not found."}, HTTPStatus.NOT_FOUND
        return user.json, HTTPStatus.OK


class UsersListResource(Resource):
    @staticmethod
    def get():
        partial_name = request.args["name"] if "name" in request.args else ""
        matches = User.get_by_partial_username(partial_name)
        return {
                   "users": [user.json for user in matches]
               }, HTTPStatus.OK


class FeedResource(Resource):
    @staticmethod
    def get(user_id: int):
        user = User.get_by_id(user_id)
        if user is None:
            return {"message": f"User with id {user_id} not found."}, HTTPStatus.NOT_FOUND

        following = user.following

        posts = Post.get_by_users([user.id for user in following])
        return {
                   "posts": [post.json for post in posts]
               }, HTTPStatus.OK


class UserPostsResource(Resource):
    @staticmethod
    def get(user_id: int):
        user = User.get_by_id(user_id)
        if user is None:
            return {"message": f"User with id {user_id} not found."}, HTTPStatus.NOT_FOUND

        posts = user.posts

        return {
                   "posts": [post.json for post in posts]
               }, HTTPStatus.OK
