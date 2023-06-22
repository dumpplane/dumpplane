#!/usr/bin/python3

import datetime
from elasticsearch import Elasticsearch

uri = "http://localhost:9200"

client = Elasticsearch(uri)


db_name = "test"
table_name = "test-collection"

name = "test002"

doc = {"author": "Mike", "uuid": "1002",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}

resp = client.index(index=db_name, id=name, document=doc)
print(resp['_version'])

