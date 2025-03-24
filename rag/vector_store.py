import chromadb
from sentence_transformers import SentenceTransformer

# Load sentence transformer model for embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="knowledge_base")

def add_document(text, doc_id):
    """Add a document to the vector database"""
    embedding = model.encode(text).tolist()
    collection.add(ids=[doc_id], embeddings=[embedding], documents=[text])

def retrieve_documents(query, top_k=3):
    """Retrieve top-k relevant documents"""
    query_embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results["documents"][0] if results else []
