import json
import bcrypt
from pymongo import MongoClient
import os

# Connect to MongoDB Atlas
client = MongoClient(host=os.environ.get("MONGODB_URI"))
db = client["sample_database"]
users_collection = db["users"]


def lambda_handler(event, context):
    # Print the entire event for debugging
    print("Received event:", json.dumps(event))

    # Use 'POST' as a default method for Lambda console testing
    http_method = event.get("httpMethod", "POST")  # Default to POST if not provided

    print("HTTP Method:", http_method)

    if http_method != "POST":
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"error": "Invalid request method, only POST is supported"}
            ),
        }

    # Parse the body
    try:
        body = event  # Assuming event contains the JSON payload directly
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON format", "details": str(e)}),
        }

    # Determine if it's a signup, login, or forgot password based on the presence of fields
    if "email" in body and "new_password" in body and "confirm_new_password" in body:
        return handle_forgot_password(body)
    elif "email" in body:
        return handle_signup(body)
    else:
        return handle_login(body)


# Function to handle signup
def handle_signup(body):
    username = body.get("username")
    password = body.get("password")
    email = body.get("email")

    if not username or not password or not email:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"error": "Username, password, and email are required for signup"}
            ),
        }

    if users_collection.find_one({"$or": [{"username": username}, {"email": email}]}):
        return {
            "statusCode": 409,
            "body": json.dumps({"error": "Username or email already exists"}),
        }

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    user = {
        "username": username,
        "email": email,
        "password": hashed_password.decode("utf-8"),
    }

    try:
        users_collection.insert_one(user)
        return {"statusCode": 200, "body": json.dumps({"message": "Signup successful"})}
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to create user", "details": str(e)}),
        }


# Function to handle login
def handle_login(body):
    username = body.get("username")
    password = body.get("password")

    if not username or not password:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"error": "Username and password are required for login"}
            ),
        }

    user = users_collection.find_one({"username": username})

    if not user:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Account not found. Please sign up."}),
        }

    if bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Login successful !!"}),
        }

    if not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        return {
            "statusCode": 403,
            "body": json.dumps({"error": "Incorrect password. Reset it now?"}),
        }
    else:
        return {
            "statusCode": 401,
            "body": json.dumps({"error": "Please check your credentials."}),
        }


# Function to handle forgot password
def handle_forgot_password(body):
    email = body.get("email")
    new_password = body.get("new_password")
    confirm_new_password = body.get("confirm_new_password")

    if not email or not new_password or not confirm_new_password:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"error": "Email, new password, and confirm new password are required"}
            ),
        }

    if new_password != confirm_new_password:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"error": "New password and confirm new password do not match"}
            ),
        }

    user = users_collection.find_one({"email": email})

    if not user:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "User with this email does not exist"}),
        }

    # Hash the new password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), salt)

    try:
        # Update the user's password in the database
        users_collection.update_one(
            {"email": email}, {"$set": {"password": hashed_password.decode("utf-8")}}
        )
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Password updated successfully"}),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"error": "Failed to update password", "details": str(e)}
            ),
        }
