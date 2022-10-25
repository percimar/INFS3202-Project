from flask import Flask
from flask_restful import Api

# The noinspection comment is needed to prevent PyCharm from removing an unused import
# The unused import is needed to load the Models before Flask-SQLAlchemy tried to initialize the db
# without the unused import, no tables will be created in the db.
# See https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/#create-the-tables
# noinspection PyUnresolvedReferences
import models
from db import db
from resources import LoginResource, PostsResource, PostsListResource, UsersListResource, UsersResource, FollowResource


def create_app():
    app = Flask(__name__)
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://infs3202:change_password_here@localhost/infs3202',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    register_extensions(app)
    register_resources(app)

    return app


def register_extensions(app):
    db.init_app(app)
    with app.app_context():
        print("Dropping and creating tables")
        db.drop_all()
        db.create_all()


def register_resources(app):
    api = Api(app, prefix="/api")

    api.add_resource(LoginResource, "/login")
    api.add_resource(PostsListResource, "/posts")
    api.add_resource(PostsResource, "/posts/<int:post_id>")
    api.add_resource(UsersListResource, "/users")
    api.add_resource(UsersResource, "/users/<int:user_id>")
    api.add_resource(FollowResource, "/users/<int:user_id>/follow")


if __name__ == '__main__':
    create_app()
