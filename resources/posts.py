from datetime import datetime
from http import HTTPStatus

from flask import session, request
from flask_restful import Resource

from models import Post


class PostsResource(Resource):
    @staticmethod
    def get(post_id: int):
        post = Post.get_by_id(post_id)

        if post is None:
            return {"message": f"Post with id {post_id} not found. Perhaps it was deleted."}, HTTPStatus.NOT_FOUND

        return post.json, HTTPStatus.OK

    @staticmethod
    def patch(post_id: int):
        if "user" not in session:
            return {"message": "Please login first."}, HTTPStatus.UNAUTHORIZED

        user_id = session["user"]

        if "content" not in request.form:
            return {"message": "Required parameter 'content' missing from form-data."}, HTTPStatus.BAD_REQUEST

        content = request.form['content']

        if len(content) < 280:
            return {"message": "Post must be at least 280 characters."}, HTTPStatus.BAD_REQUEST

        post = Post.get_by_id(post_id)

        if post is None:
            return {"message": f"Post with id {post_id} not found. Perhaps it was deleted."}, HTTPStatus.NOT_FOUND

        if post.author_id != user_id:
            return {"message": "Cannot edit someone else's posts."}, HTTPStatus.FORBIDDEN

        post.content = content
        post.save()

        return post.json, HTTPStatus.OK

    @staticmethod
    def delete(post_id: int):
        if "user" not in session:
            return {"message": "Please login first."}, HTTPStatus.UNAUTHORIZED

        user_id = session["user"]
        post = Post.get_by_id(post_id)

        if post is None:
            return {"message": f"Post with id {post_id} not found. Perhaps it was deleted."}, HTTPStatus.NOT_FOUND

        if post.author_id != user_id:
            return {"message": "Cannot edit someone else's posts."}, HTTPStatus.FORBIDDEN

        post.delete()

        return {"message": "Post deleted."}, HTTPStatus.OK


class PostsListResource(Resource):
    @staticmethod
    def get():
        if "before" in request.args:
            before = request.args["before"]
            try:
                timestamp = datetime.fromisoformat(before)
                posts = Post.get_all(timestamp)
                return {
                           "posts": [post.json for post in posts]
                       }, HTTPStatus.OK
            except ValueError:
                return {
                           "message": "Query parameter 'before' needs to be a valid iso datetime string."
                       }, HTTPStatus.BAD_REQUEST

        posts = Post.get_all()
        return {
                   "posts": [post.json for post in posts]
               }, HTTPStatus.OK

    @staticmethod
    def post():
        if "user" not in session:
            return {"message": "Please login first."}, HTTPStatus.UNAUTHORIZED

        user_id = session["user"]

        if "content" not in request.form:
            return {"message": "Required parameter 'content' missing from form-data."}, HTTPStatus.BAD_REQUEST

        content = request.form['content']

        if len(content) < 280:
            return {"message": "Post must be at least 280 characters."}, HTTPStatus.BAD_REQUEST

        post = Post(content=content, author_id=user_id).save()
        return post.json, HTTPStatus.OK
