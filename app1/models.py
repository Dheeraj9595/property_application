import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class Owner(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    PROPERTY_TYPES = [
        ("HOUSE", "House"),
        ("APARTMENT", "Apartment"),
        ("COMMERCIAL", "Commercial"),
        ("LAND", "Land"),
        ("VILLA", "Villa"),
        ("FARMHOUSE", "Farmhouse"),
    ]

    PROPERTY_SUBTYPES = [
        ("2BHK", "2BHK"),
         ("3BHK","3BHK"),
         ("4BHK","4BHK"),
         ("VILLA","VILLA"),
         ("PANT HOUSE","PANT HOUSE"),
         ("OTHERS","OTHERS")
    ]

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(
        Owner, on_delete=models.CASCADE, related_name="properties"
    )
    area = models.CharField(max_length=50)
    property_type = models.CharField(
        max_length=20, choices=PROPERTY_TYPES, default="HOUSE"
    )
    property_subtype = models.CharField(
        max_length=20, choices=PROPERTY_SUBTYPES, default="OTHERS"
    )

    def __str__(self):
        return f"{self.title} - {self.get_property_type_display()} - {self.owner.name}"
    
class RentalProperty(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255)
    property_type = models.CharField(max_length=50, choices=[("Apartment", "Apartment"), ("House", "House"), ("Office", "Office"), ("COMMERCIAL", "Commercial"), ("VILLA", "Villa")])
    property_subtype = models.CharField(
        max_length=20, choices=[
        ("2BHK", "2BHK"),
         ("3BHK","3BHK"),
         ("4BHK","4BHK"),
         ("VILLA","VILLA"),
         ("PANT HOUSE","PANT HOUSE"),
         ("OTHERS","OTHERS")], default="OTHERS"
    )
    rent_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_from = models.DateField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="rental_properties")

    def __str__(self):
        return self.title    