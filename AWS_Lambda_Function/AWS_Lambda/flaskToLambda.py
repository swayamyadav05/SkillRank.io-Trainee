import json
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB connection string
client = MongoClient(
    "mongodb+srv://swayamsk:swayamsk@cluster0.97pxt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# Selecting the database and collection
db = client["sample_database"]
collection = db["sample_collection"]


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


def get_data_by_id(event, context):
    # Fetch a document by its ID.
    id = event["pathParameters"]["id"]  # Get ID from path parameters
    try:
        # Convert the id from string to ObjectID
        document = collection.find_one({"_id": ObjectId(id)})

        if document:
            document["_id"] = str(document["_id"])  # Convert ObjectID to string
            return {
                "statusCode": 200,
                "body": json.dumps(document),  # Return document as JSON
                "headers": {"Content-Type": "application/json"},
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Document not found"}),
                "headers": {"Content-Type": "application/json"},
            }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"error": "Invalid ID format or other error", "message": str(e)}
            ),
            "headers": {"Content-Type": "application/json"},
        }
