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

def upload_document_page(request):
    return render(request, 'upload.html')