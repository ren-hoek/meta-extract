import pymongo as py
from bson.son import SON

client = py.MongoClient('mongo')
db = client['docs']
col = db['aug_meta']

pipeline = [
    {"$group": {"_id": "$Content-Type.Content", "count": {"$sum": 1}}},
    {"$sort": SON([("count", -1), ("_id", -1)])}
]

for row in col.aggregate(pipeline):
    print(row)
