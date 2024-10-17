from pymongo import MongoClient
import json

# Connecting to MongoDB Atlas
client = MongoClient(
    "mongodb+srv://swayamsk:5UWqMJMs1aqJcizU@cluster0.97pxt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# Creating a database and collection
db = client["sample_database"]
collection = db["sample_collection"]

# Loading data from the sample.json file
with open("sample.json", "r") as file:  # Opening sample.json file in read mode
    data = json.load(file)  # Loading the json data from the file

# Inserting the data into MongoDB
collection.insert_many(data)

print(
    "Data of about 1Lakh records from sample.json file has been successfully inserted into MongoDB!"
)

client.close
