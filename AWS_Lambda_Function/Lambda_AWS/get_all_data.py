import json
from pymongo import MongoClient

# MongoDB connection string
client = MongoClient(
    "mongodb+srv://swayamsk:swayamsk@cluster0.97pxt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)


# Selecting the database and collection
db = client["swayam"]
collection = db["sample"]


def get_all_data(event, context):
    # Fetch all documents from the MongoDB collection."
    try:
        # Fetching all documents
        data = list(collection.find({}))
        # Convert MongoDB documents to a list of dictionaries
        for document in data:
            document["_id"] = str(document["_id"])  # Convert ObjectId to string
        return {
            "statusCode": 200,
            "body": json.dumps(data),  # Return data as JSON
            "headers": {"Content-Type": "application/json"},
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error", "message": str(e)}),
            "headers": {"Content-Type": "application/json"},
        }
