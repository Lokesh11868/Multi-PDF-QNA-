import streamlit as st
import os
from dotenv import load_dotenv
import PyPDF2
import tempfile
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain.chains.retrieval_qa.base import RetrievalQA

# Load environment
load_dotenv()

# Page config
st.set_page_config(page_title="PDF Q&A", page_icon="📚", layout="wide")

# Simple CSS
st.markdown("""
<style>
.main-header {background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
              color: white; padding: 1rem; border-radius: 10px; text-align: center;}
.chat-box {background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0;}
.source-box {background: #000; color: #fff; padding: 0.5rem; border-radius: 5px; margin: 0.5rem 0;}
</style>
""", unsafe_allow_html=True)

def extract_pdf_text(pdf_file):
    """Extract text from PDF"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text and page_text.strip():
                text += f"\n[Page {page_num + 1}] {page_text}"
        return text
    except Exception:
        return ""

def setup_rag(documents):
    """Setup RAG system using Groq"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("Please set GROQ_API_KEY in .env file.")
        return None

    # Create documents
    docs = []
    for filename, content in documents.items():
        chunks = [content[i:i + 1000] for i in range(0, len(content), 800)]
        for i, chunk in enumerate(chunks):
            if chunk.strip():
                docs.append(Document(
                    page_content=chunk,
                    metadata={"source": filename, "chunk": i}
                ))

    if not docs:
        return None

    # Use local HuggingFace embeddings (no API limits)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.from_documents(docs, embeddings)

    # LLM setup with Groq
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=api_key,
        temperature=0.3
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    return qa_chain

def main():
    """Main Streamlit app"""
    if 'documents' not in st.session_state:
        st.session_state.documents = {}
    if 'qa_chain' not in st.session_state:
        st.session_state.qa_chain = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Header
    st.markdown('<div class="main-header"><h1>📚 Multi-PDF Q&A Assistant</h1><p style="margin:0;">Powered by Groq + Llama 3.3</p></div>', 
                unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("📁 Upload PDFs")
        uploaded_files = st.file_uploader(
            "Choose PDF files",
            type="pdf",
            accept_multiple_files=True
        )
        if uploaded_files:
            if st.button("Process Documents"):
                with st.spinner("Processing..."):
                    documents = {file.name: extract_pdf_text(file) for file in uploaded_files if extract_pdf_text(file)}
                    if documents:
                        st.session_state.documents = documents
                        st.session_state.qa_chain = setup_rag(documents)
                        st.success(f"✅ Processed {len(documents)} documents.")
                        st.rerun()
        if st.session_state.documents:
            st.subheader("📋 Loaded Files")
            for filename in st.session_state.documents.keys():
                st.write(f"📄 {filename}")

    # Main Chat Area
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header("💬 Ask Questions")
        if not st.session_state.qa_chain:
            st.info("👆 Upload and process PDF files to ask questions.")
        else:
            question = st.text_input("Your question:", key="question")
            if st.button("Ask") and question:
                with st.spinner("Getting answer..."):
                    try:
                        result = st.session_state.qa_chain.invoke({"query": question})
                        st.session_state.chat_history.append({
                            "question": question,
                            "answer": result["result"],
                            "sources": [doc.metadata["source"] for doc in result["source_documents"]],
                        })
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

        # Show chat history
        for chat in reversed(st.session_state.chat_history):
            st.markdown('</div>', unsafe_allow_html=True)
            st.write(f"**Q:** {chat['question']}")
            st.write(f"**A:** {chat['answer']}")
            if chat["sources"]:
                sources = list(set(chat["sources"]))
                st.markdown(f'<div class="source-box">📚 Sources: {", ".join(sources)}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown('<hr class="divider-line">', unsafe_allow_html=True)

    # Stats
    with col2:
        st.header("📊 Stats")
        st.metric("Documents", len(st.session_state.documents))
        st.metric("Questions", len(st.session_state.chat_history))
        if st.button("Clear History"):
            st.session_state.chat_history = []
            st.rerun()

if __name__ == "__main__":
    main()
