# app.py 

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage 
from file_handler import load_documents_from_files
from vector_store_handler import create_vector_store_from_documents, get_existing_retriever
from chain_handler import create_advanced_rag_chain

def main():
    st.set_page_config(page_title="(Pythrust RAG Assignment)", page_icon="📚", layout="wide")
    st.title(" Q & A prototype(Pythrust RAG ASSIGNMENT) ")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "retriever" not in st.session_state:
        st.session_state.retriever = None
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = None
        
    # --- Initial Load of Pre-Indexed Assignment Data ---
    if st.session_state.retriever is None:
        initial_retriever = get_existing_retriever()
        
        if initial_retriever:
            st.session_state.retriever = initial_retriever
            st.session_state.rag_chain = create_advanced_rag_chain(initial_retriever)
            st.info("Loaded pre-indexed assignment knowledge base. Ready to chat!")
        # No else block here, as the warning is handled later in the sidebar


    # --- Sidebar for Dynamic Uploads ---
    with st.sidebar:
        st.header("Controls & Dynamic Indexing")
        
        if st.session_state.retriever:
            st.success("Knowledge Base: ✅ Loaded & Ready")
        else:
            st.warning("Knowledge Base: ❌ Empty. Run 'python setup_db.py' or upload files below.")
            
        uploaded_files = st.file_uploader(
            "Upload NEW documents to ADD to the knowledge base", 
            type=["pdf", "txt"], 
            accept_multiple_files=True
        )
        
        if st.button("Add Documents to Index"):
            if uploaded_files:
                with st.spinner("Processing new documents..."):
                    loaded_docs = load_documents_from_files(uploaded_files)
                    
                    if loaded_docs:
                        # This function handles creation OR adding to the persistent store
                        updated_retriever = create_vector_store_from_documents(loaded_docs)
                        
                        st.session_state.retriever = updated_retriever
                        st.session_state.rag_chain = create_advanced_rag_chain(updated_retriever)
                        st.success("New documents processed and added successfully! Ready to chat.")
                        
                    else:
                        st.error("Could not load any content from the documents.")
            else:
                st.warning("Please upload at least one document to add.")

    # --- Main Chat Interface ---
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_question = st.chat_input("Ask a question about your documents...")
    
    if user_question:
        if st.session_state.rag_chain is None:
            st.error("The RAG pipeline is not initialized. Please run setup_db.py or upload files.")
        else:
            # 1. Add current user question to Streamlit history
            st.session_state.messages.append({"role": "user", "content": user_question})
            with st.chat_message("user"):
                st.markdown(user_question)

            with st.spinner("AI is thinking..."):
                # --- 💡 CHAT HISTORY 💡 ---
                converted_chat_history = []
                for msg in st.session_state.messages:
                    # Skip the current user message, as it is passed via "input"
                    if msg["content"] == user_question and msg["role"] == "user":
                        continue
                        
                    if msg["role"] == "user":
                        converted_chat_history.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "assistant":
                        # We save the cleaned up answer content to history, excluding source details
                        converted_chat_history.append(AIMessage(content=msg["content"]))
                        
               
                response = st.session_state.rag_chain.invoke({
                    "input": user_question,
                    "chat_history": converted_chat_history 
                })
                
                ai_response = response["answer"]
                
                # 3. Source Citation
                source_documents = response["context"]
                source_filenames = set([doc.metadata.get('source', 'Unknown Source') for doc in source_documents])
                sources_text = "Sources:\n" + "\n".join(f"- {filename}" for filename in source_filenames)

            # 4. Display and Save Response
            with st.chat_message("assistant"):
                st.markdown(ai_response)
                with st.expander("View Sources"):
                    st.info(sources_text)
            
            # Save the CLEAN answer content to history for future RAG calls
            st.session_state.messages.append({
                "role": "assistant", 
                "content": ai_response 
            })

if __name__ == "__main__":
    main()