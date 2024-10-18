import os
from pymongo import MongoClient
import json

# Fetch MongoDB connection string from environment variables
MONGO_URI = os.getenv("MONGO_URI")


def MongoDB_connection():
    try:
        # Create a connection to MongoDB Atlas
        client = MongoClient(MONGO_URI)

        # Connect to the specific database
        db = client["your_database_name"]
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


def lambda_handler(event, context):
    # Connect to MongoDB
    db = MongoDB_connection()

    if db:
        # Example: Retrieve all data from a collection named 'your_collection'
        collection = db["your_collection"]
        documents = list(collection.find())

        # Convert MongoDB documents to JSON and return them as a response
        return
