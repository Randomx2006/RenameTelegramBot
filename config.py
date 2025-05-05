import os

class Config:
    API_ID = int(os.getenv("API_ID", 25132804))
    API_HASH = os.getenv("API_HASH", "843d95d64eba173d7ef49ed4bb1440a8")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7591552604:AAHrwJwmVGwxbNTDphs-ku9wTisamrUuk0U")

    # MongoDB URL must start with mongodb:// or mongodb+srv://
    DATABASE_URL = os.getenv("DATABASE_URL", "mongodb+srv://ransome459:whitefield@cluster0.bffjdxl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

    # Optional configurations (edit as needed)
    DOWNLOAD_LOCATION = "./downloads"
    UPLOAD_AS_DOC = os.getenv("UPLOAD_AS_DOC", "False").lower() == "true"

    # Logging & Admin settings (customize these as needed)
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", 1002422067988))
    OWNER_ID = int(os.getenv("OWNER_ID", 7686184938))

    # Other optional settings
    CAPTION = os.getenv("CAPTION", "")
    PROGRESS = os.getenv("PROGRESS", "")

    MUST_JOIN = os.getenv("@𝘼𝙡𝙙𝙚𝙧𝙖𝙢𝙞𝙣 𝙤𝙣 𝙩𝙝𝙚 𝙎𝙠𝙮")  # or default to a channel username or ID, e.g., "@mychannel"
