from RenameBot.database import db

users_collection = db.users

async def add_user(user_id):
    existing = await users_collection.find_one({"_id": user_id})
    if not existing:
        await users_collection.insert_one({"_id": user_id})

async def get_all_users():
    users = []
    async for user in users_collection.find({}):
        users.append(user["_id"])
    return users

async def count_users():
    return await users_collection.count_documents({})
