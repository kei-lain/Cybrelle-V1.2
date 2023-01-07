from django.shortcuts import render 
from django.urls import  reverse_lazy
from .forms import RegistrationForm
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User

class customRegistrationView(CreateView):
    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    # fields =  '__all__'
    redirected_authenticated_user = True
    reverse_lazy =('/login')
    def get_object(self):
        return self.request.user