from rest_framework.serializers import ModelSerializer
from loginapplication.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ["id", "username", "email", "first_name", "last_name", "role"]