import os
import streamlit as st

def check_environment():
    """Check if environment is properly set up"""
    required_packages = [
        'streamlit', 'langchain', 'langchain_google_genai', 
        'PyPDF2', 'faiss', 'python_dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        st.error(f"Missing packages: {', '.join(missing_packages)}")
        st.info("Run: pip install -r requirements.txt")
        return False
    
    # Check API key
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("GOOGLE_API_KEY not found in environment variables")
        st.info("Please set your Google Gemini API key in .env file")
        return False
    
    return True

if __name__ == "__main__":
    if check_environment():
        st.success("✅ Environment setup complete!")
    else:
        st.error("❌ Environment setup incomplete!")
