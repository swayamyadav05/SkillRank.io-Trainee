import pymongo

if __name__ == "__main__":
    print("Welcome to pyMongo")
    client = pymongo.MongoClient(
        "mongodb+srv://swayam2956:Evx6BkxnQ6iwjWcO@cluster0.97pxt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )
    print(client)
    db = client["swayam"]
    collection = db["sample"]

    # one = collection.find_one({"Name": "Mohit"})
    # print(one)
    # allDocs = collection.find({"Name": "Mohit"})
    # for item in allDocs:
    #     print(item)

    allDocs = collection.find({"Name": "Mohit"}, {"Name": 1, "_id": 0})
    for item in allDocs:
        print(item)
