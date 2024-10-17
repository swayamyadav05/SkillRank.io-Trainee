import pymongo

if __name__ == "__main__":
    print("Welcome to pyMongo")
    client = pymongo.MongoClient(
        "mongodb+srv://swayam2956:Evx6BkxnQ6iwjWcO@cluster0.97pxt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )
    print(client)
