from django.urls import path, include
from .views import login_view, logout_view, UserViewset, ProfileView, ProfilePage, forgotpassword, changes_password_page, change_password
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("users", UserViewset)


urlpatterns = [
    path("auth/", include(router.urls)),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('api/token-auth/', obtain_auth_token, name='api_token_auth'),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile-page/", ProfilePage, name="profilepage"),
    path("forgetview/", forgotpassword, name="forgetview"),
    path("change-password-page/", changes_password_page, name="changepassword"),
    path("change-password/", change_password, name="changepasswordapi")

]
