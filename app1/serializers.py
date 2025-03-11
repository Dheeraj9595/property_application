from rest_framework import serializers

from .models import Owner, Property, RentalProperty

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