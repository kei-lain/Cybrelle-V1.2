from django.shortcuts import render
import json
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView
from .models import Host
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin, PermissionRequiredMixin
import zipp
from django.urls import  reverse_lazy
from django.conf import settings
from django.contrib.auth.models import User
from accounts.models import Organization


# Create your views here.

class HostsPage(LoginRequiredMixin,CreateView):
    template_name = 'hostspage.html'
    model = Host
    success_url = reverse_lazy('dashboard')

class CybrelleDashboard(LoginRequiredMixin,ListView):
    model = Host
    template_name = 'cybrelle_dashboard.html'
    def get_vuls(request):
        get_vulns_response = requests.get('127.0.0.1:8001/')
        get_vulns_response = json.loads(get_vulns_response)
        return(render(request,get_vulns_response))

class OrganizationAdmin(LoginRequiredMixin, ListView):
    model = Organization
    template_name = 'organization-admin.html'


class AccountInfo(DetailView):
    model = User
    template_name = 'accounts-page.html'


    


