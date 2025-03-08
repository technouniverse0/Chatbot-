import re
import sys
import os


# Add project root to sys.path to resolve flask_chatbot package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import re
import logging
from pymongo import MongoClient
from flask_chatbot.config import Config
from exception.exception import CustomException

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class RAGPipeline:
    def __init__(self):
        try:
            # Connect to MongoDB Atlas using the URI from config.py
            self.client = MongoClient(Config.MONGO_URI)
            self.db = self.client.get_database("chatbot_db")  # Update if your DB name is different
            self.collection = self.db.get_collection("support_tickets")  # Update collection name if needed
            logger.info("Connected to MongoDB for RAGPipeline.")
        except Exception as e:
            logger.error("Error connecting to MongoDB in RAGPipeline.")
            raise CustomException(str(e))

    def retrieve_context(self, query, limit=3):
        """
        Retrieve relevant support ticket documents based on the query.
        This uses a simple regex-based search over 'Ticket Subject', 'Ticket Description', and 'Resolution' fields.
        """
        try:
            # Create a regex pattern for the query (case-insensitive)
            regex = re.compile(query, re.IGNORECASE)
            
            # Query MongoDB: search for the query in the desired fields
            results = list(self.collection.find({
                "$or": [
                    {"Ticket Subject": regex},
                    {"Ticket Description": regex},
                    {"Resolution": regex}
                ]
            }).limit(limit))
            
            if not results:
                logger.info("No relevant context found for query: " + query)
                return "No relevant context found."
            
            # Combine the results into a single context string for further processing
            context = "\n".join(
                [
                    f"Subject: {doc.get('Ticket Subject', 'N/A')}\n"
                    f"Description: {doc.get('Ticket Description', 'N/A')}\n"
                    f"Resolution: {doc.get('Resolution', 'N/A')}"
                    for doc in results
                ]
            )
            logger.info("Retrieved relevant context for query.")
            return context
        except Exception as e:
            logger.error("Error retrieving context in RAGPipeline.")
            raise CustomException(str(e))
    
    def generate_response(self, query, llm_service):
        """
        Generate a response using the provided LLM service.
        'llm_service' should be an object that implements a method get_response(query, context).
        """
        try:
            context = self.retrieve_context(query)
            # Call the LLM service to generate a response based on query and retrieved context
            response = llm_service.get_response(query, context)
            return response
        except Exception as e:
            logger.error("Error generating response in RAGPipeline.")
            raise CustomException(str(e))

# Example usage
if __name__ == "__main__":
    try:
        rag = RAGPipeline()
        test_query = "password reset"
        context = rag.retrieve_context(test_query)
        print("Retrieved Context:\n", context)
    except Exception as e:
        print(e)
