from flask import Flask
from flask_restful import Api

from resources import LoginResource, PostsResource, PostsListResource, UsersListResource, UsersResource, FollowResource

app = Flask(__name__)
api = Api(app, prefix="/api")

api.add_resource(LoginResource, "/login")
api.add_resource(PostsListResource, "/posts")
api.add_resource(PostsResource, "/posts/<int:post_id>")
api.add_resource(UsersListResource, "/users")
api.add_resource(UsersResource, "/users/<int:user_id>")
api.add_resource(FollowResource, "/users/<int:user_id>/follow")


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
