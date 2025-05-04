import shutil
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from Data import Data
from RenameBot.database import users_col  # Ensure users_col is a pymongo collection


async def image_to_binary(image):
    with open(image, 'rb') as f:
        binary = f.read()
    return binary


@Client.on_callback_query()
async def _callbacks(bot: Client, callback_query: CallbackQuery):
    user = await bot.get_me()
    mention = user.mention
    query = callback_query.data.lower()
    user_id = callback_query.from_user.id

    if query == "home":
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=callback_query.message.message_id,
            text=Data.START.format(callback_query.from_user.mention, mention),
            reply_markup=InlineKeyboardMarkup(Data.buttons),
        )

    elif query == "about":
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=callback_query.message.message_id,
            text=Data.ABOUT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons),
        )

    elif query == "help":
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=callback_query.message.message_id,
            text="**Here's How to use me**\n" + Data.HELP,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons),
        )

    elif query in ["add_tn", "change_tn"]:
        await callback_query.message.delete()
        image_message = await bot.ask(user_id, "Send an image to set as thumbnail", filters=filters.photo)
        await bot.send_message(user_id, "Wait...Downloading and Saving...")
        image = await image_message.download()
        binary = await image_to_binary(image)
        users_col.update_one(
            {"_id": user_id},
            {"$set": {"thumbnail": binary, "thumbnail_status": True}},
            upsert=True
        )
        await image_message.reply("Thumbnail Set!", quote=True)
        shutil.rmtree("downloads")

    elif query == "remove_tn":
        users_col.update_one(
            {"_id": user_id},
            {"$set": {"thumbnail": None, "thumbnail_status": False}}
        )
        await callback_query.message.delete()
        await bot.send_message(user_id, "Thumbnail Removed!")

    elif query == "tn_status_change":
        user_data = users_col.find_one({"_id": user_id}) or {}
        status = not user_data.get("thumbnail_status", False)
        users_col.update_one(
            {"_id": user_id},
            {"$set": {"thumbnail_status": status}},
            upsert=True
        )
        switch = "On" if status else "Off"
        await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Change Thumbnail", callback_data="change_tn")],
                [InlineKeyboardButton("Remove Thumbnail", callback_data="remove_tn")],
                [InlineKeyboardButton(f"Thumbnail Status : {switch}", callback_data="tn_status_change")]
            ])
        )

    elif query == "video_to_setting":
        user_data = users_col.find_one({"_id": user_id}) or {}
        new_format = "document" if user_data.get("video_to", "video") == "video" else "video"
        users_col.update_one(
            {"_id": user_id},
            {"$set": {"video_to": new_format}},
            upsert=True
        )
        await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"Video to : {new_format.capitalize()}", callback_data="video_to_setting")]
            ])
        )
