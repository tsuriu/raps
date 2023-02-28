import json

from pymongo import mongo_client
import pymongo

from app.config import settings

client = mongo_client.MongoClient(settings.DATABASE_URL)
print('Connected to MongoDB...')

db = client[settings.DATABASE_NAME]

User = db.users
Raffle = db.raffles
Purchase = db.purchase
Session = db.sessions
Parameters = db.parameters

User.create_index([("email", pymongo.ASCENDING)], unique=True)
Raffle.create_index([("title", pymongo.ASCENDING)], unique=True)
Purchase.create_index([("bet", pymongo.ASCENDING)], unique=True)
Session.create_index([("key", pymongo.ASCENDING)], unique=True)
Parameters.create_index([("config_description", pymongo.ASCENDING)], unique=True)


with open(f'app/parameters_collection.json') as f:
    parameters = json.load(f)
    
try:
    Parameters.insert_many(parameters)
except Exception as e:
    print(e)