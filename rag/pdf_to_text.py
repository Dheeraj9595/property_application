from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS  # or Chroma, Pinecone, Weaviate, etc.
from pypdf import PdfReader
from docx import Document
from rag.vector_store import *  # Ensure this has `add_document` & `add_large_document`
import pytesseract
from pdf2image import convert_from_path



def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file"""
    reader = PdfReader(pdf_path)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file"""
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


def extract_image_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = "\n".join([pytesseract.image_to_string(img) for img in images])
    return text

def process_and_store_file(file_path, doc_id):
    """Extract, process, and store a file in ChromaDB with chunking"""
    if file_path.endswith(".pdf"):
        text = extract_image_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format") 

    # Use add_large_document to ensure chunking before storing
    add_large_document(text, doc_id)  
    print(f"Document {doc_id} stored successfully!")
