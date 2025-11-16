#  Q & A prototype

**Live Demo:** [https://multi-doc-pro.streamlit.app/](https://multi-doc-pro.streamlit.app/)

## 💡Overview:

This project is a **Retrieval-Augmented Generation (RAG)** system that allows users to query information from a **custom document knowledge base**. It uses **LangChain**, **Chroma Vector Database**, **Google or OpenAI embeddings**, and a **Streamlit UI**.

The solution supports **two types of workflows**, demonstrating modularity and real-world flexibility:

1️⃣ **Pre-Indexed Dataset Mode (Recommended):**  
   Uses pre-indexed `.txt` files stored in the `/data` folder.  
   This mode loads instantly without requiring file upload.

2️⃣ **User-Uploaded Document Mode:**  
   Allows the user to upload PDF or TXT files dynamically and re-index.

---

## 📁 Project Structure

| File / Folder | Description |
|--------------|-------------|
| `app.py` | Main Streamlit chat interface |
| `file_handler.py` | Loads and validates PDF/TXT files |
| `vector_store_handler.py` | Handles embeddings + Chroma vector storage |
| `chain_handler.py` | History-aware retrieval chain using LangChain LCEL |
| `setup_db.py` | One-time script to build persistent Chroma DB |
| `data/` | Folder containing 10–20 `.txt` sample docs |
| `submission_note.md` | Design, reasoning, trade-offs, and testing steps |
| `requirements.txt` | Project dependencies |
|`data_loader.py` |	Loads documents directly from the /data directory (used by setup_db.py)|

---

## 🛠️ Technical Architecture

The application is built on a modular architecture using the core principles of an AI Agent pipeline:

1.  **File Loading (`file_handler.py`):** Takes multiple PDFs and TXT files, loads them into LangChain `Document` objects, and cleans/validates them.
2.  **Indexing (`vector_store_handler.py`):** Uses **RecursiveCharacterTextSplitter** and **GoogleGenerativeAIEmbeddings** to index data into a persistent **ChromaDB**.
3.  **Indexing Setup (setup_db.py): Utilizes (`data_loader.py`) to ingest the documents from the /data folder, chunks them, and performs the initial indexing to create the persistent ChromaDB directory.**
4.  **The Conversational Chain (`chain_handler.py`):** An advanced LangChain Expression Language (LCEL) chain manages contextualization, retrieval, and final generation using Groq's fast LLM.
5.  **Interface (`app.py`):** Streamlit manages the user experience, file uploads, conversation history, and displays the final output with sources.

## 💻 Getting Started (Local Development

### 🛠️ Requirements

* Python 3.10+
* A `GROQ_API_KEY` (for fast inference)
* A `GOOGLE_API_KEY` (for embeddings)

### Setup

1.  **Clone the repository & install dependencies:**
    ```bash
    git clone [https://github.com/Madhan-mohan14/Pythrust-rag-assignment.git](https://github.com/Madhan-mohan14/Pythrust-rag-assignment.git)
    cd Pythrust-rag-assignment
    pip install -r requirements.txt 
    ```
2.  **Set Environment Variables:** Create a `.env` file in the root directory:
    ```
    GROQ_API_KEY="YOUR_GROQ_KEY"
    GOOGLE_API_KEY="YOUR_GOOGLE_KEY"
    ```
3.  **Run the App:**
4.  first you have to run the setup_db.py to load the documents which we have and pre index them 
    ```bash
     python setup_db.py
    streamlit run app.py
    ```

---
## Evaluation Notes

No need to upload documents if pre-indexed DB exists

Upload mode is still available for flexibility

Codebase is modular and extendable

Embeddings + model selection are environment driven

No private or paid datasets used

##🚧 Future Enhancements
Support .docx and website URLs like (youtube video)

Add prompt-template selector
using tokenization and fast answers 
Integrate evaluation metrics (faithfulness + citation grounding)
