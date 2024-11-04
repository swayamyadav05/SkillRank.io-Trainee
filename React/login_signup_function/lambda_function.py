import json
import bcrypt
from pymongo import MongoClient
import os

# Connect to MongoDB Atlas
client = MongoClient(host=os.environ.get("MongoDB_URI"))
db = client["sample_database"]
users_collection = db["users"]

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))  # Log the entire event for inspection

    action = event.get('action')  # Get the action from the event
    if action == 'signup':
        return handle_signup(event.get('username'), event.get('email'), event.get('password'))
    elif action == 'login':
        return handle_login(event)  # Pass the whole event for login
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid action. Please specify either "signup" or "login".'})
        }

# Function to handle signup
def handle_signup(username, email, password):
    print("MongoDB URI:", os.environ.get("MongoDB_URI"))  # Log URI to confirm connection string availability
    
    if users_collection.find_one({'$or': [{'username': username}, {'email': email}]}):
        return {
            'statusCode': 409,
            'body': json.dumps({'error': 'Username or email already exists'})
        }

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    user = {
        'username': username,
        'email': email,
        'password': hashed_password.decode('utf-8')
    }

    print("Attempting to insert user:", user)  # Log user data to confirm it's as expected

    try:
        users_collection.insert_one(user)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Signup successful'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to create user', 'details': str(e)})
        }

# Function to handle login
def handle_login(body):
    print("Received login data:", body)  # Log the body to verify it contains expected fields

    username = body.get('username')
    password = body.get('password')

    if not username or not password:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Username and password are required for login'})
        }

    user = users_collection.find_one({'username': username})

    if not user:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': "Account not found. Please sign up."})
        }

    if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Login successful !!'})
        }

    return {
        'statusCode': 403, 
        'body': json.dumps({'error': 'Incorrect password.'})
    }

# The handle_forgot_password function is omitted for brevity


# Function to handle forgot password
def handle_forgot_password(body):
    email = body.get('email')
    new_password = body.get('new_password')
    confirm_new_password = body.get('confirm_new_password')

    if not email or not new_password or not confirm_new_password:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Email, new password, and confirm new password are required'})
        }

    if new_password != confirm_new_password:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'New password and confirm new password do not match'})
        }

    user = users_collection.find_one({'email': email})

    if not user:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'User with this email does not exist'})
        }

    # Hash the new password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)

    try:
        # Update the user's password in the database
        users_collection.update_one({'email': email}, {'$set': {'password': hashed_password.decode('utf-8')}})
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Password updated successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to update password', 'details': str(e)})
        }
