import json


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Book, CustomUser, Student
from .serializers import BookSerializer, UserSerializer, CustomUserSerializer, StudentSerializer
from django.contrib.auth import get_user_model

