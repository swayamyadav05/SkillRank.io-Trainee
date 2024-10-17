import pymongo

if __name__ == "__main__":
    print("Welcome to pyMongo")
    client = pymongo.MongoClient(
        "mongodb+srv://swayam2956:Evx6BkxnQ6iwjWcO@cluster0.97pxt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )
    print(client)
    db = client["swayam"]
    collection = db["sample"]

    # Insert one
    dictionary = {"name": "Swayam", "age": "22"}
    collection.insert_one(dictionary)

    # Insert many
    insertThese = [
        {"Name": "Swayam", "Age": "40"},
        {"Name": "Shivam", "Age": "20"},
        {"Name": "Tushar", "Age": "22"},
        {"Name": "Mohit", "Age": "22"},
    ]
    collection.insert_many(insertThese)
