from datetime import datetime
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
        if "name" not in request.args:
            return {"message": "Query parameter 'name' is mandatory."}, HTTPStatus.BAD_REQUEST

        partial_name = request.args["name"]

        # If the name is too small, we don't want to expose all our usernames
        if len(partial_name) < 3:
            return {"message": "Query parameter 'name' too short."}, HTTPStatus.BAD_REQUEST

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

        if "before" in request.args:
            before = request.args["before"]
            try:
                timestamp = datetime.fromisoformat(before)
                posts = Post.get_by_users([user.id for user in following], timestamp)
                return {
                           "posts": [post.json for post in posts]
                       }, HTTPStatus.OK
            except ValueError:
                return {
                           "message": "Query parameter 'before' needs to be a valid iso datetime string."
                       }, HTTPStatus.BAD_REQUEST

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
