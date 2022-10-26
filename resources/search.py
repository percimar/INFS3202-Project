from http import HTTPStatus

from flask import request
from flask_restful import Resource

from models import User, Post


class SearchResource(Resource):
    @staticmethod
    def get():
        if "q" not in request.args:
            return {"message": "Query parameter 'q' is mandatory."}, HTTPStatus.BAD_REQUEST

        query_string = request.args["q"]

        # If the query string is too small, we don't want to expose all our usernames
        # post matches will be unlikely anyway, it's best not to autocomplete until we have some characters
        if len(query_string) < 3:
            return {"message": "Query parameter 'q' is too short."}, HTTPStatus.BAD_REQUEST

        user_matches = User.get_by_partial_username(query_string)
        post_matches = Post.get_by_partial_content(query_string)

        return {
                   "users": [user.json for user in user_matches],
                   "posts": [post.json for post in post_matches]
               }, HTTPStatus.OK
