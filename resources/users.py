from http import HTTPStatus

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from models import User, Follower


class UsersResource(Resource):
    def get(self, user_id: int):
        user = User.get_by_id(user_id)
        if user is None:
            return {"message": f"User with id {user_id} not found."}, HTTPStatus.NOT_FOUND
        return user.json, HTTPStatus.OK


class UsersListResource(Resource):
    def get(self):
        partial_name = request.args["name"] if "name" in request.args else ""
        matches = User.get_by_partial_username(partial_name)
        return {
                   "users": [user.json for user in matches]
               }, HTTPStatus.OK


class FollowResource(Resource):
    def post(self, user_id: int):
        logged_in_id = session["user"]
        if logged_in_id == user_id:
            return {"message": "Cannot follow yourself."}, HTTPStatus.BAD_REQUEST

        try:
            Follower(user_id=logged_in_id, following_id=user_id).save()
        except IntegrityError:
            # even though this is an error, the goal (have logged-in user following user_id) is accomplished,
            # so we return OK instead of an error status.
            return {"message": "Current user is already following."}, HTTPStatus.OK

        return {"message": "Current user is now following."}, HTTPStatus.OK


class FollowerListResource(Resource):
    def get(self, user_id: int):
        user = User.get_by_id(user_id)
        if user is None:
            return {"message": f"User with id {user_id} not found."}, HTTPStatus.NOT_FOUND

        followers = user.followers

        return {
                   "followers": [user.json for user in followers]
               }, HTTPStatus.OK


class FollowingListResource(Resource):
    def get(self, user_id: int):
        user = User.get_by_id(user_id)
        if user is None:
            return {"message": f"User with id {user_id} not found."}, HTTPStatus.NOT_FOUND

        users_followed = user.following

        return {
                   "following": [user.json for user in users_followed]
               }, HTTPStatus.OK
