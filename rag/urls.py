from django.urls import path
import rag.views as rag_views

urlpatterns = [
    path("upload-document/", rag_views.upload_document, name="upload_document"),
    path("upload-document-page/", rag_views.upload_document_page, name="upload_document_page"),
    path("query-page/", rag_views.query_document, name='query-document'),
]
