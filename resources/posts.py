from flask_restful import Resource, reqparse

content_parser = reqparse.RequestParser()
content_parser.add_argument('content', required=True)


class PostsResource(Resource):
    def get(self, post_id: int):
        if post_id is None:
            # return Bad request
            return
        # get post from db and return it

    def patch(self, post_id: int):
        args = content_parser.parse_args()
        content: str = args['content']
        pass  # update post

    def delete(self, post_id: int):
        pass  # delete post


class PostsListResource(Resource):
    def get(self):
        pass  # return posts

    def post(self):
        args = content_parser.parse_args()
        content: str = args['content']
        pass  # create post
