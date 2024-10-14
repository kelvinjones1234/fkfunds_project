import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
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
        search_kwargs={'k': 3}  # Retrieve top 3 most relevant documents
    )
    relevant_docs = retriever.invoke(query)

    # Print relevant documents
    print('--------------------Relevant Documents-----------------')
    for i, doc in enumerate(relevant_docs, 1):
        print(f'Document {i}:\n\nContent: {doc.page_content}\n')
        if hasattr(doc, 'metadata') and 'score' in doc.metadata:
            print(f'Score: {doc.metadata["score"]}\n')
        print('---\n')

    # Prepare input for the model
    combined_input = (
        f"Here are some documents that can answer your question: {query}\n\n"
        f"Relevant Documents:\n"
        f"{' '.join([doc.page_content for doc in relevant_docs])}\n\n"
        "Please provide an answer based only on the provided documents. "
        "If the answer is not in the documents, respond with 'This information is not available.'"
        "Please ensure all responses are strictly in English language"
    )

    # Generate response using the g4f client
    client = Client()
    try:
        print("Sending request to g4f client...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": combined_input}
            ],
        )
        print("Received response from g4f client.")
        
        if response and response.choices:
            print("Model's response:")
            print(response.choices[0].message.content)
        else:
            print("No response content received from the model.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    # Load environment variables
    load_environment_variables()

    # Set up paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    persist_dir = os.path.join(current_dir, 'chroma_db')

    # Example query
    query = 'what are the post application process for the fed poly bida?'
    query_and_respond(persist_dir, query)

if __name__ == '__main__':
    main()



import streamlit as st

# Initialize session state for conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Sidebar
st.sidebar.title("Consultation System")

# Main Section
st.title("Welcome to the Federal Polytechnic Consultation System")

st.subheader("Frequently Asked Questions:")
st.write("""
    1. What is the cut-off mark for admission?
    2. How do I apply for admission?
    3. What documents are required for admission?
    """)

# Display conversation history
st.subheader("Conversations:")
for item in st.session_state.conversation:
    st.write(f"Q: {item['question']}")
    st.write(f"A: {item['answer']}")
    st.write("---")

# Adding space above the input field
st.markdown("<br>", unsafe_allow_html=True)

# Input field and submit button


question = st.chat_input("Type your question here")

# Handling the submit action
if question:
    # Placeholder for response logic
    response = "This is where the system will provide guidance."
    
    # Add to conversation history
    st.session_state.conversation.append({
        "question": question,
        "answer": response
    })
    
    # Clear the input field by rerunning the app
    st.rerun()
