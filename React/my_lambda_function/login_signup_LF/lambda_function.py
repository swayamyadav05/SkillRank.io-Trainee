import json
import bcrypt
import os
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# Initialize MongoDB client
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["sample_database"]
users_collection = db["users"]


def lambda_handler(event, context):
    body = json.loads(event["body"])
    action = body.get("action")  # Either 'signup' or 'login'

    if action == "signup":
        return signup_user(body)
    elif action == "login":
        return login_user(body)
    else:
        return {"statusCode": 400, "body": json.dumps({"message": "Invalid action."})}


def signup_user(data):
    try:
        username = data["username"]
        password = data["password"]

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Insert the user in MongoDB
        user = {"_id": username, "password": hashed_password}
        users_collection.insert_one(user)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "User registered successfully."}),
        }
    except DuplicateKeyError:
        return {
            "statusCode": 409,
            "body": json.dumps({"message": "Username already exists."}),
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}


def login_user(data):
    try:
        username = data["username"]
        password = data["password"]

        # Find the user in MongoDB
        user = users_collection.find_one({"_id": username})
        if not user:
            return {
                "statusCode": 401,
                "body": json.dumps({"message": "Invalid username or password."}),
            }

        # Check the hashed password
        if bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Login successful."}),
            }
        else:
            return {
                "statusCode": 401,
                "body": json.dumps({"message": "Invalid username or password."}),
            }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}
