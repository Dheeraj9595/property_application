from django.urls import path
import rag.views as rag_views

urlpatterns = [
    path("upload-document/", rag_views.upload_document, name="upload_document"),
    path("upload-document-page/", rag_views.upload_document_page, name="upload_document_page"),
    path("query-page/", rag_views.query_document, name='query-document'),
    path("insert-data/", rag_views.insert_data, name="insert data"),
    path("retrieve-data/", rag_views.retrieve_data, name="retrieve data"),
    path("retrieve-data-uuid/", rag_views.retrieve_data_by_id, name="retrieve_data_by_id"),

]
