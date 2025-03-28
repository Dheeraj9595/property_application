import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Owner, Property, RentalProperty
from .serializers import (OwnerSerializer, PropertySerializer,
                          RentalPropertySerializer)


@method_decorator(csrf_exempt, name="dispatch")
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().order_by('-id')
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            return JsonResponse({"message": "Property created", "data": data}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
@method_decorator(csrf_exempt, name="dispatch")
class RentalPropertyView(viewsets.ModelViewSet):
    queryset = RentalProperty.objects.all().order_by('-id')
    serializer_class = RentalPropertySerializer
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            return JsonResponse({"message": "Rental Property created", "data": data}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

@login_required
@csrf_exempt
@api_view(["POST"])
def property_form(request):
    serializer = PropertySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Property Created Successfully!"}, status=status.HTTP_201_CREATED)
    
    # Return errors if the request fails validation
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
def property_create(request):
    return render(request, 'property_form.html')

@login_required
def home(request):
    user = request.user
    if user.is_landlord():
        return redirect("property_form")
    if user.is_tenant():
        return redirect("buying")
    return render(request, "index.html")

@login_required
def aboutus(request):
    return render(request, 'subpage.html')


from django.http import HttpResponse
from django.template import loader


@login_required
def Property_list(request):
    mydata = Property.objects.all().order_by("-id")
    paginator = Paginator(mydata, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = loader.get_template('buying.html')
    context = {
        'properties': page_obj,
    }
    return HttpResponse(template.render(context, request))


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

@login_required
def Owner_list_view(request): 
    return render(request, 'owner.html')   


from django.http import JsonResponse
from django.shortcuts import redirect, render

from .forms import PropertyForm, RentalForm
from .models import Property


@login_required
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
    return render(request, "property_form.html", {"form": form})

@login_required
def rental_form_view(request):
    if request.method == "POST":
        # breakpoint()
        form = RentalForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Rental Property Created Successfully!"}, status=201)
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    
    form = RentalForm()
    return render(request, "rental_form.html", {"form": form})

def rental_home(request):
    return render(request, 'rental_home.html')


from django.shortcuts import get_object_or_404, render


@login_required
def rental_list(request):
    properties = RentalProperty.objects.all()
    return render(request, 'rental_list.html', {'properties': properties})
@login_required
def rental_detail(request, pk):
    property = get_object_or_404(RentalProperty, pk=pk)
    return render(request, 'rental_detail.html', {'property': property})
