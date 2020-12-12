from app import api, db
from app.models import User, Score
""" TODO: Put something meaningful"""
import os
import json
import shutil
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()

# For the code resource
parser.add_argument("score")
parser.add_argument("name")
parser.add_argument("new_name")

CODE = {}
status = {}


class HelloWorld(Resource):
    """Returns hello world"""

    def get(self):
        return {'hello': 'world'}


class GetScore(Resource):
    def get(self):
        return status

    def post(self):
        args = parser.parse_args()
        rank = 0
        user = User.query.filter_by(name=args["name"]).first()
        if user == None:
            status = {
                "success": False,
                "user": args["name"],
                "message": "User does not exist"
            }

            return status, 422
        else:
            score = Score.query.filter_by(user=user).first()
            if score == None:
                status = {
                    "success": False,
                    "user": args["name"],
                    "message": "User has no score"
                }
            else:
                # Get user's rank
                users = User.query.all()
                unsorted_users = {}
                for user in users:
                    unsorted_users[user.name] = user.score.score
                sorted_users = dict(
                    sorted(unsorted_users.items(),
                           key=lambda item: item[1], reverse=True))
                for i in range(len(sorted_users)):
                    if args["name"] == list(sorted_users.keys())[i]:
                        rank = i + 1
                        break

                status = {
                    "success": True,
                    "user": args["name"],
                    "score": score.score,
                    "rank": rank
                }
            return status, 200


class SetScore(Resource):
    def get(self):
        return status

    def post(self):
        args = parser.parse_args()
        user = User.query.filter_by(name=args["name"]).first()
        if user == None:
            status = {
                "success": False,
                "user": args["name"],
                "score": args["score"],
                "message": "User does not exist"
            }

            return status, 422

        # Check if the user's score exists
        score = Score.query.filter_by(user=user).first()
        if score == None:
            # The user's score does not exist, add new
            score = Score(score=int(args["score"]), user=user)
        else:
            score.score = int(args["score"])

        db.session.add(score)
        try:
            db.session.commit()
            status = {
                "success": True,
                "user": args["name"],
                "score": args["score"]
            }
        except Exception as _e:
            # TODO: Log the exception
            # log your exception in the way you want -> log to file, log as error with default logging, send by email. It's upon you
            db.session.rollback()
            db.session.flush()  # for resetting non-commited .add()
            status = {
                "success": False,
                "user": args["name"],
                "score": args["score"]
            }

        return status, 201


class GetAllScores(Resource):

    def get(self):
        users = User.query.all()
        for user in users:
            status[user.name] = user.score.score

        sorted_users = dict(
            sorted(status.items(), key=lambda item: item[1], reverse=True))

        return sorted_users


class AddUser(Resource):
    def get(self):
        return status

    def post(self):
        args = parser.parse_args()
        user = User(name=args["name"])
        score = Score(score=0, user=user)
        db.session.add(user)
        db.session.add(score)
        try:
            db.session.commit()
            status = {
                "success": True,
                "user": args["name"]
            }
        except Exception as _e:
            # TODO: Log the exception
            # log your exception in the way you want -> log to file, log as error with default logging, send by email. It's upon you
            db.session.rollback()
            db.session.flush()  # for resetting non-commited .add()
            status = {
                "success": False,
                "user": args["name"]
            }

        return status, 201


class UpdateUser(Resource):
    def post(self):
        args = parser.parse_args()
        user = User.query.filter_by(name=args["name"]).first()

        if args["new_name"] == None or args["name"] == None:
            status = {
                "success": False,
                "user": args["name"],
                "message": "Missing Arguments"
            }
            return status

        if user == None:
            status = {
                "success": False,
                "user": args["name"],
                "message": "User does not exist"
            }
            return status
        else:
            user.name = args["new_name"]
            db.session.add(user)

        try:
            db.session.commit()
            status = {
                "success": True,
                "user": user.name,
                "old_name": args["name"]
            }
        except Exception as _e:
            # TODO: Log the exception
            # log your exception in the way you want -> log to file, log as error with default logging, send by email. It's upon you
            db.session.rollback()
            db.session.flush()  # for resetting non-commited .add()
            status = {
                "success": False,
                "user": args["name"],
                "unadded_name": args["name"]
            }

        return status


api.add_resource(HelloWorld, '/')
api.add_resource(AddUser, "/add_user/")
api.add_resource(UpdateUser, "/update_user/")
api.add_resource(GetScore, "/get_score/")
api.add_resource(SetScore, "/set_score/")
api.add_resource(GetAllScores, "/get_all_scores/")
