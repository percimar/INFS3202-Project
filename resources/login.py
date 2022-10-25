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
        user = User.get_or_create_user(user_name)
        # set a cryptographically secured cookie
        session["user"] = user.id

        return {
                   "message": "Logged In",
                   **user.json
               }, HTTPStatus.OK
