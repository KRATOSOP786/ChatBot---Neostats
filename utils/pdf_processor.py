from PyPDF2 import PdfReader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.config import CHUNK_SIZE, CHUNK_OVERLAP

def extract_text_from_pdf(pdf_file):
    """
    Extract text from uploaded PDF file
    
    Args:
        pdf_file: Streamlit uploaded file object
        
    Returns:
        str: Extracted text from PDF
    """
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        if not text.strip():
            return None
            
        print(f"✅ Extracted {len(text)} characters from PDF")
        return text
        
    except Exception as e:
        print(f"❌ Error extracting PDF text: {e}")
        return None

def split_text_into_chunks(text):
    """
    Split text into chunks for RAG
    
    Args:
        text (str): Full text to split
        
    Returns:
        list: List of text chunks
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        
        chunks = text_splitter.split_text(text)
        print(f"✅ Split text into {len(chunks)} chunks")
        return chunks
        
    except Exception as e:
        print(f"❌ Error splitting text: {e}")
        return []

def process_pdf(pdf_file):
    """
    Process PDF file: extract text and split into chunks
    
    Args:
        pdf_file: Streamlit uploaded file object
        
    Returns:
        list: List of text chunks or None if error
    """
    try:
        # Extract text
        text = extract_text_from_pdf(pdf_file)
        if not text:
            return None
        
        # Split into chunks
        chunks = split_text_into_chunks(text)
        if not chunks:
            return None
        
        return chunks
        
    except Exception as e:
        print(f"❌ Error processing PDF: {e}")
        return None