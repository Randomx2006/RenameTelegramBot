from pymongo import MongoClient
from config import Config

MONGO_DB_URI = Config.DATABASE_URL

client = MongoClient(MONGO_DB_URI)
db = client['RenameBotDB']  # You can change this to any DB name you want
users_col = db['users']
