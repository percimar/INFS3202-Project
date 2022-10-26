from datetime import datetime
from http import HTTPStatus

from flask import request
from flask_restful import Resource
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from models import User, Post, Follower, Like


class PopulateResource(Resource):
    @staticmethod
    def post():
        if "password" not in request.form:
            return {}, HTTPStatus.BAD_REQUEST

        password = request.form["password"]
        hashed_pw = '$pbkdf2-sha256$29000$kxLCuHfuPQcg5Lw3pvT.Hw$VMXnNkpt2Q80.R0jMu319nuVU7hB6nlkYWfuMLOypYs'

        if not pbkdf2_sha256.verify(password, hashed_pw):
            return {}, HTTPStatus.BAD_REQUEST

        u1 = User(username="Asmar")
        u2 = User(username="admin")
        u3 = User(username="test")
        u4 = User(username="test2")
        u5 = User(username="Alice")
        u6 = User(username="UserBob")
        u7 = User(username="Ghassan")
        u8 = User(username="BigBrother")
        u9 = User(username="PierreGasly")
        u10 = User(username="MaxVerstappen")
        u11 = User(username="TheLoremIpsum")
        u12 = User(username="TimeTraveller")
        u13 = User(username="NotAHacker")

        users = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12, u13]
        User.save_users(users)

        big_brother = User.get_by_username("BigBrother")
        for user in users:
            Follower(user_id=big_brother.id, following_id=User.get_by_username(user.username).id).save()

        p1 = Post(author_id=User.get_by_username("TheLoremIpsum").id,
                  content="Proin congue risus volutpat metus dignissim, nec elementum lacus tristique. "
                          "Integer commodo dapibus nulla. Sed pulvinar condimentum risus dictum vulputate. "
                          "Vestibulum pulvinar imperdiet est, vel semper arcu interdum vitae. Donec "
                          "fermentum massa et justo viverra placerat. Mauris malesuada ornare semper. Morbi "
                          "sodales sit amet erat eu efficitur. Proin mauris sem, efficitur sit amet dictum "
                          "eu, aliquam ut ligula. Nulla dictum.").save()

        p2 = Post(author_id=User.get_by_username("TheLoremIpsum").id,
                  content="Cras augue dui, fringilla vitae neque sit amet, ullamcorper suscipit metus. "
                          "Suspendisse sit amet porttitor lorem. Duis scelerisque, tellus eget semper "
                          "blandit, sapien augue vehicula tortor, a tempor elit nulla eu nunc. Aenean "
                          "finibus nisl ut suscipit commodo. Donec consectetur hendrerit volutpat. Praesent "
                          "in tempor eros. In vehicula odio in est aliquam pellentesque. Mauris sit amet "
                          "elementum turpis, eget faucibus.").save()

        p3 = Post(author_id=User.get_by_username("TheLoremIpsum").id,
                  content="Nulla molestie nisi at elit pulvinar, et rhoncus dolor mattis. Etiam accumsan "
                          "libero eu lorem tempor consectetur. Donec a congue felis. Class aptent taciti "
                          "sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Fusce ut "
                          "erat pretium, dignissim tellus ut, egestas sapien. Praesent molestie erat vel "
                          "felis interdum, id congue libero varius. In in dui vitae ante ornare.").save()

        p4 = Post(author_id=User.get_by_username("TheLoremIpsum").id,
                  content="Maecenas lectus lacus, ultricies sed ultricies iaculis, gravida ac tellus. "
                          "Quisque convallis auctor porttitor. Curabitur rhoncus dui ex, a pharetra leo "
                          "gravida eu. Donec id velit nisi. Fusce sodales urna luctus augue aliquet "
                          "placerat. Fusce imperdiet vehicula lorem, commodo varius orci euismod eu. Sed "
                          "ultricies pretium erat id gravida. Vestibulum ante ipsum primis in faucibus orci "
                          "luctus et ultrices posuere.").save()

        p5 = Post(author_id=User.get_by_username("TheLoremIpsum").id,
                  content="In viverra varius dapibus. Mauris vehicula orci ut hendrerit dignissim. Donec "
                          "ante arcu, maximus posuere sagittis quis, aliquam eu ligula. Integer volutpat "
                          "tortor iaculis elit auctor congue. Donec eleifend id augue eu ultrices. "
                          "Pellentesque eget faucibus nisl. Etiam a maximus nibh, eget venenatis quam. Etiam "
                          "elementum tempor ante non sodales. Nam semper venenatis augue et.").save()

        p6 = Post(author_id=User.get_by_username("Asmar").id,
                  content="Why is it that a software project ALWAYS takes so much longer than you expect? "
                          "Like is there some kind of mind-reading code goblin that knows how long you think "
                          "a project is going to take, and then intentionall messes up the libraries you're "
                          "using so you have to waste time debugging them, or obfuscates the documentation "
                          "for that one specific use case you have as much as possible so it takes you "
                          "attempt after attempt of trial and error to figure out how the library authors "
                          "thought you should be forced to write your code. Initially they give you like "
                          "sixteen different ways to solve your problem, but the more you try them, "
                          "the more you realise that 14 of those don't work, 1 of those causes behaviour so "
                          "unexpected that you consider quitting programming forever, and one of them works "
                          "just well enough for you to be happy after hours of trial and error and make a "
                          "pact to never touch that piece of code again.").save()

        p6 = Post(author_id=User.get_by_username("Asmar").id,
                  content="In case it wasn't clear in my previous post, I was referring to this project, "
                          "and specifically the flask-SQLAlchemy library, a library that assumes you already "
                          "know everything about SQLAlchemy, and that you've read the SQLAlchemy "
                          "documentation cover to cover, because god forbid they document something that you "
                          "could find in the SQLAlchemy documentation. Instead you're constantly hopping "
                          "between Flask-SQLAlchemy documentation and SQLAlchemy documentation to figure out "
                          "different levels of abstraction you're working at.").save()

        p7 = Post(author_id=User.get_by_username("TimeTraveller").id,
                  content="This post is from the past, a past you will never know, for the living records of "
                          "this time are incomplete and unreliable. There are treasures hidden from this "
                          "past that would amaze even the rich and powerful. There are inventions lost here "
                          "that rival the great geniuses of Da Vinci or Linus Torvals. There is a history so "
                          "rich, so deep, that you could spend your entire life analysing a single day on "
                          "earth and still have more to learn.",
                  date_created=datetime(1, 10, 28, 11, 2, 16)).save()

        p8 = Post(author_id=User.get_by_username("TimeTraveller").id,
                  content="This post is from the future, a future you will never know, for the greatest "
                          "advances in modern medicine cannot prepare a journey this long or arduous. I "
                          "suppose you could acquire a time machine as I have and experience it that way, "
                          "but for reasons I cannot disclose time travel will soon become impossible. This "
                          "future is not immutable. A small step today will create ripples that will be "
                          "magnified through time into massive tsunamis in the future.",
                  date_created=datetime(3622, 11, 2, 23, 55, 16)).save()

        p9 = Post(author_id=User.get_by_username("NotAHacker").id,
                  content="I thought posts were supposed to be over 280 characters... :)").save()

        posts = [p1, p2, p3, p4, p5, p6, p7, p8, p9]

        pierre_gasly = User.get_by_username("PierreGasly")
        for post in posts:
            Like(user_id=pierre_gasly.id, post_id=post.id).save()

        return {}, HTTPStatus.OK
