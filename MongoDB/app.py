# import awsgi
from flask import Flask, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

# Initializing the Flask app
app = Flask(__name__)

# Connecting to MongoDB Atlas
client = MongoClient(
    "mongodb+srv://swayamsk:swayamsk@cluster0.97pxt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# Selecting the database and collection
db = client["sample_database"]
collection = db["sample_collection"]


# Creating an endpoint to list all documents
@app.route("/api/data", methods=["GET"])
def get_all_data():
    # Fetching all documents from the collection
    data = list(collection.find({}))

    # Converting MongoDB documents to a list of dictionaries
    for document in data:
        document["_id"] = str(
            document["_id"]
        )  # Converting ObjectID to string for JSON serialization

    return (
        jsonify(data),
        200,
    )  # Return the data as JSON with a 200 HTTP status code (OK)


# Endpoint to fetch a document by its ID
@app.route("/api/data/<id>", methods=["GET"])
def get_data_by_id(id):
    try:
        # Converting the id from string to ObjectID and fetching the document
        document = collection.find_one({"_id": ObjectId(id)})

        if document:
            # Convert ObjectID to string for JSON serialization
            document["_id"] = str(document["_id"])
            return (
                jsonify(document),
                200,
            )  # Return the document as JSON with a 200 status code
        else:
            return (
                jsonify({"error": "Document not found"}),
                404,
            )  # If no document is found, return an error message with a 404 status code (Not Found)

    # Handling any errors
    except Exception as e:
        return (
            jsonify({"error": "Invalid ID format or other error", "message": str(e)}),
            400,
        )  # Return an error message with a 400 status code (Bad Request) and the exception message


# def lambda_handler(event, context):
#     return awsgi.response(app, event, context)


# Running the Flask app
if __name__ == "__main__":
    app.run(debug=True)  # Run the app in debug mode
