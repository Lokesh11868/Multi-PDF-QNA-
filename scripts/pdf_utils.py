import PyPDF2
from typing import List, Dict, Any
import re

def clean_text(text: str) -> str:
    """Clean extracted text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?;:()\-"]', '', text)
    return text.strip()

def extract_text_from_pdf(pdf_path: str, filename: str) -> Dict[str, Any]:
    """Extract text from a single PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            chunks = []
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                if text.strip():  # Only add non-empty pages
                    cleaned_text = clean_text(text)
                    if len(cleaned_text) > 50:  # Only add substantial content
                        # Split long pages into smaller chunks
                        if len(cleaned_text) > 1000:
                            # Split into smaller chunks
                            chunk_size = 1000
                            overlap = 200
                            for i in range(0, len(cleaned_text), chunk_size - overlap):
                                chunk_text = cleaned_text[i:i + chunk_size]
                                if len(chunk_text.strip()) > 50:
                                    chunks.append({
                                        'content': chunk_text,
                                        'page': page_num,
                                        'chunk_id': f"{page_num}_{i//chunk_size}"
                                    })
                        else:
                            chunks.append({
                                'content': cleaned_text,
                                'page': page_num,
                                'chunk_id': str(page_num)
                            })
            
            return {
                'filename': filename,
                'chunks': chunks,
                'total_pages': len(pdf_reader.pages)
            }
    
    except Exception as e:
        raise Exception(f"Error processing {filename}: {str(e)}")

def extract_text_from_pdfs(pdf_paths: List[str], filenames: List[str]) -> List[Dict[str, Any]]:
    """Extract text from multiple PDF files"""
    documents = []
    
    for pdf_path, filename in zip(pdf_paths, filenames):
        try:
            doc = extract_text_from_pdf(pdf_path, filename)
            if doc['chunks']:  # Only add documents with content
                documents.append(doc)
        except Exception as e:
            print(f"Warning: Could not process {filename}: {str(e)}")
            continue
    
    return documents
