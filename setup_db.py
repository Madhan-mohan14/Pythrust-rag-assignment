# setup_db.py 

import os
from dotenv import load_dotenv
from data_loader import load_documents_from_directory
from vector_store_handler import create_vector_store_from_documents

# Load environment variables (like API keys)
load_dotenv()

def setup_database():
    """
    Loads documents from the 'data/' folder and creates the persistent ChromaDB.
    """
    print("--- Starting RAG Database Setup (Pythrust Assignment) ---")
    
    # 1. Load documents from the 'data/' folder
    documents = load_documents_from_directory(directory_path="data")
    
    if documents:
        # 2. Create the vector store (which persists/saves it to disk)
        create_vector_store_from_documents(documents)
        print("\n--- Database setup COMPLETE. Ready to run 'streamlit run app.py' ---")
    else:
        print("\n!!! ERROR: No documents found or loaded. Please check your 'data/' folder and document contents.")

if __name__ == "__main__":
    if not os.getenv("GOOGLE_API_KEY"):
        print("ERROR: GOOGLE_API_KEY is not set. Please set it in your .env file or environment.")
    else:
        setup_database()