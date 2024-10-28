import json
import os
from bson import ObjectId
from pymongo import MongoClient
import bcrypt
import jwt
from datetime import datetime, timedelta

# MongoDB Client Initialization
MONGODB_URI = os.getenv("MONGODB_URI")
JWT_SECRET = os.getenv("JWT_SECRET")
if not MONGODB_URI or not JWT_SECRET:
    raise ValueError("Environment variables MONGODB_URI and JWT_SECRET must be set")

client = MongoClient(MONGODB_URI)
db = client["sample_database"]
users_collection = db["users_collection"]

# Response headers
headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
}


def lambda_handler(event, context):
    print("Received event: ", json.dumps(event))
    http_method = event.get("httpMethod", "").upper()
    path_parameters = event.get("pathParameters") or {}

    if http_method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "CORS preflight success"}),
        }

    try:
        # Route handling
        if http_method == "POST" and event["path"] == "/signup":
            return signup(json.loads(event["body"]))
        elif http_method == "POST" and event["path"] == "/login":
            return login(json.loads(event["body"]))
        elif http_method == "GET" and path_parameters and "id" in path_parameters:
            return get_user_by_id(path_parameters["id"])
        elif http_method == "GET":
            return get_paginated_users(event)
        elif http_method == "POST":
            return create_user(json.loads(event["body"]))
        elif http_method == "PUT" and "id" in path_parameters:
            return update_user_by_id(path_parameters["id"], json.loads(event["body"]))
        elif http_method == "DELETE" and "id" in path_parameters:
            return delete_user_by_id(path_parameters["id"])

        return {
            "statusCode": 405,
            "body": json.dumps({"error": f"Method {http_method} not allowed"}),
            "headers": headers,
        }
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error", "message": str(e)}),
            "headers": headers,
        }


# Authentication Handlers


def signup(body):
    try:
        username = body["username"]
        password = body["password"]

        # Check if user already exists
        if users_collection.find_one({"username": username}):
            return {
                "statusCode": 409,
                "body": json.dumps({"error": "Username already exists"}),
                "headers": headers,
            }

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Create user document
        new_user = {
            "username": username,
            "password": hashed_password.decode("utf-8"),
            "createdAt": datetime.utcnow(),
        }
        result = users_collection.insert_one(new_user)

        return {
            "statusCode": 201,
            "body": json.dumps(
                {
                    "message": "User created successfully",
                    "userId": str(result.inserted_id),
                }
            ),
            "headers": headers,
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Signup failed", "message": str(e)}),
            "headers": headers,
        }


def login(body):
    try:
        username = body["username"]
        password = body["password"]

        # Fetch the user by username
        user = users_collection.find_one({"username": username})
        if not user or not bcrypt.checkpw(
            password.encode("utf-8"), user["password"].encode("utf-8")
        ):
            return {
                "statusCode": 401,
                "body": json.dumps({"error": "Invalid username or password"}),
                "headers": headers,
            }

        # Generate JWT token
        token = jwt.encode(
            {"userId": str(user["_id"]), "exp": datetime.utcnow() + timedelta(hours=1)},
            JWT_SECRET,
            algorithm="HS256",
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Login successful", "token": token}),
            "headers": headers,
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Login failed", "message": str(e)}),
            "headers": headers,
        }


# CRUD Handlers


def get_paginated_users(event):
    query_params = event.get("queryStringParameters") or {}
    page = int(query_params.get("page", 1))
    limit = int(query_params.get("limit", 20))
    skip = (page - 1) * limit

    documents = list(users_collection.find({}).skip(skip).limit(limit))
    for doc in documents:
        doc["_id"] = str(doc["_id"])

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "data": documents,
                "page": page,
                "limit": limit,
                "total": users_collection.count_documents({}),
            }
        ),
        "headers": headers,
    }


def get_user_by_id(user_id):
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
            return {"statusCode": 200, "body": json.dumps(user), "headers": headers}
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "User not found"}),
                "headers": headers,
            }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"error": "Invalid ID format or other error", "message": str(e)}
            ),
            "headers": headers,
        }


def create_user(body):
    try:
        result = users_collection.insert_one(body)
        return {
            "statusCode": 201,
            "body": json.dumps(
                {
                    "message": "User created successfully",
                    "userId": str(result.inserted_id),
                }
            ),
            "headers": headers,
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Create failed", "message": str(e)}),
            "headers": headers,
        }


def update_user_by_id(user_id, body):
    try:
        result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": body})
        if result.matched_count:
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "User updated successfully"}),
                "headers": headers,
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "User not found"}),
                "headers": headers,
            }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Update failed", "message": str(e)}),
            "headers": headers,
        }


def delete_user_by_id(user_id):
    try:
        result = users_collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 1:
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "User deleted successfully"}),
                "headers": headers,
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "User not found"}),
                "headers": headers,
            }
    except Exception as e:
        print("Error deleting user:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to delete user"}),
            "headers": headers,
        }
