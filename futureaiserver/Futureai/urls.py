from django.urls import path
from . import views

urlpatterns = [
    path('chatbot/', views.chatbot_page, name='chatbot_page'),  # GET: HTML page load
    path('chatbot/api/', views.AIresponce, name='chatbot_api'),  # POST: Ollama API response
]