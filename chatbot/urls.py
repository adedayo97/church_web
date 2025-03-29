from django.urls import path
from . import views

urlpatterns = [
    path('response/', views.chat_response, name='chat_response'),
]