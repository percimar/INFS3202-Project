from http import HTTPStatus

from flask import request, session
from flask_restful import Resource

from models import User


class LoginResource(Resource):
    @staticmethod
    def post():
        if "user" not in request.form:
            return {"message": "Please provide a user"}, HTTPStatus.BAD_REQUEST
        user_name = request.form["user"]

        if len(user_name) == 0:
            return {"message": "Please provide a user"}, HTTPStatus.BAD_REQUEST

        if len(user_name) < 4:
            return {"message": "user name too short"}, HTTPStatus.BAD_REQUEST

        user = User.get_or_create_user(user_name)
        # set a cryptographically secured cookie
        session["user"] = user.id

        return {
                   **user.json,
                   "last_login": str(user.last_login)
               }, HTTPStatus.OK
