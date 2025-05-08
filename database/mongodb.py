from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = "govcarpeta"

class MongoDB:
    client: AsyncIOMotorClient = None

    async def connect(self):
        self.client = AsyncIOMotorClient(MONGO_URL)
        self.db = self.client[DB_NAME]

    async def close(self):
        self.client.close()

mongo = MongoDB()
