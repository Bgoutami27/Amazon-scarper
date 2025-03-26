from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["amazon_scraper"]
collection = db["tv_details"]

# Fetch and print all stored TV details
print("📌 Stored TV Details in MongoDB:")
for doc in collection.find({}, {"_id": 0}):  # Exclude "_id" field
    print(doc)
