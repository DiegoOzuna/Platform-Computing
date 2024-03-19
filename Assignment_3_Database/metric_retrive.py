import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#grab key from hidden json file...
with open('key.json', 'r') as f:
    password = json.load(f)

#URI Password is hidden 
uri = f"mongodb+srv://007157781:{password}@cluster0.hy4vdxy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['metrics']

# Iterate over each collection in the database
for collection_name in db.list_collection_names():
    collection = db[collection_name]
    print(f"Collection: {collection_name}")
    
    # Iterate over each document in the collection
    for document in collection.find():
        # Exclude the '_id' field
        del document['_id']
        print(document)
