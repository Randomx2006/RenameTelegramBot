import os
import time
import logging
import asyncio
from pyrogram import Client, idle
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid
import Config

# Set timezone to UTC (may help with msg_id sync issue)
os.environ["TZ"] = "UTC"
time.tzset()

# Set up logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Create Client instance with plugin support
app = Client(
    "Rename-Bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="RenameBot"),
)

# Async main function to run the bot
async def main():
    try:
        await app.start()
    except ApiIdInvalid:
        raise Exception("Your API_ID/API_HASH is not valid.")
    except ApiIdPublishedFlood:
        raise Exception("Too many uses of this API_ID. Use another one.")
    except AccessTokenInvalid:
        raise Exception("Your BOT_TOKEN is not valid.")
    
    uname = (await app.get_me()).username
    print(f"@{uname} Started Successfully!")

    await idle()
    await app.stop()
    print("Bot stopped. Alvida!")

# Run async main
if __name__ == "__main__":
    asyncio.run(main())
