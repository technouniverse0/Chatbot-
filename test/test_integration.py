import sys
import os
import logging

# Add the project root to sys.path so that 'services' can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.rag_pipeline import RAGPipeline
from services.llm_service import LLMService

def run_integration_test(user_query):
    try:
        # Initialize the RAG pipeline and retrieve context for the given query.
        logging.info("Initializing RAGPipeline...")
        rag = RAGPipeline()
        context = rag.retrieve_context(user_query)
        logging.info("Retrieved context:\n%s", context)
        
        # Initialize the LLM service and generate a response using the query and context.
        logging.info("Initializing LLMService...")
        llm = LLMService()
        response = llm.get_response(user_query, context)
        logging.info("Generated response:\n%s", response)
        
        return response
    except Exception as e:
        logging.error("Integration test failed: %s", e)
        raise e

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Define a sample user query for testing
    test_query = "How can I reset my password?"
    print("Running integration test with query:", test_query)
    
    result = run_integration_test(test_query)
    print("\nFinal Response from Chatbot:\n", result)
