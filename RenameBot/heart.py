import shutil
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import Message
from RenameBot.functions import progress
from RenameBot.database.users_mongo import Users  # ✅ MongoDB handler class

extensions = ["mp4", "mkv", "avi", "pdf"]

@Client.on_message(filters.private & (filters.document | filters.video) & ~filters.edited & filters.incoming)
async def _rename(bot: Client, msg: Message):
    user_id = msg.from_user.id
    user = await Users.get(user_id)

    if user and user.get("running", False):
        await msg.reply("One at a Time !", quote=True)
        return

    await Users.update(user_id, {"running": True})

    try:
        new_name_message = await bot.ask(
            msg.chat.id,
            "What should be the new name ? \n\n[To cancel send `/cancel`]",
            filters=filters.user(user_id) & filters.text,
        )

        if await is_cancel(new_name_message):
            await new_name_message.reply("Cancelled the Process !", quote=True)
            return

        old_name = msg.video.file_name if msg.video else msg.document.file_name
        new_name = new_name_message.text
        if "." in old_name:
            ext = old_name.rsplit(".", 1)[1]
            if "." not in new_name:
                new_name += f".{ext}"

        surely_question = await bot.send_message(
            msg.chat.id,
            f"Are you sure that '`{new_name}`' should be the new name ? \n\n"
            f"If yes, reply with 'y' or 'yes'. \nIf no, reply with 'n' or 'no'. New name will be asked again. \n"
            f"To cancel send `/cancel`\n\n[To prevent spelling/typing mistakes.]"
        )

        surely = await bot.listen(msg.chat.id, timeout=300, filters=filters.user(user_id) & filters.text)

        if await is_cancel(surely):
            await new_name_message.reply("Cancelled the Process !", quote=True)
            return

        if surely.text.lower() in ["n", "no"]:
            new_name = (await bot.ask(msg.chat.id, "\nWhat should be the new name ?\n")).text
            if "." in old_name:
                ext = old_name.rsplit(".", 1)[1]
                if "." not in new_name:
                    new_name += f".{ext}"

        await surely_question.delete()
        await surely.delete()

        user = await Users.get(user_id)
        if user.get("thumbnail_status") and user.get("thumbnail"):
            thumb = BytesIO(user["thumbnail"])
            thumb.name = "image.jpg"
        else:
            thumb = None

        downloading = await msg.reply("**Downloading...**")
        file_path = await msg.download(progress=progress, progress_args=(downloading, "Downloading..."))
        await downloading.edit("**Downloaded.**")
        await downloading.delete()

        uploading = await msg.reply("**Now Uploading...**")
        caption = msg.caption or ""

        if user.get("video_to") == "video":
            await bot.send_video(
                chat_id=msg.chat.id, video=file_path, file_name=new_name, caption=caption,
                thumb=thumb, progress=progress, progress_args=(uploading, "Uploading...")
            )
        else:
            await bot.send_document(
                chat_id=msg.chat.id, document=file_path, file_name=new_name, caption=caption,
                thumb=thumb, progress=progress, progress_args=(uploading, "Uploading...")
            )

        await uploading.edit("**Uploaded.**")
        await uploading.delete()

    except Exception as e:
        await msg.reply(f"Error : {e} \n\nTry Again and if still doesn't work then forward this message to @StarkBots !")

    finally:
        await Users.update(user_id, {"running": False})
        try:
            shutil.rmtree("downloads")
        except FileNotFoundError:
            pass

async def is_cancel(msg):
    return msg.text.startswith("/cancel")
