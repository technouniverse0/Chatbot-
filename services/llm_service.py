import sys
import os


# Ensure the project root is in sys.path so that imports work correctly.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from flask_chatbot.config import Config
from exception.exception import CustomException

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LLMService:
    def __init__(self):
        try:
            # Initialize the ChatOpenAI model.
            self.chat_model = ChatOpenAI(
                openai_api_key=Config.OPENAI_API_KEY,
                model_name="gpt-3.5-turbo",
                temperature=0.5,
                streaming=True
            )
            # Define the QA prompt template.
            qa_template = """
            You are Tecqsa, an intelligent, detailed, and helpful assistant built by Bhavik Ramina for Tecstaq and Green Aims Pvt Ltd. Your purpose is to analyze the provided context from uploaded documents (PDFs, Excel, CSV, etc.) and deliver a structured, comprehensive answer.

            Guidelines:
           1. Carefully extract relevant information from the context.
           2. If the context provides sufficient details, answer step-by-step.
           3. If the context is sparse or only partially relevant, provide general advice and mention that the available context is limited.
           4. If no useful context is provided, clearly state: "I don't have enough context to provide a specific answer." Then, provide general best-practice advice if possible.
           5. Organize your answer using bullet points, lists, or sections.
           6. If numerical or tabular data is present, format it clearly.
           7. Do not fabricate details; base your response only on the provided context.
           8. Ask clarifying questions if the query is ambiguous.

         Context:
          {context}

         Question:
          {question}

         Answer:
        """
            # Create a prompt template using LangChain's ChatPromptTemplate.
            self.prompt_template = ChatPromptTemplate.from_template(qa_template)
            # Build an LLMChain combining the chat model and the prompt template.
            self.chain = LLMChain(llm=self.chat_model, prompt=self.prompt_template)
            logger.info("LLMService initialized successfully.")
        except Exception as e:
            logger.error("Error initializing LLMService.")
            raise CustomException(str(e), sys)
    
    def get_response(self, question, context):
        """
        Generate a response from the LLM using the provided question and context.
        """
        try:
            # Prepare the inputs for the chain.
            inputs = {"question": question, "context": context}
            response = self.chain.run(inputs)
            return response.strip()
        except Exception as e:
            logger.error("Error generating response from LLMService.")
            raise CustomException(str(e), sys)

# Example usage for testing
if __name__ == "__main__":
    try:
        llm_service = LLMService()
        test_question = "How can I reset my password?"
        test_context = (
            "Subject: Password Reset\n"
            "Description: The user forgot their password.\n"
            "Resolution: Provide a password reset link."
        )
        answer = llm_service.get_response(test_question, test_context)
        print("LLM Response:\n", answer)
    except Exception as e:
        print(e)
