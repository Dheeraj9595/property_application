import chromadb
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load sentence transformer model for embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="knowledge_base")

def chunk_text(text, chunk_size=500, overlap=50):
    """Splits text into smaller chunks for better retrieval"""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    chunks = text_splitter.split_text(text)
    return chunks

def add_document(text, doc_id):
    """Add a document to the vector database"""
    embedding = model.encode(text).tolist()
    collection.add(ids=[doc_id], embeddings=[embedding], documents=[text])

def add_large_document(text, doc_id_prefix):
    """Handles large documents by chunking them before adding"""
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        chunk_id = f"{doc_id_prefix}_{i}"  # Unique ID for each chunk
        add_document(chunk, chunk_id)

    print(f"Added {len(chunks)} chunks for document {doc_id_prefix} successfully!")

def retrieve_documents(query, top_k=3):
    """Retrieve top-k relevant documents"""
    query_embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results["documents"][0] if results else []

def update_documents(doc_id, new_text):
    """Update an existing document in the vector database"""
    #Delete the old document
    collection.delete(ids=[doc_id])
    
    #Add the update document
    add_document(new_text, doc_id)
    print(f"Document {doc_id} update successfully!")

    