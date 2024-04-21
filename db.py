import motor.motor_asyncio
from decouple import config

client = motor.motor_asyncio.AsyncIOMotorClient(config("MONGO_URL"))
db = client.get_database("spotify-yt-sync-db")