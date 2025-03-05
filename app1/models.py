from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
import uuid


User = get_user_model()

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)


    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey('app1.Student', on_delete=models.SET_NULL, null=True, blank=True, related_name="books")

    def __str__(self):
        return self.title



class UserClone(models.Model):
    username = models.CharField(max_length=100)


class CustomUser(AbstractUser):
    unique_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",  # Avoids conflict with default User
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions_set",  # Avoids conflict
        blank=True,
    )


