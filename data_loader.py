# data_loader.py 

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
from typing import List
import os

def load_documents_from_directory(directory_path: str = "data") -> List[Document]:
    """
    Loads text documents (TXT files) from a specified directory.
    
    Args:
        directory_path (str): The path to the folder containing source documents.

    Returns:
        List[Document]: A list of LangChain Document objects.
    """
    print(f"Loading documents from directory: {directory_path}...")
    
    # Using DirectoryLoader to find and load all .txt files
    # Note: You can expand 'glob' to include other types if needed (e.g., "**/*.*")
    try:
        loader = DirectoryLoader(
            path=directory_path,
            glob="**/*.txt", 
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8", "autodetect_encoding": True} # Added autodetect for robustness
        )
        
        documents = loader.load()
        
        # Filter out any empty documents
        non_empty_docs = [doc for doc in documents if doc.page_content.strip()]

        if not non_empty_docs:
            print("Warning: Directory loading resulted in zero non-empty documents.")
            
        print(f"Successfully loaded {len(non_empty_docs)} documents.")
        return non_empty_docs

    except Exception as e:
        print(f"Error loading documents from directory {directory_path}: {e}")
        return []