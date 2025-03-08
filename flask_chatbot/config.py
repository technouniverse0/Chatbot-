import os 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for the chatbot."""
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MONGO_URI = os.getenv("MONGO_URI")
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

# Example usage
if __name__ == "__main__":
    print("OPENAI_API_KEY:", Config.OPENAI_API_KEY)
    print("MONGO_URI:", Config.MONGO_URI)
    print("DEBUG Mode:", Config.DEBUG)