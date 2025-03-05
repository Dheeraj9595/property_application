import json


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Book, CustomUser, Student
from .serializers import BookSerializer, UserSerializer, CustomUserSerializer, StudentSerializer
from django.contrib.auth import get_user_model


User = get_user_model()







@api_view(["GET"])
@csrf_exempt  # This exempts the view from CSRF checks (for testing purposes)
def get_books(request):
    # Get all books from the database
    books = Book.objects.all()

    # Serialize the list of books
    serializer = BookSerializer(books, many=True)

    # Return the serialized data
    return Response(serializer.data)


@csrf_exempt
def create_book(request):
    if request.method == "POST":
        try:
            # Manually parse the JSON data from request.body
            data = json.loads(request.body)

            title = data.get("title")
            author = data.get("author")
            publication_date = data.get("publication_date")

            # Assuming you've validated the data and created a new Book
            book = Book.objects.create(
                title=title, author=author, publication_date=publication_date
            )

            return JsonResponse({"id": book.id, "title": book.title}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)


class BookListCreate(generics.ListCreateAPIView):
    queryset = (
        Book.objects.all()
    )  # Define the queryset for the list view and create view
    serializer_class = BookSerializer  # Specify the serializer to use


class BookRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = (
        Book.objects.all()
    )  # Define the queryset for retrieve, update, and destroy views
    serializer_class = BookSerializer  # Specify the serializer to use


class Usercreate(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomUsersView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer    

class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

from django.shortcuts import render, redirect
from .models import Book
from app1.forms import BookForm


def create_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return JsonResponse({"message": "Successfully Created Book", "book_id": book.id}, status=201)
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    form = BookForm()
    return render(request, "book_form.html", {"form": form})
