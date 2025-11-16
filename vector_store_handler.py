# vector_store_handler.py 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def create_vector_store_from_documents(documents: list[Document]):
    """
    Creates a ChromaDB vector store from a list of documents, handling empty inputs.
    """
    if not documents:
        print("Error: No documents provided to create the vector store. Aborting.")
        return None
        
    print("Starting the vector store creation process...")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunked_docs = text_splitter.split_documents(documents)

    # --- ADDED VALIDATION ---
    if not chunked_docs:
        print("Error: Document chunking resulted in zero chunks. Aborting.")
        return None

    print(f"Split {len(documents)} documents into {len(chunked_docs)} chunks.")

    embedding_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    vector_db = Chroma.from_documents(
        documents=chunked_docs,
        embedding=embedding_model,
        persist_directory="./chroma_db_prod"
    )
    print(f"Vector store created successfully in './chroma_db_prod'.")
    
    return vector_db.as_retriever()

def get_existing_retriever(persist_directory: str = "./chroma_db_prod"):
    """
    Loads an existing ChromaDB vector store from disk and returns a retriever.
    
    It is crucial to provide the same embedding function used during creation
    to embed the query correctly during retrieval.
    """
    # 1. The embedding model
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    # 2. Check if the persistence directory exists first
    if not os.path.isdir(persist_directory):
        print(f"Warning: Persistent directory '{persist_directory}' not found. Run 'python setup_db.py' first.")
        return None

    try:
        # 3. Load the Chroma DB 
        vector_db = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding_model,
        )
        
        # 4. Check if the collection has any items (optional, but robust)
        # Note: Accessing the count is a way to verify content is loaded.
        if vector_db._collection.count() > 0:
            print(f"Loaded existing vector store with {vector_db._collection.count()} chunks.")
            return vector_db.as_retriever()
        else:
            print("Warning: Existing vector store found, but it is empty.")
            return None
            
    except Exception as e:
        print(f"Error loading vector store from disk: {e}")
        return None