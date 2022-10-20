from flask_restful import Resource


class LoginResource(Resource):
    def post(self, user_name: str):
        if user_name is None:
            # return Bad request
            return
        # login and update last_login if exists, else register
        # return logged in user or jwt
