import json
import os
from bson import ObjectId
from pymongo import MongoClient

# Initialize MongoDB client outside the handler for reusability
MONGODB_URI = os.getenv("MONGODB_URI")  # Ensure this is set in the environment
if not MONGODB_URI:
    raise ValueError("MONGODB_URI is not set in the environment")

client = MongoClient(MONGODB_URI)

# Set up database and collection references
db = client["sample_database"]
collection = db["sample_collection"]

# Define headers for the response
headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
}


def lambda_handler(event, context):
    try:
        # Early logging for visibility on all requests
        print("Received event: ", json.dumps(event))
        http_method = event.get("httpMethod", "").upper()
        
        # Safely handle pathParameters if it is None
        path_parameters = event.get("pathParameters") or {}

        if 'body' in event:
            print(f"Body: {event['body']}")

        # Handle preflight request
        if http_method == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({"message": "CORS preflight success"})
            }

        # Path Parameter Check for ObjectId
        if "id" in path_parameters and not ObjectId.is_valid(path_parameters["id"]):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid ObjectId format"}),
                "headers": headers,
            }

        # Logic for handling different methods
        if http_method == "GET":
            if path_parameters and "id" in path_parameters:
                return get_data_by_id(path_parameters["id"])
            return get_paginated_data(event)
        
        elif http_method == "POST":
            return create_data(json.loads(event["body"]))

        elif http_method == "PUT" and "id" in path_parameters:
            return update_data_by_id(path_parameters["id"], json.loads(event["body"]))

        elif http_method == "DELETE" and "id" in path_parameters:
            return delete_data_by_id(path_parameters["id"])

        return {
            "statusCode": 405,  # Method Not Allowed
            "body": json.dumps({"error": f"Method {http_method} not allowed"}),
            "headers": headers,
        }

    except Exception as e:
        # Log the error for debugging
        print(f"Error occurred: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error", "message": str(e)}),
            "headers": headers,
        }


def get_paginated_data(event):
    # Safely handle queryStringParameters if it is None
    query_params = event.get("queryStringParameters") or {}

    page = int(query_params.get("page", 1))  # Default to page 1 if not provided
    limit = int(query_params.get("limit", 20))  # Default limit to 20

    skip = (page - 1) * limit  # Calculate skip value

    # Fetch a subset of documents using pagination
    documents = list(collection.find({}).skip(skip).limit(limit))

    # Convert ObjectId to string for each document
    for doc in documents:
        doc["_id"] = str(doc["_id"])

    # Return the paginated data in JSON format
    return {
        "statusCode": 200,
        "body": json.dumps({
            "data": documents,
            "page": page,
            "limit": limit,
            "total": collection.count_documents({}),  # Optional: to know total count
        }),
        "headers": headers,
    }


def get_data_by_id(id):
    try:
        # Fetch a document by its ID
        document = collection.find_one({"_id": ObjectId(id)})

        if document:
            document["_id"] = str(document["_id"])  # Convert ObjectID to string
            return {
                "statusCode": 200,
                "body": json.dumps(document),  # Return document as JSON
                "headers": headers,
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Document not found"}),
                "headers": headers,
            }

    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid ID format or other error", "message": str(e)}),
            "headers": headers,
        }


def create_data(body):
    try:
        # Insert a new document in the collection
        result = collection.insert_one(body)
        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Document created successfully", "id": str(result.inserted_id)}),
            "headers": headers,
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Create failed", "message": str(e)}),
            "headers": headers,
        }


def update_data_by_id(id, body):
    try:
        # Update the document by its ID with provided data
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": body})

        if result.matched_count:
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Document updated successfully"}),
                "headers": headers,
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Document not found"}),
                "headers": headers,
            }

    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Update failed", "message": str(e)}),
            "headers": headers,
        }


def delete_data_by_id(id):
    try:
        # Delete the document by its ID
        result = collection.delete_one({"_id": ObjectId(id)})

        if result.deleted_count:
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Document deleted successfully"}),
                "headers": headers,
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Document not found"}),
                "headers": headers,
            }

    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Delete failed", "message": str(e)}),
            "headers": headers,
        }
