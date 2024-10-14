import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader


def load_environment_variables():
    """Load environment variables from .env file."""
    load_dotenv()

def get_knowledge(filename):
    """Read knowledge from a file."""
    with open(filename, "r") as f:
        text = f.read()
    return text

def split_text_into_chunks(text):
    """Split text into manageable chunks."""
    text_splitter = CharacterTextSplitter(chunk_size=1000, separator='\n', chunk_overlap=100, length_function=len)
    return text_splitter.split_text(text)

def create_vector_store(chunks, persist_dir):
    """Create or load vector store."""
    if not os.path.exists(persist_dir):
        print('Vector store does not exist. Initializing vector store...')
        documents = [Document(page_content=chunk) for chunk in chunks]
        print(f'Document chunks: {len(documents)}')
        embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001')
        db = Chroma.from_documents(documents, embeddings, persist_directory=persist_dir)
        print('Finished creating vector store.')
    else:
        print('Vector store already exists.')

def main():
    # Load environment variables
    load_environment_variables()
    
    # Paths and files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    knowledge_base = os.path.join(current_dir, 'knowledge.txt')
    persist_dir = os.path.join(current_dir, 'chroma_db')
    
    # Get knowledge text from file
    knowledge_text = get_knowledge(knowledge_base)
    
    # Split text into chunks
    chunks = split_text_into_chunks(knowledge_text)
    
    # Create or load vector store
    create_vector_store(chunks, persist_dir)

if __name__ == '__main__':
    main()



