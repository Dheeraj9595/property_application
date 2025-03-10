from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Owner, Property, RentalProperty

User = get_user_model()


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"
        
class RentalPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalProperty
        fields = "__all__"        
class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = "__all__"

# class BookSerializer(serializers.ModelSerializer):

#     user = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(), required=False, allow_null=True
#     )

#     class Meta:
#         model = Book
#         fields = ["id", "title", "author", "publication_date", "user", "student"]


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "username"]

# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'unique_id']
#         extra_kwargs = {'password': {'write_only': True}}
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user

# class StudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ['id', 'name', 'books']
