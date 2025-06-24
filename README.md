# 📚 Multi‑PDF Q&A Assistant

A Streamlit app that allows you to ask questions about one or more uploaded PDFs using **Google Gemini** and **LangChain** (RAG). The app processes PDFs, creates embeddings, and retrieves relevant information to answer questions.

---

## ⚡️ Features
- ✅ Upload multiple PDFs
- ✅ Extract text from PDFs
- ✅ Create embeddings using **Google Gemini**
- ✅ Retrieve relevant context via **FAISS**
- ✅ Chat-style Q&A interface
- ✅ Displays sources for transparency
- ✅ Works with **Streamlit Community Cloud**

---

## 🛠️ Tech Stack
- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [langchain-google-genai](https://pypi.org/project/langchain-google-genai/)
- [langchain-community](https://pypi.org/project/langchain-community/)
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- [faiss-cpu](https://pypi.org/project/faiss-cpu/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [google-generativeai](https://pypi.org/project/google-generativeai/)

---

## ⚡️ Demo Screenshot
![image](https://github.com/user-attachments/assets/f83379a2-1157-476b-9484-8ece31995411)
---

## 📋 Getting Started

### ✅ 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 🔑 2️⃣ Set Up API Key
Get API key from google gemini
```bash
GOOGLE_API_KEY = "your_real_gemini_api_key_here"
```
### 🚀 3️⃣ Run Locally
```bash
streamlit run app.py
```
## ⚡️ Usage
1. Upload one or more PDFs.
2. Click **Process Documents**.
3. Enter questions related to the files.
4. Receive answers sourced from the PDFs.

