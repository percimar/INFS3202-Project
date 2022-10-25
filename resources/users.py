from http import HTTPStatus

from flask import request
from flask_restful import Resource

from models import User


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
