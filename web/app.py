from flask import Flask, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB
users = db.Users


def user_exists(username):
    if users.find({"Username": username}).count() == 0:
        return False
    else:
        return True


class Register(Resource):
    def post(self):
        posted_data = request.get_json()

        username = posted_data['Username']
        password = posted_data['Password']

        if user_exists(username):
            return {
                "Status": 401,
                "Message": "Invalid Username!"
            }

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 10
        })

        return {
            "Status": 200,
            "Message": "You've successfully signed up for the API"
        }


def verify_pw(username, password):
    if not user_exists(username):
        return False

    hashed_pw = users.find({"Username": username})[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False


def count_tokens(username):
    return users.find({"Username": username})[0]["Tokens"]


class Detect(Resource):
    def post(self):
        posted_data = request.get_json()

        username = posted_data['Username']
        password = posted_data['Password']
        text_1 = posted_data["Text_1"]
        text_2 = posted_data["Text_2"]

        if not user_exists(username):
            return {
                "Status": 401,
                "Message": "Invalid Username!"
            }

        correct_pw = verify_pw(username, password)

        if not correct_pw:
            return {
                "Status": 402,
                "Message": "Incorrect Password!"
            }

        num_tokens = count_tokens(username)

        if num_tokens <= 0:
            return {
                "Status": 403,
                "Message": "Not enough tokens! Please refill."
            }

        nlp = spacy.load('en_core_web_sm')

        text_1 = nlp(text_1)
        text_2 = nlp(text_2)

        # The close the ratio is to 1, the more similar
        ratio = text_1.similarity(text_2)

        current_tokens = count_tokens(username)

        users.update({
            "Username": username
        }, {
            "$set": {
                "Tokens": current_tokens - 1
            }
        })

        return {
            "Status": 200,
            "Similarity": ratio,
            "Message": "Similarity score calculated successfully"
        }


class Refill(Resource):
    def post(self):
        posted_data = request.get_json()

        username = posted_data['Username']
        password = posted_data['Admin_Password']
        refill_amount = posted_data["Refill"]

        if not user_exists(username):
            return {
                "Status": 401,
                "Message": "Invalid Username!"
            }

        # DO NOT USE IN PROD. Save hash in db under separate collection
        admin_pw = "abc123"

        if not password == admin_pw:
            return {
                "Status": 404,
                "Message": "Invalid Admin Password!"
            }

        current_tokens = count_tokens(username)
        users.update({
            "Username": username
        }, {
            "$set": {
                "Tokens": refill_amount + current_tokens
            }
        })

        return {
            "Status": 200,
            "Message": "Tokens refilled successfully"
        }


api.add_resource(Register, '/register')
api.add_resource(Detect, '/detect')
api.add_resource(Refill, '/refill')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
