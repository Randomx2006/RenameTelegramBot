import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["rename_bot"]
users_collection = db["users"]

class Users:
    @staticmethod
    async def add_user(user_id: int):
        user = await users_collection.find_one({"_id": user_id})
        if not user:
            await users_collection.insert_one({"_id": user_id})
            return True
        return False

    @staticmethod
    async def get_all_users():
        return [user["_id"] async for user in users_collection.find()]

    @staticmethod
    async def count_users():
        return await users_collection.count_documents({})
