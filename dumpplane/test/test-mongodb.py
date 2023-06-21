#!/usr/bin/python3

import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb://127.0.0.1:27017"

client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Pinged deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db_name = "test"
table_name = "test-collection"

db = client[db_name]

collection = db[table_name]

post = {"author": "Mike", "uuid": "1001",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}

#post_id = collection.insert_one(post).inserted_id

filter = {'uuid': '1001'}

result = collection.replace_one(filter, post, True)


print(result.matched_count, result.modified_count)

client.close()
