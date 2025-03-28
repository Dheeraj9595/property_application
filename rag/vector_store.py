import weaviate
from weaviate.classes.config import Property, DataType
from sentence_transformers import SentenceTransformer
import json

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to Weaviate
client = weaviate.connect_to_local(
    host="127.0.0.1",
    port=8080,
    grpc_port=50051,

)

# Ensure Weaviate is ready
if not client.is_ready():
    raise Exception("Weaviate is not ready!")

# Function to create a collection (if not exists) and insert data
def data_insert_into_weaviate(text, collection_name):
    client.connect()
    if collection_name not in [col for col in client.collections.list_all()]:
        # Create collection if it doesn't exist
        client.collections.create(
            name=collection_name,
            properties=[Property(name="content", data_type=DataType.TEXT)],
        )
    
    # Insert Data
    collection = client.collections.get(collection_name)
    collection.data.insert({"content": text})
    print(f"Data inserted into collection: {collection_name} successfully")
    client.close()
    return JsonResponse({"message": f"Your data is inserted into Collection: {collection_name}"})

# Function to retrieve data from Weaviate
def retrieve_documents(collection_name):
    client.connect()
    if collection_name not in [col for col in client.collections.list_all()]:
        return json.dumps({"error": "Collection does not exist"})

    collection = client.collections.get(collection_name)
    response = collection.query.fetch_objects()

    # Convert the result into a dictionary
    result = {"documents": [obj.properties["content"] for obj in response.objects]}
    client.close()
    return json.dumps(result, indent=2)

import json
from django.http import JsonResponse
from weaviate.exceptions import WeaviateBaseError  # Handle potential errors

def retrieve_documents_by_uuid(UUID, collection_name):
    try:
        client.connect()
        collection = client.collections.get(collection_name)
        response = collection.query.fetch_object_by_id(UUID)

        # Extract properties from the response
        if response:
            result = response.properties  # Extract properties dictionary
        else:
            result = None

        client.close()
        return JsonResponse({"result": result}, status=200 if result else 404)

    except WeaviateBaseError as e:
        return JsonResponse({"error": f"Weaviate error: {str(e)}"}, status=500)

    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

