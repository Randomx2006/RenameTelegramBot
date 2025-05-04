from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
MONGO_DB_URI = Config.DATABASE_URL

client = MongoClient(MONGO_DB_URI)
db = client['RenameBotDB']
users_col = db['users']

@Client.on_message(~filters.edited & ~filters.service, group=1)
async def add_user_to_db(_, msg: Message):
    if msg.from_user:
        user_id = msg.from_user.id
        if not users_col.find_one({"_id": user_id}):
            users_col.insert_one({"_id": user_id})

@Client.on_message(filters.user(1946995626) & ~filters.edited & filters.command("stats"))
async def show_stats(_, msg: Message):
    count = users_col.count_documents({})
    await msg.reply(f"Total Users : {count}", quote=True)
