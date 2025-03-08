import pandas as pd
import json
import sys
import os


# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import json
from pymongo import MongoClient
from flask_chatbot.config import Config
from exception.exception import CustomException
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Connect to MongoDB
    client = MongoClient(Config.MONGO_URI)
    db = client.get_database("chatbot_db")  # Change DB name if needed
    collection = db.get_collection("support_tickets")  # Change collection name if needed

    # Load CSV file
    csv_path = "C:\Modular Chatbot\data\customer_support_tickets.csv"  # Update this with your actual file path
    df = pd.read_csv(csv_path)

    # Drop rows with null values
    df_cleaned = df.dropna()

    # Convert DataFrame to JSON
    json_records = json.loads(df_cleaned.to_json(orient="records"))

    # Clear existing collection (optional)
    collection.delete_many({})  # Uncomment if you want to remove old data

    # Insert clean data into MongoDB
    collection.insert_many(json_records)
    logger.info(f"✅ Inserted {len(json_records)} cleaned records into MongoDB!")

except Exception as e:
    logger.error("❌ Error while processing data")
    raise CustomException(str(e))
