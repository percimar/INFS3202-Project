from http import HTTPStatus

from flask import session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from models import Follower, User


class FollowResource(Resource):
    @staticmethod
    def post(user_id: int):
        if "user" not in session:
            return {"message": "Please login first."}, HTTPStatus.UNAUTHORIZED

        logged_in_id = session["user"]
        if logged_in_id == user_id:
            return {"message": "Cannot follow yourself."}, HTTPStatus.BAD_REQUEST

        try:
            Follower(user_id=logged_in_id, following_id=user_id).save()
        except IntegrityError:
            # even though this is an error, the goal (have logged-in user following user_id) is accomplished,
            # so we return OK instead of an error status.
            return {"message": "Current user is already following this user."}, HTTPStatus.OK

        return {"message": "Current user is now following this user."}, HTTPStatus.OK


class UnfollowResource(Resource):
    @staticmethod
    def post(user_id: int):
        if "user" not in session:
            return {"message": "Please login first."}, HTTPStatus.UNAUTHORIZED

        logged_in_id = session["user"]
        if logged_in_id == user_id:
            return {"message": "Cannot unfollow yourself."}, HTTPStatus.BAD_REQUEST

        follower_record = Follower.get_record(logged_in_id, user_id)

        if follower_record is None:
            # even though this is an error, the goal (have logged-in user not following user_id) is accomplished,
            # so we return OK instead of an error status.
            return {"message": "Current user was not following this user."}, HTTPStatus.OK

        follower_record.delete()

        return {"message": "Current user is no longer following this user."}, HTTPStatus.OK


class FollowerListResource(Resource):
    @staticmethod
    def get(user_id: int):
        user = User.get_by_id(user_id)
        if user is None:
            return {"message": f"User with id {user_id} not found."}, HTTPStatus.NOT_FOUND

        followers = user.followers

        return {
                   "followers": [user.json for user in followers]
               }, HTTPStatus.OK


class FollowingListResource(Resource):
    @staticmethod
    def get(user_id: int):
        user = User.get_by_id(user_id)
        if user is None:
            return {"message": f"User with id {user_id} not found."}, HTTPStatus.NOT_FOUND

        users_followed = user.following

        return {
                   "following": [user.json for user in users_followed]
               }, HTTPStatus.OK
