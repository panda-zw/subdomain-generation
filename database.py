# database.py
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from a .env.local file

MONGO_URI = os.getenv("MONGO_URI")  # Set this in your .env.local file
client = AsyncIOMotorClient(MONGO_URI)
db = client["subdomain-generation"]  # Replace 'subdomain-generation' with your database name
