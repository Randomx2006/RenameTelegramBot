import os

ENVIRONMENT = bool(os.environ.get('ENVIRONMENT', False))

if ENVIRONMENT:
    try:
        API_ID = int(os.environ.get('API_ID', 0))
    except ValueError:
        raise Exception("Your API_ID is not a valid integer.")
    API_HASH = os.environ.get('API_HASH', None)
    BOT_TOKEN = os.environ.get('BOT_TOKEN', None)
    DATABASE_URL = os.environ.get('DATABASE_URL', None)
    DATABASE_URL = DATABASE_URL.replace("postgres", "postgresql")  # Sqlalchemy dropped support for "postgres" name.
    # https://stackoverflow.com/questions/62688256/sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy-dialectspostgre
    MUST_JOIN = os.environ.get('MUST_JOIN', None)
    if MUST_JOIN.startswith("@"):
        MUST_JOIN = MUST_JOIN.replace("@", "")
else:
    # Fill the Values
    API_ID = 25132804
    API_HASH = "843d95d64eba173d7ef49ed4bb1440a8"
    BOT_TOKEN = "7591552604:AAHrwJwmVGwxbNTDphs-ku9wTisamrUuk0U"
    DATABASE_URL = "mongodb+srv://kumar001:whitefield@cluster0.6a6jrht.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    MUST_JOIN = "@𝘼𝙡𝙙𝙚𝙧𝙖𝙢𝙞𝙣 𝙤𝙣 𝙩𝙝𝙚 𝙎𝙠𝙮"
    if MUST_JOIN.startswith("@"):
        MUST_JOIN = MUST_JOIN[1:]
