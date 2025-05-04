from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from motor.motor_asyncio import AsyncIOMotorClient
from io import BytesIO
import os

# MongoDB config (ensure MONGO_URI is set in environment)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client.rename_bot  # database name
users_collection = db.users  # collection name

@Client.on_message(filters.private & filters.command(["thumbnail", "tn"]) & ~filters.edited)
async def thumbnail_handler(_, msg: Message):
    user_id = msg.from_user.id
    user = await users_collection.find_one({"_id": user_id})

    if not user:
        # Initialize the user document
        user = {
            "_id": user_id,
            "thumbnail": None,
            "thumbnail_status": False
        }
        await users_collection.insert_one(user)

    switch = "On" if user.get("thumbnail_status", False) else "Off"
    thumbnail_data = user.get("thumbnail")

    if thumbnail_data:
        thumb_io = BytesIO(thumbnail_data)
        thumb_io.name = "thumbnail.jpg"
        await msg.reply_photo(
            thumb_io,
            caption="This is your current thumbnail.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✨ Change Thumbnail ✨", callback_data="change_tn")],
                [InlineKeyboardButton("❌ Remove Thumbnail ❌", callback_data="remove_tn")],
                [InlineKeyboardButton(f"🟢 Status: {switch}", callback_data="tn_status_change")]
            ])
        )
    else:
        await msg.reply(
            "No thumbnail found.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add Thumbnail", callback_data="add_tn")]
            ])
        )
