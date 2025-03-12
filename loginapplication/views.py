from django.shortcuts import render
from loginapplication.serializers import UserSerializer
from loginapplication.models import User
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

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
    
@login_required    
def ProfilePage(request):
    return render(request, 'profile.html')    

from django.http import JsonResponse
import json
from django.core.mail import send_mail

@csrf_exempt
def forgotpassword(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')

            # Find user by username or email
            user = None
            if username:
                user = User.objects.filter(username=username).first()
            elif email:
                user = User.objects.filter(email=email).first()

            if not user:
                return JsonResponse({"error": "User not found"}, status=404)

            # Set and hash temporary password
            temporary_password = 'please_change@123'
            user.set_password(temporary_password)  # Hash the password
            user.save()

            # Send email
            send_mail(
                'Temporary Password',
                f'Temporary password: {temporary_password}\n\n'
                'This is a system-generated password. Please change it after first login.',
                'dheeraj.systango@gmail.com',  # Sender
                [user.email],  # Recipient
                fail_silently=False
            )

            return JsonResponse({
                "message": f"Temporary password has been sent to {user.email}. Please change it after first login."
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def changes_password_page(request):
    return render(request, 'change_password_page.html')

from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

User = get_user_model()

@csrf_exempt
def change_password(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            old_password = data.get("old_password")
            new_password = data.get("new_password")

            if not old_password or not new_password:
                return JsonResponse({"detail": "Both old and new passwords are required."}, status=400)

            user = request.user  # Get logged-in user
            if not check_password(old_password, user.password):
                return JsonResponse({"detail": "Old password is incorrect."}, status=400)

            user.set_password(new_password)  # Securely hash new password
            user.save()

            return JsonResponse({"detail": "Password updated successfully."})

        except json.JSONDecodeError:
            return JsonResponse({"detail": "Invalid JSON data."}, status=400)

    return JsonResponse({"detail": "Invalid request method."}, status=405)
