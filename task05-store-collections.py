import pymongo
from pymongo import MongoClient
from util import get_args

args = get_args()

mclient = MongoClient(args.mongo_client, 3306)

f = open(args.database+".collections.txt","w+")

for collection in mclient[args.database].list_collection_names():
    f.write(collection+"\n")
    
