from pymongo import MongoClient
import json

# Connecting to MongoDB Atlas
client = MongoClient(
    "mongodb+srv://swayamsk:5UWqMJMs1aqJcizU@cluster0.97pxt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# Creating a database and collection
db = client["sample_database"]
collection = db["sample_collection"]

# Defining the filter
filter_criteria = {
    "language": "Sindhi",  # Filtering for documents where language is Sindhi
    "version": {
        "$lte": 4.2
    },  # Filtering for documents where version is less than or equal to 4.2
}

# Fetching data from the collection based on the filter_criteria
results = collection.find(filter_criteria)

# Printing the fetched documents
for document in results:
    print(document)

# Closing the MongoDB connection
client.close
