from django.shortcuts import render
from loginapplication.serializers import UserSerializer
from loginapplication.models import User
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("http://localhost:8000/api/home/")  # Redirect to home page or dashboard
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")    


from django.shortcuts import redirect
from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect("login")  # Redirect to login page after logout

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

@method_decorator(csrf_exempt, name="dispatch")
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    


    def get_object(self):
        return self.request.user
    
def ProfilePage(request):
    return render(request, 'profile.html')    
    
