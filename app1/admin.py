from django.contrib import admin

from app1.models import Book, Student

# Register your models here.
admin.site.register([Book, Student])
