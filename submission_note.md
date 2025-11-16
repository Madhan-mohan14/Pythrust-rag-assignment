RAG Pipeline Design and Analysis

The project delivers a modular, dual-mode Retrieval-Augmented Generation (RAG) pipeline built on LangChain. My approach focused on demonstrating robust code architecture and advanced conversational capabilities to fulfill the Generative AI Engineer Intern role requirements efficiently.

Approach
The design implements separated workflows for data ingestion. The Pre-Indexing mode utilizes setup_db.py to automatically ingest the 10–20 assignment documents from the /data folder into a persistent ChromaDB, ensuring immediate, hands-on testing for the evaluator. The application retains a Dynamic Upload mode via file_handler.py for real-time document additions.

To ensure excellent follow-up question support, the core of the system is the history-aware retriever chain. This LCEL construct contextualizes the user's latest query using the chat history, generating a precise standalone search query for the vector store, which significantly enhances conversational accuracy.

Performance was prioritized through LLM selection: Llama-3.1-8b-instant via Groq's API. This choice ensures fast, low-latency generation, providing a superior user experience in the Streamlit interface.

Trade-offs and Design Decisions 
A key trade-off involved LLM dependency, requiring separate GROQ_API_KEY (for generation) and GOOGLE_API_KEY (for embeddings). This decision was made to leverage best-in-class components for speed and quality over API consolidation. While standard RecursiveCharacterTextSplitter was used for simplicity, it offers a strong baseline for future retrieval improvements.

Future Enhancements 
Future work should focus on robustness, generalizability, and observability to prepare the pipeline for production:

Hallucination Prevention and Groundedness: Implement an evaluation framework (like Ragas) to calculate Faithfulness and Context Adherence scores after every response, providing automated detection of ungrounded answers. The system's prompt should be refined to explicitly state when an answer cannot be found in the provided context.

Advanced Observability and Tracking: Integrate structured logging for every query, capturing the query timestamp, retrieved documents, and LLM usage metadata (e.g., input/output tokens). Utilizing a platform like LangSmith would enable full traceability of the RAG chain for deep debugging.


Multimodal Data Ingestion: Expand data ingestion beyond TXT and PDF to handle complex sources, including .docx and .csv, and utilize specialized loaders for external content like Web URLs and YouTube video transcripts. Crucially, the system could evolve into a Multimodal RAG by integrating visual processing to ingest image data and answer queries based on both visual and textual content.
