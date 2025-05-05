from pymongo import MongoClient
from config import Config

# MongoDB connection URI from config
MONGO_DB_URI = Config.DATABASE_URL

# Create and expose a global MongoDB client session
SESSION = MongoClient(MONGO_DB_URI)

# Select your database
db = SESSION['RenameBotDB']

# Collections you plan to use
users_col = db['users']
files_col = db['files']  # if storing file metadata
settings_col = db['settings']  # optional for bot settings
