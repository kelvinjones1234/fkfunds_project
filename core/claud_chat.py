import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from anthropic import Anthropic


def load_environment_variables():
    """Load environment variables from .env file."""
    load_dotenv()

def query_and_respond(persist_dir, query):
    # Initialize embeddings and vector store
    embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001')
    db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    # Retrieve relevant documents
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={'k': 3}  # Retrieve top 5 most relevant documents
    )
    relevant_docs = retriever.invoke(query)
    # print(f"Reference: {' '.join(doc.page_content for doc in relevant_docs)}")

    # Prepare input for the model
    combined_input = (
        f"Answer as the school consultant of the Federal Polytechnic Bida: {query}\n\n"
        f"Reference: {' '.join([doc.page_content for doc in relevant_docs])}\n\n"
        "Provide a brief, professional response that:"
        "- Helps students, parents, or staff"
        "- Is empathetic, clear, and follows best practices"
        "- shows respect and confidence"
        "- Sounds natural"
        "- Focuses on the query without extra info"
        "- Clarifies when giving general vs. specific advice"
    )
    ANTHROPIC_API_KEY = "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"
    client = Anthropic(
                api_key=ANTHROPIC_API_KEY
            )  # Replace with your actual API key
    try:
        response = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=400,
                    messages=[
                {"role": "user", "content": f"{combined_input}"},
        
            ],
                )
        if response:
            print('Response recieved from anthropic...')
            return response.content[0].text
        else:
          return "I apologize, but I couldn't generate a response at this time. Please try again later or contact the school office for assistance."
    except Exception as e:
        return f"I'm sorry, but an error occurred while processing your request: {str(e)}. Please try again or contact the school's IT support if the problem persists."
    
