from pymongo import mongo_client
import pymongo
from app.config import settings

client = mongo_client.MongoClient(settings.DATABASE_URL)
print('Connected to MongoDB...')

db = client[settings.MONGO_INITDB_DATABASE]

User = db.users
Raffle = db.raffles
Purchase = db.purchase
Session = db.sessions

User.create_index([("email", pymongo.ASCENDING)], unique=True)
Raffle.create_index([("title", pymongo.ASCENDING)], unique=True)
Purchase.create_index([("bet", pymongo.ASCENDING)], unique=True)
Session.create_index([("key", pymongo.ASCENDING)], unique=True)