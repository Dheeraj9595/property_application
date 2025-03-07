import json

import requests
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Owner, Property
from .serializers import OwnerSerializer, PropertySerializer


@method_decorator(csrf_exempt, name="dispatch")
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().order_by('-id')
    serializer_class = PropertySerializer

    def create(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            return JsonResponse({"message": "Property created", "data": data}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)


@csrf_exempt
@api_view(["POST"])
def property_form(request):
    serializer = PropertySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Property Created Successfully!"}, status=status.HTTP_201_CREATED)
    
    # Return errors if the request fails validation
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def property_create(request):
    return render(request, 'property_form.html')

def home(request):
    return render(request, "index.html")

def aboutus(request):
    return render(request, 'subpage.html')


from django.http import HttpResponse
from django.template import loader

def Property_list(request):
    mydata = Property.objects.all().order_by("-id")
    template = loader.get_template('buying.html')
    context = {
        'properties': mydata,
    }
    return HttpResponse(template.render(context, request))

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    # pagination_class = 

def Owner_list_view(request): 
    return render(request, 'owner.html')   


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import PropertyForm
from .models import Property

def property_form_view(request):
    if request.method == "POST":
        # breakpoint()
        form = PropertyForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Property Created Successfully!"}, status=201)
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    
    form = PropertyForm()
    return render(request, "property_form2.html", {"form": form})
