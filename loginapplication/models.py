from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    class Meta:
        db_table = "auth_user"

    ADMIN = "admin"
    TENANT = "tenant"
    LANDLORD = "landlord"

    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (TENANT, "Tenant"),
        (LANDLORD, "Landlord"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=TENANT)

    def is_admin(self):
        return self.role == self.ADMIN

    def is_tenant(self):
        return self.role == self.TENANT

    def is_landlord(self):
        return self.role == self.LANDLORD

    def __str__(self):
        return f"{self.username} - {self.role}"