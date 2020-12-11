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

CODE = {}
status = {}


class HelloWorld(Resource):
    """Returns hello world"""

    def get(self):
        return {'hello': 'world'}


class SetScore(Resource):
    def get(self):
        return status

    def post(self):
        args = parser.parse_args()
        user = User.query.filter_by(name=args["name"]).first()
        score = Score(score=int(args["score"]), user=user)
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


class AddUser(Resource):
    def get(self):
        return status

    def post(self):
        args = parser.parse_args()
        user = User(name=args["name"])
        db.session.add(user)
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


api.add_resource(HelloWorld, '/')
api.add_resource(AddUser, "/add_user/")
api.add_resource(SetScore, "/set_score/")
