from pymongo import MongoClient, UpdateOne
from pymongo.errors import InvalidOperation
from bson import ObjectId
import dateutil.parser as parser

# ensure you update your host information below!
host = "mongodb+srv://m220student:m220password@mflix-zqxvf.mongodb.net/test?retryWrites=true&w=majority"

# don't update this information
MFLIX_DB_NAME = "sample_mflix"
mflix = MongoClient(host)[MFLIX_DB_NAME]

# here we're making sure "lastupdated" exists in the document as a string
predicate = {"lastupdated": {"$exists": True, "$type": "string"}}
# this projection only sends the "lastupdated" and "_id" fields back to the client
projection = {"lastupdated": 1}

cursor = mflix.movies.find(predicate, projection)

# this will transform the "lastupdated" field to an ISODate() from a string
movies_to_migrate = []
for doc in cursor:
    doc_id = doc.get('_id')
    lastupdated = doc.get('lastupdated', None)
    movies_to_migrate.append(
        {
            "doc_id": ObjectId(doc_id),
            "lastupdated": parser.parse(lastupdated)
        }
    )

print(f"{len(movies_to_migrate)} documents to migrate")

try:
    bulk_updates = [UpdateOne(
        {"_id": movie.get("doc_id")},
        {"$set": {"lastupdated": movie.get("lastupdated")}}
    ) for movie in movies_to_migrate]

    # here's where the bulk operation is sent to MongoDB
    bulk_results = mflix.movies.bulk_write(bulk_updates)
    print(f"{bulk_results.modified_count} documents updated")

except InvalidOperation:
    print("no updates necessary")
except Exception as e:
    print(str(e))
