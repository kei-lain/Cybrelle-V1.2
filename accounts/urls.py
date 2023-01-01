from django.contrib import admin
from django.urls import path , include
from .views import customRegistrationView

urlpatterns = [
    path('register/', customRegistrationView.as_view(), name='register'),
    
]


