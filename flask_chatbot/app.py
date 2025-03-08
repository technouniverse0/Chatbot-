import sys
import os

# Add the project root directory to sys.path so that services and other modules are discoverable.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, render_template, request
from services.rag_pipeline import RAGPipeline
from services.llm_service import LLMService

app = Flask(__name__)

# Initialize the RAG pipeline and LLM service once at startup
rag_pipeline = RAGPipeline()
llm_service = LLMService()

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    user_query = None
    if request.method == "POST":
        user_query = request.form.get("query")
        if user_query:
            # Retrieve relevant context from your documents
            context = rag_pipeline.retrieve_context(user_query)
            # Generate a response using your LLM service
            response = llm_service.get_response(user_query, context)
    return render_template("chat.html", query=user_query, response=response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
