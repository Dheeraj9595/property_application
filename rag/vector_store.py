import weaviate
from weaviate.classes.config import Property, DataType
from sentence_transformers import SentenceTransformer
import json
from django.http import JsonResponse
from weaviate.exceptions import WeaviateBaseError  
from functools import wraps  # To define the decorator

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

#Reusable Weaviate Client Wrapper
class WeaviateClient:
    def __init__(self, host="127.0.0.1", port=8080, grpc_port=50051):
        self.client = weaviate.connect_to_local(host=host, port=port, grpc_port=grpc_port)

    def __enter__(self):
        self.client.connect()
        return self.client

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()  # Ensure the client is closed

#Create a Decorator to Use the Weaviate Client
def with_weaviate_client(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with WeaviateClient() as client:
            return func(client, *args, **kwargs)  # Pass the client to the function
    return wrapper

#Ensure Weaviate is ready
with WeaviateClient() as client:
    if not client.is_ready():
        raise Exception("Weaviate is not ready!")
    else:
        print("Weaviate is ready")


def add_document(text, doc_id):
    """Store document with embedding in Weaviate"""
    embedding = model.encode(text).tolist()  # Convert text to embedding
    collection = client.collections.get(doc_id)
    collection.data.insert(
        {
            "content": text,
            "doc_id": doc_id,
        },
        "Document",
        vector=embedding  # Store embedding in Weaviate
    )

    
@with_weaviate_client
def data_insert_into_weaviate(client, text, collection_name):
    # Compute embedding for the text
    vector = model.encode(text).tolist()

    # Check if the collection exists
    if collection_name not in [col for col in client.collections.list_all()]:
        # Create collection with a vector index
        client.collections.create(
            name=collection_name,
            properties=[
                Property(name="content", data_type=DataType.TEXT),
            ],
            vectorizer_config=None,  # Disable Weaviate's built-in vectorizer
        )

    # Insert data with embedding
    collection = client.collections.get(collection_name)
    collection.data.insert(
        {"content": text},
        vector=vector  # Store the computed embedding
    )
    
    print(f"Data inserted into collection: {collection_name} successfully")

    return JsonResponse({"message": f"Your data is inserted into Collection: {collection_name} with embeddings"})

# Function to Retrieve Data
@with_weaviate_client
def retrieve_documents(client, collection_name):
    if collection_name not in [col for col in client.collections.list_all()]:
        return JsonResponse({"error": "Collection does not exist"}, status=404)

    collection = client.collections.get(collection_name)
    response = collection.query.fetch_objects()
    result = {"documents": [obj.properties["content"] for obj in response.objects]}
    client.close()
    return json.dumps(result, indent=2)

import json
from django.http import JsonResponse
from weaviate.exceptions import WeaviateBaseError  # Handle potential errors

# Function to Retrieve Data by UUID
@with_weaviate_client
def retrieve_documents_by_uuid(client, UUID, collection_name):
    try:
        collection = client.collections.get(collection_name)
        response = collection.query.fetch_object_by_id(UUID)

        if response:
            result = response.properties  # Extract properties dictionary
        else:
            result = None

        return JsonResponse({"result": result}, status=200 if result else 404)

    except WeaviateBaseError as e:
        return JsonResponse({"error": f"Weaviate error: {str(e)}"}, status=500)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
