import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from g4f.client import Client

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
        search_kwargs={'k': 5}  # Retrieve top 5 most relevant documents
    )
    relevant_docs = retriever.invoke(query)
    # Prepare input for the model
    combined_input = (
        f"As a school consultant of the Federal Polytechnic Bida, answer this question: {query}\n\n"
        f"Relevant documents:\n{' '.join([doc.page_content for doc in relevant_docs])}\n\n"
        "Provide a concise, professional answer based on these documents. "
        "Be helpful and informative for students, parents, or staff. "
        "If information is lacking, suggest speaking with a school administrator. "
        "Be empathetic, clear, and align with educational practices. "
        "Maintain confidentiality for sensitive topics. "
        "Sound as human as possible. "
        "Focus solely on answering the question without unnecessary information."
        "Ensure your response(s) are provided strictly in English language"
    )
    # Generate response using the g4f client
    client = Client()
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable and professional school consultant, dedicated to providing accurate and helpful information to the school community."},
                {"role": "user", "content": combined_input}
            ],
        )
        if response and response.choices:
            return response.choices[0].message.content
        elif response.choices[0].message.content == "":
            return "As the online consultant of the Federal Polytechnic Bida, Niger State, I regret to bring to you that we are currently out of service, just try again in a sec."
        else:
          return "I apologize, but I couldn't generate a response at this time. Please try again later or contact the school office for assistance."
    except Exception as e:
        return f"I'm sorry, but an error occurred while processing your request: {str(e)}. Please try again or contact the school's IT support if the problem persists."
    
