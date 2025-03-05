from django.urls import include, path
from rest_framework.routers import DefaultRouter

import app1.views
from app1.views import (
    BookListCreate,
    BookRetrieveUpdateDestroy,
    UserViewSet,
    BookViewSet,
    CustomUsersView,
    StudentsViewSet, 
    create_book
)


router = DefaultRouter()

router.register(r"users", UserViewSet)
router.register(r"newbooks", BookViewSet)
router.register(r'CustomUser', CustomUsersView)
router.register(r'students', StudentsViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("books/", app1.views.create_book, name="book-list-create"),
    path("getbooks/", app1.views.get_books, name="book-list"),
    path("newbooks/", BookListCreate.as_view(), name="book-list-create"),
    path(
        "books/<int:pk>/",
        BookRetrieveUpdateDestroy.as_view(),
        name="book-retrieve-update-destroy",
    ),
    # path('add-book/', create_book, name='add_book'),
    path("create-book/", create_book, name="create_book"),
]
