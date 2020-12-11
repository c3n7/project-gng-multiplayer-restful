from app import api
""" TODO: Put something meaningful"""
import os
import json
import shutil
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()

# For the code resource
parser.add_argument("code")
parser.add_argument("test")

CODE = {}


class HelloWorld(Resource):
    """Returns hello world"""

    def get(self):
        return {'noma': 'tupu'}


class EvalCode(Resource):
    """Runs code and returns the result"""

    def get(self):
        return CODE

    def post(self):
        args = parser.parse_args()
        CODE = {
            "code": args["code"],
            "test": args["test"]
        }

        # Write the code file to disk
        os.mkdir("tmp")
        with open("tmp/user_code.py", 'w') as f:
            f.write(CODE["code"])

        with open("tmp/test_code.py", 'w') as f:
            f.write(CODE["test"])

        os.system("py.test --json-report")
        RESULT = {}

        with open(".report.json") as f:
            RESULT = json.load(f)

        # A bit of clean up
        shutil.rmtree("tmp")
        os.remove(".report.json")

        # Return the goodies
        print(json.dumps(RESULT, indent=1))
        return RESULT, 201


api.add_resource(HelloWorld, '/')
api.add_resource(EvalCode, "/code/")
