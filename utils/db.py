from motor.motor_asyncio import AsyncIOMotorClient
from utils.config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client.mental_health_tracker
