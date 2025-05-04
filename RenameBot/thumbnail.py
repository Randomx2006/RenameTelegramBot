from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from motor.motor_asyncio import AsyncIOMotorClient
from io import BytesIO
import os

# MongoDB config (make sure to set MONGO_URI in your config)
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["rename_bot"]
users_collection = db["users"]

@Client.on_message(filters.private & filters.command(["thumbnail", "tn"]) & ~filters.edited)
async def _thumbnail(_, msg: Message):
    user_id = msg.from_user.id
    user = await users_collection.find_one({"_id": user_id})

    if not user:
        await users_collection.insert_one({
            "_id": user_id,
            "thumbnail": None,
            "thumbnail_status": False
        })
        switch = "Off"
        thumbnail = None
    else:
        switch = "On" if user.get("thumbnail_status", False) else "Off"
        thumbnail = user.get("thumbnail")

    if thumbnail:
        thumbnail = BytesIO(thumbnail)
        thumbnail.name = "image.jpg"
        await msg.reply_photo(
            thumbnail,
            caption="This is the current thumbnail",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✨ Change Thumbnail ✨", callback_data="change_tn")],
                [InlineKeyboardButton("✨ Remove Thumbnail ✨", callback_data="remove_tn")],
                [InlineKeyboardButton(f"Thumbnail Status : {switch}", callback_data="tn_status_change")]
            ])
        )
    else:
        await msg.reply(
            "No Thumbnail Found",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✨ Add Thumbnail ✨", callback_data="add_tn")]
            ])
        )
