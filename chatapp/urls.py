from django.urls import path
from .views import chatbot_response, chatbot_page

urlpatterns = [
    path("chat/", chatbot_response, name="chatbot-response"),
    path("chatbotpage/", chatbot_page, name="chatbotpage"),
]
