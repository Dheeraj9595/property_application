import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rag.pdf_to_text import process_and_store_file  # Import your function

@csrf_exempt
def upload_document(request):
    """Handles file upload and processes it for ChromaDB storage"""
    if request.method == "POST" and request.FILES.get("document"):
        uploaded_file = request.FILES["document"]
        file_path = f"media/uploads/{uploaded_file.name}"

        # Save file temporarily
        path = default_storage.save(file_path, ContentFile(uploaded_file.read()))

        # Process and store in ChromaDB
        try:
            doc_id = os.path.basename(path)
            process_and_store_file(path, doc_id)
            return JsonResponse({"message": "File uploaded and stored successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "No file uploaded"}, status=400)

import json
from rag.vector_store import retrieve_documents


@csrf_exempt
def query_document(request):
    """Handles query in chromadb storage"""
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")
        query_response = retrieve_documents(query=user_message, top_k=3)
        return JsonResponse({"response": query_response})
    else:
        return render(request, 'query.html')
    
def upload_document_page(request):
    return render(request, 'upload.html')

def query_page(request):
    return render(request, 'query.html')

# @csrf_exempt
# def insert_data(request):
#     from rag.vector_store import data_insert_into_weaviate
#     data = json.loads(request.body)
#     content = data.get("content", "")
#     collection_name = data.get("collection_name", "")
#     result = data_insert_into_weaviate(text=content, id=collection_name)
#     breakpoint()
#     if result:
#         return JsonResponse({"response": f"Successfully Added text in collection {collection_name}"})
#     else:
#         return JsonResponse({"error": "There is some error"})


# @csrf_exempt
# def retrieve_data(request):
#     from rag.vector_store import retrieve_documents
#     data = json.loads(request.body)
#     collection_name = data.get("collection_name", "")
#     result = retrieve_documents(collection_name=collection_name)
#     if result:
#         return JsonResponse({"response": result})
#     else:
#         return JsonResponse({"error": "there is some error"})


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rag.vector_store import data_insert_into_weaviate, retrieve_documents, retrieve_documents_by_uuid

@csrf_exempt
def insert_data(request):
    """Handles inserting text data into a Weaviate collection."""
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

    try:
        data = json.loads(request.body)
        content = data.get("content")
        collection_name = data.get("collection_name")

        if not content or not collection_name:
            return JsonResponse({"error": "Missing 'content' or 'collection_name'"}, status=400)

        success = data_insert_into_weaviate(text=content, collection_name=collection_name)

        if success:
            return JsonResponse({"response": f"Successfully added text in collection '{collection_name}'"})
        else:
            return JsonResponse({"error": "Failed to insert data"}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)


@csrf_exempt
def retrieve_data(request):
    """Fetches stored text data from a Weaviate collection."""
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

    try:
        data = json.loads(request.body)
        collection_name = data.get("collection_name")

        if not collection_name:
            return JsonResponse({"error": "Missing 'collection_name'"}, status=400)

        result = retrieve_documents(collection_name=collection_name)
        result_dict = json.loads(result)  # Convert JSON string to Python dictionary

        return JsonResponse({"response": result_dict})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rag.vector_store import retrieve_documents_by_uuid  # Import your function

@csrf_exempt
def retrieve_data_by_id(request):
    """Fetches stored text data from a Weaviate collection by using UUID."""
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

    try:
        data = json.loads(request.body)
        collection_name = data.get("collection_name")
        document_uuid = data.get("uuid")  # Renamed `uuid` to `document_uuid` to avoid confusion

        if not collection_name:
            return JsonResponse({"error": "Missing 'collection_name'"}, status=400)
        if not document_uuid:
            return JsonResponse({"error": "Missing 'uuid'"}, status=400)

        # Call function to retrieve document
        return retrieve_documents_by_uuid(UUID=document_uuid, collection_name=collection_name)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
