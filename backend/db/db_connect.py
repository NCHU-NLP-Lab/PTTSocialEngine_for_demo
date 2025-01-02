from dotenv import load_dotenv
import motor.motor_asyncio
import os

load_dotenv()
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db = client.pttengine
result_collection = db.get_collection("result")