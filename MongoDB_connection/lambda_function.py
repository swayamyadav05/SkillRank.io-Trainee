import json
import os
from bson import ObjectId
from pymongo import MongoClient

# Initialize MongoDB client outside the handler for reusability
MONGODB_URI = os.getenv("MONGODB_URI")  # Ensure this is set in the environment
client = MongoClient(MONGODB_URI)

# Set up database and collection references
db = client["swayam"]
collection = db["sample"]

# Define headers for the response
headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",  # Adjust as needed for security
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
}


def lambda_handler(event, context):
    try:
        print("Received event: ", json.dumps(event))  # Log the incoming event
        http_method = event[
            "httpMethod"
        ].upper()  # Get HTTP method (GET, POST, PUT, DELETE)

        # Check for body content
        if "body" in event and event["body"]:
            print("Request Body:", event["body"])  # Log the request body
        else:
            print("No body received")

        # Check if path contains ID (for fetching single document)
        path_parameters = event.get("pathParameters", {})

        # Fetch or modify a document by ID if provided in the URL
        if path_parameters and "id" in path_parameters:
            if http_method == "GET":
                return get_data_by_id(path_parameters["id"])
            elif http_method == "PUT":
                return update_data_by_id(
                    path_parameters["id"], json.loads(event["body"])
                )
            elif http_method == "DELETE":
                return delete_data_by_id(path_parameters["id"])

        # Fallback to pagination if no specific ID is provided and method is GET
        if http_method == "GET":
            return get_paginated_data(event)

        return {
            "statusCode": 405,  # Method Not Allowed
            "body": json.dumps({"error": f"Method {http_method} not allowed"}),
            "headers": headers,
        }

    except Exception as e:
        # Log the error for debugging
        print(f"Error occurred: {str(e)}")

        # Return an error response with a 500 status code
        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "error": "Internal Server Error",
                    "message": str(e),
                }
            ),
            "headers": headers,
        }


def get_paginated_data(event):
    # Get query parameters for pagination (page and limit)
    query_params = (
        event.get("queryStringParameters", {}) or {}
    )  # Safely handle NoneType

    page = int(query_params.get("page", 1))  # Default to page 1 if not provided
    limit = int(query_params.get("limit", 1000))  # Default limit to 1000

    # Calculate the number of documents to skip based on the current page
    skip = (page - 1) * limit

    # Fetch a subset of documents using pagination
    documents = list(collection.find({}).skip(skip).limit(limit))

    # Convert ObjectId to string for each document
    for doc in documents:
        doc["_id"] = str(doc["_id"])

    # Return the paginated data in JSON format
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "data": documents,
                "page": page,
                "limit": limit,
                "total": collection.count_documents(
                    {}
                ),  # Optional: to know total count
            }
        ),
        "headers": headers,
    }


def get_data_by_id(id):
    # Fetch a document by its ID.
    try:
        # Convert the id from string to ObjectID
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
            "body": json.dumps(
                {"error": "Invalid ID format or other error", "message": str(e)}
            ),
            "headers": headers,
        }


def update_data_by_id(id, body):
    try:
        # Update the document by its ID with provided data
        result = collection.update_one(
            {"_id": ObjectId(id)},  # Filter by _id
            {"$set": body},  # Update document with provided body data
        )

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
