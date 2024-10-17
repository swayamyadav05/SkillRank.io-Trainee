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
