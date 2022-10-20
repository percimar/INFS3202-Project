from flask_restful import Resource


class UsersResource(Resource):
    def get(self, user_id: int):
        pass  # return user details


class UsersListResource(Resource):
    def get(self):
        pass  # return users, with search


class FollowResource(Resource):
    def post(self, user_id: int):
        pass  # follow user
